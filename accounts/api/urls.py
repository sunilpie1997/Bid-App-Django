from django.urls import path
from .views import *
from . import views




urlpatterns=[

    #for get and patch request same view
    path('',UserRetrieveUpdateAPIView.as_view(),name='user-detail-or-update'),
    
    #for viewing..GET request
    path('image/',ProfileImageView.as_view(),name='profile-image-view'),

    #post request
    path('profile/<str:filename>/',ProfileImageUploadView.as_view(),name='profile-image-upload'),

    path('create/',UserCreateAPIView.as_view(),name='user-create'),
    
    path('<str:username>/',UserByAdminAPIView.as_view(),name='user-by-admin'),#for get,PUT,delete request
]
    