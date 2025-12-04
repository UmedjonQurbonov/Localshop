from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ["username", "id", "email", "password"]
    # list_select_related = ["profile"]
    readonly_fields = ["email"]
    search_fields = ["username"]
admin.site.register(CustomUser, CustomUserAdmin)
