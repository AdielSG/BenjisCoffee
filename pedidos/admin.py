from django.contrib import admin
from .models import Order, Product, Cart, CartItem, OrderItem, Rewards

# class OrderAdmin(admin.ModelAdmin):
#     readonly_fields = ("created", )

# Register your models here.

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Rewards)
