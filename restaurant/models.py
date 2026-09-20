from django.db import models
from django.conf import settings

class Category(models.Model):
    slug = models.SlugField(db_index=True)
    title = models.CharField(max_length=255, db_index=True)
    class Meta:
        verbose_name_plural = "Categories"
    def __str__(self):
        return self.title

class Menu(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, db_index=True)
    featured = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="menu_items")
    def __str__(self):
        return self.title

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name="bookings")
    first_name = models.CharField(max_length=255, db_index=True)
    email = models.EmailField()
    date = models.DateField(db_index=True)
    time = models.TimeField(db_index=True)
    number_of_people = models.PositiveIntegerField()
    special_requests = models.TextField(blank=True, null=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["first_name", "email", "date", "time"], name="unique_booking"
            )
        ]
    def __str__(self):
        return f"Booking for {self.first_name} on {self.date} at {self.time}"   

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart_items",)
    menuitem = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="in_carts",)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "menuitem"], name="unique_user_menuitem_cart"
            )
        ]
    def __str__(self):
        return f"{self.user.username}'s cart: {self.menuitem.title} (x{self.quantity})"

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    delivery_crew = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="deliveries_assigned", null=True, blank=True,)
    status = models.BooleanField(default=False, db_index=True)
    date = models.DateField(db_index=True)
    total = models.DecimalField(max_digits=6, decimal_places=2)
    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    menuitem = models.ForeignKey(Menu,on_delete=models.CASCADE, related_name="in_orders")
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ["order", "menuitem"], name="unique_order_menuitem_orderitem"
            )
        ]
    def __str__(self):
        return f"Order #{self.order.id} item: {self.menuitem.title}"

