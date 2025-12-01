from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils.timezone import now, timedelta
from localshop.models import Product
from accounts.models import CustomUser

class Command(BaseCommand):
    help = 'Send email notifications about products with discount or nearing expiry'

    def handle(self, *args, **kwargs):
        today = now().date()
        upcoming_days = today + timedelta(days=3) 

        products = Product.objects.filter(discount__gt=0, expiry_date__gte=today, notified_about_discount=False)
        if not products:
            self.stdout.write('No products to notify.')
            return

        users = CustomUser.objects.filter(is_active=True)
        for product in products:
            for user in users:
                subject = f"Скидка на товар {product.name}"
                message = (
                    f"Привет, {user.username}!\n\n"
                    f"На товар {product.name} действует скидка {product.discount}%.\n"
                    f"Срок годности: {product.expiry_date}\n\n"
                    f"Поторопитесь приобрести!"
                )
                send_mail(subject, message, None, [user.email], fail_silently=False)
            product.notified_about_discount = True
            product.save()
            self.stdout.write(f'Notification sent for product {product.name}')
