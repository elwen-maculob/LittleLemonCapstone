from rest_framework import generics, permissions, status
from django.contrib.auth.models import User, Group
from rest_framework.permissions import (IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser)
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from datetime import date
from django.views.generic import TemplateView, ListView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect

from .models import Menu, Order, Cart, OrderItem, Booking
from .serializers import UserSerializer, MenuSerializer, CustomerOrderSerializer, CartSerializer, ManagerOrderSerializer, DeliveryOrderSerializer, OrderItemSerializer, BookingSerializer
from .permissions import IsDeliveryCrew, IsManagerOrReadOnly, IsCustomer

#1. displays menuitem even for all, GET only for C's
#/api/menu-items/
class MenuView(generics.ListCreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsManagerOrReadOnly]

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['category']
    search_fields = ['title']
    ordering_fields = ['price']

#2. displays cart for C's orders
#/api/cart/menu-items/
class CartView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsCustomer]

#3. displays all orders
#/api/orders
class OrderView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Manager").exists() or user.is_staff:
            return Order.objects.all()
        if user.groups.filter(name="Delivery crew").exists():
            return Order.objects.filter(delivery_crew=user)
        return Order.objects.filter(user=user)
    def get_serializer_class(self):
        user = self.request.user
        if user.groups.filter(name="Manager").exists() or user.is_staff:
            return ManagerOrderSerializer
        return CustomerOrderSerializer
    def post(self, request, *args, **kwargs):
        if request.user.groups.filter(name__in=["Manager", "Deliver crew"]).exists() and not request.user.is_superuser:
            return Response({'detail' : "Only customers can place orders."}, status=status.HTTP_403_FORBIDDEN)
        return self.create(request, *args, **kwargs)
    def create(self, request, *args, **kwargs):
        user = request.user
        cart_items = Cart.objects.filter(user=user)
        if not cart_items.exists():
            return Response({"detail": "Cart is empty."}, status=status.HTTP_400_BAD_REQUEST)
        total = sum(item.price for item in cart_items)
        order = Order.objects.create(
            user=user,
            total=total,
            date=date.today()
        )
        order_items = [
            OrderItem(
                order=order,
                menuitem=item.menuitem,
                quantity=item.quantity,
                unit_price=item.unit_price,
                price=item.price
               )
            for item in cart_items

        ]
        OrderItem.objects.bulk_create(order_items)
        cart_items.delete()
        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
