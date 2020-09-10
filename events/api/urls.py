from django.urls import path

from .views import *




urlpatterns=[
    
    #event
    path('',EventListAPIView.as_view(),name='event-list'),
    path('<int:pk>/',EventRetrieveAPIView.as_view(),name='event-detail'),
    path('<int:pk>/destroy/',EventDestroyAPIView.as_view(),name='event-destroy'),
    path('create/',EventCreateAPIView.as_view(),name='event-create'),
    
    #event product image uload view
    #post request
    path('<int:event_id>/image/<str:filename>/',ProductImageUploadView.as_view(),name='product-image-upload'),

    #bids
    path('<int:event_id>/bids/',BidListAPIView.as_view(),name='bid-list'),
    path('<int:event_id>/highest_bid/',HighestBidRetrieveAPIView.as_view(),name='highest-bid'),
    path('<int:event_id>/bids/create/',BidCreateAPIView.as_view(),name='bid-create'),

]