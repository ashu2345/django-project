from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.
class CustomUser(AbstractUser):
    firstname = models.CharField(max_length = 50, null = True)
    lastname = models.CharField(max_length = 50, null = True)
    def __str__(self):
        return self.email

class Orders(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    item_name = models.CharField(max_length = 40)
    order_time = models.DateField(default = timezone.now)