from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.
class CustomUser(AbstractUser):
    firstname = models.CharField(max_length = 50, null = True)
    lastname = models.CharField(max_length = 50, null = True)
    def __str__(self):
        return self.email

class Item(models.Model):
    name = models.CharField(max_length = 100, null = True)
    descr = models.CharField(max_length = 200, null = True)
    price = models.FloatField(default = 0)

class Orders(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    item = models.ForeignKey(Item, on_delete = models.CASCADE, related_name = "conf_item", null = True)

class CartOrders(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    item = models.ForeignKey(Item, on_delete = models.CASCADE, related_name = "cart_item", null = True)