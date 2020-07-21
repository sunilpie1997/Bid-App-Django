"""bid_app_rest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path,include
from events import views
from . import token_views

urlpatterns = [
    path('',views.homepage,name="home"),
    path('admin/', admin.site.urls),
    path('auth/login/', token_views.MyTokenObtainPairView.as_view(), name='auth-login'),
    path('user/',include('accounts.api.urls'),name='user-api' ),
    path('api/events/',include('events.api.urls'),name='event-api' ),

    
    


]
