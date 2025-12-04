from django.views.generic import ListView,DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from datetime import date
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import requests

def send_telegram_message(token, chat_id, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, data=payload)


class CategoryListView(ListView):
    model = Category
    template_name = "category_list.html"
    context_object_name = "categories"

from datetime import date

class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_id = self.kwargs['category_id']

        expired = Product.objects.filter(expiry_date__lt=date.today(), is_deleted=False)
        for product in expired:
            DeletedProduct.objects.create(product=product)
            product.is_deleted = True
            product.save()
        return Product.objects.filter(
            category_id=category_id,
            expiry_date__gte=date.today(),
            is_deleted=False
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs['category_id']
        context['category'] = Category.objects.get(id=category_id)
        return context



class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        if product.discount:
            context['discount_price'] = product.price * (100 - product.discount) / 100
            if product.expiry_date:
                remaining_days = (product.expiry_date - date.today()).days
                context['remaining_days'] = remaining_days if remaining_days > 0 else 0
        else:
            context['discount_price'] = product.price
        return context


class DeletedProductListView(ListView):
    model = DeletedProduct
    template_name = 'deleted_products.html'
    context_object_name = 'deleted_products'

class CartView(LoginRequiredMixin, ListView):
    template_name = 'cart.html'
    context_object_name = 'items'

    def get_queryset(self):
        order = Order.objects.filter(user=self.request.user, status='new').first()
        if order:
            return order.orderitem_set.all()
        return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = context['items']
        total = sum([item.total_price() for item in items])
        context['total_price'] = total
        return context

def get_or_create_order(user):
    order, created = Order.objects.get_or_create(user=user, status='new')
    return order

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    order = get_or_create_order(request.user)
    quantity = int(request.POST.get('quantity', 1))

    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
    if not created:
        order_item.quantity += quantity
    else:
        order_item.quantity = quantity
    order_item.save()

    return redirect('category_list')

def send_telegram_message(text):
    TG_TOKEN = "8358129923:AAFk230-gOABG0TagvKRAHKRS41YaCGw8Yg"
    TG_CHAT_ID = 1066934350
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    payload = {"chat_id": TG_CHAT_ID, "text": text}
    requests.post(url, data=payload)

class CheckoutView(LoginRequiredMixin, TemplateView):
    template_name = 'checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = Order.objects.filter(user=self.request.user, status='new').first()
        if order:
            context['items'] = order.orderitem_set.all()
            context['total_price'] = sum([item.total_price() for item in context['items']])
        else:
            context['items'] = []
            context['total_price'] = 0
        return context

    def post(self, request, *args, **kwargs):
        order = Order.objects.filter(user=request.user, status='new').first()
        if order:
            for item in order.orderitem_set.all():
                product = item.product
                if product.quantity >= item.quantity:
                    product.quantity -= item.quantity
                else:
                    product.quantity = 0
                product.save()

            order.status = 'confirmed'
            order.save()

            tg_message = f"Новый заказ от {request.user.email}:\n"
            for item in order.orderitem_set.all():
                tg_message += f"{item.product.name} - {item.quantity} шт.\n"
            tg_message += f"Общая сумма: {sum([i.total_price() for i in order.orderitem_set.all()])} сомони"

            send_telegram_message(tg_message)

        return redirect('cart')

class MyOrdersListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'my_orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        orders = Order.objects.filter(user=self.request.user).order_by('-created_at')
        for order in orders:
            order.total_price = sum(item.total_price() for item in order.orderitem_set.all())
        return orders