#4. diplays single order from each C's
#/api/orders/id
class SingleOrderView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Manager").exists() or user.is_staff:
            return Order.objects.all()
        if user.groups.filter(name="Delivery crew").exists():
            return Order.objects.filter(delivery_crew=user)
        return Order.objects.filter(user=user)
    def get_serializer_class(self):
        user = self.request.user
        if user.groups.filter(name="Manager").exists() or user.is_staff:
            return ManagerOrderSerializer
        if user.groups.filter(name="Delivery crew").exists():
            return DeliveryOrderSerializer
        return CustomerOrderSerializer
    def delete(self, request, *args, **kwargs):
        user = self.request.user
        if not user.groups.filter(name="Manager").exists() or user.is_staff:
            return Response({"detail": "Only managers can delete orders."}, status=status.HTTP_403_FORBIDDEN)
        return self.destroy(request, *args, **kwargs)
    def patch(self, request, *args, **kwargs):
        user = self.request.user
        order = self.get_object()
        if user.groups.filter(name="Delivery crew").exists() and not (user.groups.filter(name="Manager").exists() or user.is_staff):
            if order.status is True:
                return Response({"detail": "This has already been delivered. Call manager to revert status."},status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.patch(request, *args, **kwargs)
#5. diplays order item for M's
#/api/order-items
class OrderItemView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderItemSerializer
    def get_queryset(self):
        user=self.request.user
        if user.groups.filter(name="Manager").exists() or user.is_staff:
            return OrderItem.objects.all()
        raise PermissionDenied("Only managers can view order items.")

#6. handles Manager group
#/api/groups/manager/users
#/api/groups/manager/users/pk
class ManagerGroupView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    def get_queryset(self):
        return User.objects.filter(groups__name="Manager")
    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        if not username:
            return Response({"detail": "Input valid username."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(username=username)
            manager_group = Group.objects.get(name="Manager")
            user.groups.add(manager_group)
            return Response({"detail": f"User {username} successfully added as manager"})
        except User.DoesNotExist:
            return Response({"detail": f"Sorry, user {username} not found."}, status=status.HTTP_404_NOT_FOUND)
class ManagerGroupDeleteView(generics.RetrieveDestroyAPIView):
    queryset = User.objects.filter(groups__name="Manager")
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    def destroy(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        try:
            user = User.objects.get(pk=user_id)
            manager_group = Group.objects.get(name="Manager")
            user.groups.remove(manager_group)
            return Response({"detail": f"User {user} successfully removed as Manager"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"detail": f"User {user} not found."}, status=status.HTTP_404_NOT_FOUND)

#7. handles delivery crew group
#/api/groups/delivery-crew/users
#/api/groups/delivery-crew/users/pk
class DeliveryCrewGroupView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    def get_queryset(self):
        return User.objects.filter(groups__name="Delivery crew")
    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        if not username:
            return Response({"detail": "Input valid username."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(username=username)
            delivery_crew_group = Group.objects.get(name="Delivery crew")
            user.groups.add(delivery_crew_group)
            return Response({"detail": f"User {username} successfully added as delivery crew."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"detail": f"Sorry, user {username} not found."}, status=status.HTTP_404_NOT_FOUND)
class DeliveryCrewDeleteView(generics.RetrieveDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    queryset = User.objects.filter(groups__name="Delivery crew")
    def destroy(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        try:
            user = User.objects.get(pk=user_id)
            delivery_crew_group = Group.objects.get(name="Delivery crew")
            user.groups.remove(delivery_crew_group)
            return Response({"detail:": f"User {user} successfully removed as delivery crew"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"detail": f"User {user} not found."}, status=status.HTTP_404_NOT_FOUND)
        
        
#8. all users display
#/api/users/
class UserView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()

class BookingView(generics.ListCreateAPIView):
    serializer_class = BookingSerializer
    def get_queryset(self):
        if self.request.user.groups.filter(name="Manager").exists() or self.request.user.is_staff:
            return Booking.objects.all()
        return Booking.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [permissions.IsAuthenticated, IsCustomer]
        elif self.request.method == 'GET':
            self.permission_classes = [permissions.IsAuthenticated, IsManagerOrReadOnly]
        return super().get_permissions()
class SingleBookingView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookingSerializer
    def get_queryset(self):
        if self.request.user.groups.filter(name="Manager").exists() or self.request.user.is_staff:
            return Booking.objects.all()
        return Booking.objects.filter(user=self.request.user)
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [permissions.IsAuthenticated, IsManagerOrReadOnly]
        else:
            self.permission_classes = [permissions.IsAuthenticated] 
        return super().get_permissions()

#9 HTML views
class IndexView(TemplateView):
    template_name = 'LittleLemonAPI/index.html'
    def post(self, request, *args, **kwargs):
        first_name = request.POST.get('first_name')
        date = request.POST.get('date')
        time = request.POST.get('time')
        raw_guest_count = request.POST.get('number_of_guests')
        number_of_guests = int(raw_guest_count) if raw_guest_count else 1
        special_requests = request.POST.get('special_requests', '')
        # Create a new Booking instance
        Booking.objects.create(
            user=request.user,
            first_name=first_name,
            date=date,
            time=time,
            number_of_people=number_of_guests,
            special_requests=special_requests
        )
        context = {'success_message': 'Booking created successfully.'}
        return render(request, self.template_name, context)

class MenuListView(LoginRequiredMixin, ListView):
    model = Menu
    template_name = 'LittleLemonAPI/menu_items.html'
    context_object_name = 'menu_items'
    login_url = '/login/'  
    def post(self, request, *args, **kwargs):
        menuitem_id = request.POST.get('menuitem_id')
        menu_item  = get_object_or_404(Menu, id=menuitem_id)
        cart_item, created = Cart.objects.get_or_create(
            user=request.user if request.user.is_authenticated else None,
            menuitem=menu_item,
            defaults={
                'quantity': 1,
                'unit_price': menu_item.price,
                'price': menu_item.price
            }
        )
        if not created:
            cart_item.quantity += 1
            cart_item.price = cart_item.unit_price * cart_item.quantity
            cart_item.save()
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        context['success_message'] = f'Added {menu_item.title} to cart.'
        return self.render_to_response(context)

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'LittleLemonAPI/signup.html'
    success_url = reverse_lazy('login')

class CartListView(LoginRequiredMixin, ListView):
    model = Cart
    template_name = 'LittleLemonAPI/cart.html'
    context_object_name = 'cart_items'
    login_url = '/login/'  
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = self.get_queryset()
        total_price = sum(item.price for item in cart_items) if cart_items else 0
        context['total_price'] = total_price
        return context

class CheckoutView(LoginRequiredMixin, View):
    login_url = '/login/'
    def post(self, request, *args, **kwargs):
        user = request.user
        cart_items = Cart.objects.filter(user=user)
        if not cart_items.exists():
            return redirect('cart')
        total = sum(item.price for item in cart_items)
        order = Order.objects.create(
            user=user,
            total=total,
            date=date.today(),
            status=False
        )
        order_items = [
            OrderItem(
                order=order,
                menuitem=item.menuitem,
                quantity=item.quantity,
                unit_price=item.unit_price,
                price=item.price
            )
            for item in cart_items
        ]
        OrderItem.objects.bulk_create(order_items)
        cart_items.delete()
        return redirect('order-success')

class OrderSuccessView(TemplateView):
    template_name = 'LittleLemonAPI/order_success.html'
    login_url = '/login/'