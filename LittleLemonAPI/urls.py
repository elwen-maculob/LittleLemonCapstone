from django.urls import path
from . import views
from .views import IndexView, MenuItemsListView, CartListView, ManagerGroupView, ManagerGroupDeleteView, DeliveryCrewGroupView, DeliveryCrewDeleteView, SignUpView, OrderSuccessView, CheckoutView

urlpatterns = [
    path('menu-items', views.MenuItemsView.as_view()),
    path('cart/menu-items', views.CartView.as_view()),
    path('orders', views.OrderView.as_view()),
    path('orders/<int:pk>', views.SingleOrderView.as_view()),
    path('order-items', views.OrderItemView.as_view()),
    path('users', views.UserView.as_view()),
    path('groups/manager/users', views.ManagerGroupView.as_view()),
    path('groups/manager/users/<int:pk>', views.ManagerGroupDeleteView.as_view()),
    path('groups/delivery-crew/users', views.DeliveryCrewGroupView.as_view()),
    path('groups/delivery-crew/users/<int:pk>', views.DeliveryCrewDeleteView.as_view()),
    path('bookings', views.BookingView.as_view()),
    path('bookings/<int:pk>', views.SingleBookingView.as_view()),
    path('', views.IndexView.as_view(), name='index'),
    path('menu/', views.MenuItemsListView.as_view(), name='menu-items'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('cart/', views.CartListView.as_view(), name='cart'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('order-success/', views.OrderSuccessView.as_view(), name='order-success'),
]