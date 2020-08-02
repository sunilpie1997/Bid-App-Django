from events.models import Event,Product,Bid
from .serializers import EventSerializer,ProductSerializer,EventCreateSerializer,BidSerializer,BidCreateSerializer
from rest_framework import generics
from rest_framework.permissions import IsAdminUser,IsAuthenticated,AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.api.serializers import UserSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

User=get_user_model()

#Event view

class EventRetrieveAPIView(generics.RetrieveAPIView):
    queryset=Event.objects.all()
    serializer_class=EventSerializer
    permission_classes=[AllowAny]
  
    

class EventDestroyAPIView(generics.DestroyAPIView):
    queryset=Event.objects.all()
    serializer_class=EventSerializer
    permission_classes=[IsAdminUser]

class EventCreateAPIView(generics.CreateAPIView):
    queryset=Event.objects.all()
    serializer_class=EventCreateSerializer
    permission_classes=[IsAuthenticated]

class EventListAPIView(generics.ListAPIView):
    queryset=Event.objects.all().order_by("-date_added")
    serializer_class=EventSerializer
    permission_classes=[AllowAny]

#Bids view

class BidListAPIView(generics.ListAPIView):
    serializer_class=BidSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        """
        This view returns a list of all bids placed for
        the event as determined by the event_id portion of the URL.
        """
        event_id = self.kwargs['event_id']
        event_object=get_object_or_404(Event,id=event_id)#checks whether event of given id exists
        #only highest 10 bids are retrieved for efficiency
        return Bid.objects.filter(event_id=event_id).order_by("-bid_price")[0:10]


    
#user has to pass event_id in url to view
class HighestBidRetrieveAPIView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,event_id,format=None): # 'event_id'is passed as extra arguement to get()-->check url
        
        event_id=self.kwargs['event_id']
        event_object=get_object_or_404(Event,id=event_id)#to check event exists
        print(event_object)
        #below query will return only one object if it exists
        try:

            highest_bid_object=Bid.objects.filter(event_id=event_id).order_by("-bid_price")[0:1].get()
            if request.user.is_staff:
                #admin can check details of user placing highest bid at the moment
                highest_bid_user=User.objects.get(id=highest_bid_object.user_id)
                user_serializer=UserSerializer(highest_bid_user)#serializing object 
                return Response({"user":user_serializer.data,"highest_bid":highest_bid_object.bid_price})
            else:
                return Response({"user":None,"highest_bid": highest_bid_object.bid_price})
        except ObjectDoesNotExist:
            return Response({"detail":"not bids received for this event"},status=status.HTTP_404_NOT_FOUND)
            
class BidCreateAPIView(generics.CreateAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=BidCreateSerializer

    def get_serializer_context(self):
        context=super().get_serializer_context()
        context.update({"event_id":self.kwargs['event_id']})
        return context
    
           

