from django.contrib import admin
from .models import Order

# class OrderAdmin(admin.ModelAdmin):
#     readonly_fields = ("created", )

# Register your models here.

admin.site.register(Order)
