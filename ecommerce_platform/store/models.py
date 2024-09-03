from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Seller(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)  # Add this line

    def __str__(self):
        return f"Order #{self.id} by {self.customer.name}"


class PlatformApiCall(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    requested_url = models.URLField()
    requested_data = models.JSONField()
    response_data = models.JSONField()

    def __str__(self):
        return f"API Call by {self.user.username}"
