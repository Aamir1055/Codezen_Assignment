from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Customer, Seller, Product, Order, PlatformApiCall

admin.site.register(Customer)
admin.site.register(Seller)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(PlatformApiCall)
