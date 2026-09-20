from rest_framework import serializers
from decimal import Decimal
from django.contrib.auth.models import User, Group
from .models import Category, Menu, Cart, OrderItem, Order, Booking

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            'id',
            'first_name',
            'email',
            'date',
            'time',
            'number_of_people',
            'special_requests'
        ]

class MenuSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Menu
        fields = [
            'id',
            'title',
            'price',
            'featured',
            'category',
            'category_id',
        ]

class CartSerializer(serializers.ModelSerializer):
    menuitem = MenuSerializer(read_only=True)
    menuitem_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Cart
        fields = [
            'id',
            'user',
            'price',
            'unit_price',
            'quantity',
            'menuitem',
            'menuitem_id',
        ]
        read_only_fields = ['user', 'price', 'unit_price']

    def create(self, validated_data):
        menuitem_id = validated_data.pop("menuitem_id")
        try:
            menuitem = Menu.objects.get(id=menuitem_id)
        except Menu.DoesNotExist:
            raise serializers.ValidationError(
                {"menuitem_id" : "Invalid menu item ID."}
            )
        quantity = validated_data.get("quantity")
        unit_price = menuitem.price
        user = self.context["request"].user
        cart_item, created = Cart.objects.get_or_create(
            user=user,
            menuitem=menuitem,
            defaults={
                "quantity" : quantity,
                "unit_price" : unit_price,
                "price" : unit_price * quantity,
            },
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.price = cart_item.unit_price * cart_item.quantity
            cart_item.save()
        return cart_item

class OrderItemSerializer(serializers.ModelSerializer):
    menuitem = MenuSerializer(read_only=True)
    class Meta:
        model = OrderItem
        fields = [
            'id',
            'order',
            'menuitem',
            'quantity',
            'unit_price',
            'price',  
        ]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {"password": {"write_only": True}}
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class CustomerOrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Order
        fields = [
            'id',
            'status',
            'user',
            'delivery_crew',
            'delivery_crew_id',
            'date',
            'total',
        ]
        read_only_fields = ['status', 'user', 'delivery_crew', 'date', 'total',]
class ManagerOrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    delivery_crew = UserSerializer(read_only=True)
    delivery_crew_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(groups__name="Delivery crew"),
        source="delivery_crew",
        required=False,
        allow_null=True
    )
    class Meta:
        model = Order
        fields = [
            'id',
            'status',
            'user',
            'delivery_crew',
            'delivery_crew_id',
            'date',
            'total',
        ]
        read_only_fields = [
            'user',
            'total',
            'date',
        ]
class DeliveryOrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    delivery_crew = UserSerializer(read_only=True)
    class Meta:
        model = Order
        fields = [
                'id',
                'status',
                'user',
                'delivery_crew',
                'date',
                'total',
        ]
        read_only_fields = [
                'id',
                'user',
                'total',
                'date',
                'delivery_crew'
        ]