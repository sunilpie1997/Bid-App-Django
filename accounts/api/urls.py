from django.urls import path
from .views import *
from . import views




urlpatterns=[
    path('',UserRetrieveUpdateAPIView.as_view(),name='user-detail-or-update'),#for get and patch request same view
    #NOT for put request
    path('profile/<str:filename>/',ProfileImageUploadView.as_view(),name='profile-photo-upload'),#patch request
    path('create/',UserCreateAPIView.as_view(),name='user-create'),
    path('<str:username>/',UserByAdminAPIView.as_view(),name='user-by-admin'),#for get,PUT,delete request
]
    