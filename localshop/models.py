from django.db import models
from accounts.models import CustomUser

class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField()

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10,   decimal_places=2)
    quantity = models.PositiveIntegerField()
    expiry_date = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='products/', blank=True)
    discount = models.PositiveIntegerField(default=0)
    is_deleted = models.BooleanField(default=False)

class DeletedProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name="deleted_record")
    deleted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=[('new','New'),('confirmed','Confirmed'),('shipped','Shipped'),('delivered','Delivered')])

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity

