from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    pass

class Supply(models.Model):
    name = models.CharField(max_length=100, unique=True)
    quantity = models.IntegerField()
    display = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return self.name
    
class Cashier(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()

    def __str__(self):
        return f'{self.name} - {self.date}'

class Product(models.Model):
    cashier = models.ForeignKey(Cashier, on_delete=models.CASCADE)
    product_name = models.ForeignKey(Supply, to_field='name', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    display = models.BooleanField(default=False)
    expenses = models.IntegerField()
    sale = models.IntegerField()

    def __str__(self):
        return self.product_name
    
class Report(models.Model):
    cashier = models.ForeignKey(Cashier, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    display = models.BooleanField(default=False)
    expenses = models.IntegerField()
    sale = models.IntegerField()
    

    def __str__(self):
        return self.product_name.name
    
class OldStock(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    display = models.BooleanField(default=False)
    saved_at = models.DateTimeField(auto_now_add=True)