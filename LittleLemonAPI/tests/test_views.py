from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from LittleLemonAPI.models import Category, MenuItem
from LittleLemonAPI.serializers import MenuItemSerializer

User = get_user_model()

class MenuViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client.force_login(self.user)

        self.category = Category.objects.create(title="Desserts", slug="desserts")
        
        MenuItem.objects.create(
            title="Ice Cream",
            price=5.50,
            featured=True,
            category=self.category
        )
        MenuItem.objects.create(
            title="Chocolate Cake",
            price=8.00,
            featured=False,
            category=self.category
        )

    def test_get_all(self):
        # Target your actual API endpoint URL directly
        response = self.client.get('/api/menu-items')
        
        menu_items = MenuItem.objects.all()
        serializer = MenuItemSerializer(menu_items, many=True)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], serializer.data)