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
