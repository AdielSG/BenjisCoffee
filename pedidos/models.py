from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Order(models.Model):
    Cliente = models.CharField(max_length=100)
    Orden = models.CharField(max_length=100)
    Precio = models.IntegerField()
    Completado = models.BooleanField(blank=True, default=False)
    datecompleted = models.DateTimeField(null=True, blank=True)
    Extras = models.CharField(max_length=100 ,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.Cliente + ' Pedido ' + self.Orden
