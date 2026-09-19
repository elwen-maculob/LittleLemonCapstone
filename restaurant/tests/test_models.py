from datetime import date, time
from django.contrib.auth import get_user_model
from django.test import TestCase
from restaurant.models import Category, MenuItem, Cart, Order, OrderItem, Booking

User = get_user_model()

class AllModelsTest(TestCase):
    def setUp(self):
        # Create a sample user for related models
        self.user = User.objects.create_user(username="testuser", password="password123")
        
        # Create Category and MenuItem
        self.category = Category.objects.create(title="Appetizers", slug="appetizers")
        self.menu_item = MenuItem.objects.create(
            title="Spring Rolls",
            price=10.50,
            featured=True,
            category=self.category
        )

    def test_category_str(self):
        self.assertEqual(str(self.category), "Appetizers")

    def test_menu_item_str(self):
        self.assertEqual(str(self.menu_item), "Spring Rolls")

    def test_cart_str(self):
        cart = Cart.objects.create(
            user=self.user,
            menuitem=self.menu_item,
            quantity=2,
            unit_price=10.50,
            price=21.00
        )
        self.assertEqual(str(cart), "testuser's cart: Spring Rolls (x2)")

    def test_order_str(self):
        order = Order.objects.create(
            user=self.user,
            status=False,
            date=date.today(),
            total=21.00
        )
        self.assertEqual(str(order), f"Order #{order.id} - testuser")

    def test_order_item_str(self):
        order = Order.objects.create(
            user=self.user,
            status=False,
            date=date.today(),
            total=21.00
        )
        order_item = OrderItem.objects.create(
            order=order,
            menuitem=self.menu_item,
            quantity=2,
            unit_price=10.50,
            price=21.00
        )
        self.assertEqual(str(order_item), f"Order #{order.id} item: Spring Rolls")

    def test_booking_str(self):
        booking = Booking.objects.create(
            user=self.user,
            first_name="Elwen",
            email="elwen@example.com",
            date=date(2026, 12, 25),
            time=time(18, 30),
            number_of_people=4
        )
        self.assertEqual(str(booking), "Booking for Elwen on 2026-12-25 at 18:30:00")