from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.

class Product(models.Model):
    Nombre = models.CharField(max_length=100)
    Precio = models.IntegerField()
    Descripcion = models.CharField(max_length=100)
    Disponibilidad = models.BooleanField()
    picture = models.CharField(max_length=4000)

    def __str__(self):
        return self.Nombre + '  ' + str(self.Precio) + '  Pesos'
    

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    completed = models.BooleanField(default=False)
    listo = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
    
    @property
    def total_price(self):
        cartitems = self.cartitems.all()
        total = sum([item.price for item in cartitems])
        return total
    
    @property
    def num_of_items(self):
        caritems = self.cartitems.all()
        quantity = sum([item.quantity for item in caritems])
        return quantity
    
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cartitems')
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.product.Nombre
    
    @property
    def price(self):
        new_price = self.product.Precio * self.quantity
        return new_price
    

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='itemsfororder')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderitems')
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.product.Nombre
    
class Rewards(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Quantity = models.IntegerField(default=0)

    def __str__(self):
        return str(self.Quantity)
