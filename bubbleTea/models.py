from django.db import models


# Create your models here.

class Product(models.Model):
    identifier = models.CharField(max_length=79)
    description = models.TextField(max_length=125)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    picture = models.ImageField(upload_to="images", null=True, blank=True)
    stock = models.IntegerField
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField

class User(models.Model):
    name = models.CharField(max_length=30)
    firstname = models.CharField(max_length=30)
    email = models.EmailField(max_length=254)
    picture = models.ImageField(upload_to="images", null=True, blank=True)
    password1 = models.CharField(max_length=1000)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField

class Cart(models.Model):
    print('test')
