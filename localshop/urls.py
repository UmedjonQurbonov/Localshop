from django.urls import path
from .views import *

urlpatterns = [
    path('category/', CategoryListView.as_view(), name='category_list'),
    path('category/<int:category_id>/products/', ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('deleted/', DeletedProductListView.as_view(), name='deleted_list'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='cart_add'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('my-orders/', MyOrdersListView.as_view(), name='my_orders'),
]
