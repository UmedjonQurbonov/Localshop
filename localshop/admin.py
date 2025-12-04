from django.contrib import admin
from .models import *


class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "quantity", "category"]
    list_select_related = ["category"]
    readonly_fields = ["discount"]
    search_fields = ["name", "quantity"]
    
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Product, ProductAdmin)