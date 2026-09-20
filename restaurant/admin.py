from django.contrib import admin
from .models import Booking, Category, Menu, Order, OrderItem, Cart
# Register your models here.
admin.site.register(Category)
admin.site.register(Menu)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Cart)
admin.site.register(Booking)