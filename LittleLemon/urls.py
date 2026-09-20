"""
URL configuration for LittleLemon project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from restaurant.views import IndexView, MenuListView
from django.contrib.auth.views import LoginView, LogoutView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('restaurant.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/token/login/', obtain_auth_token, name='token_login'),

    path('auth/', include('djoser.urls.authtoken')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/users/', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
    
    path('login/', LoginView.as_view(template_name='LittleLemonAPI/login.html', next_page='menu-items'), name='login'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('', IndexView.as_view(), name='index'), 
    path('menu/', MenuListView.as_view(), name='menu-items'),
]
