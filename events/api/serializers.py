from rest_framework import serializers
from events.models import Event,Product,Bid,ProductImageModel
from accounts.models import Profile
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


#serializer for product(retrieval and creation)
class ProductSerializer(serializers.ModelSerializer):
    
    name=serializers.CharField(required=True,max_length=50,min_length=3)
    category=serializers.CharField(required=True,max_length=50,min_length=3)
    description=serializers.CharField(required=True,max_length=100,min_length=3)
    
    class Meta:
    
        model=Product
        fields=['name','category','description']



#serializer for event product image
class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        
        model=ProductImageModel
        fields=['uploaded_at','image']



#serializer for Event(retrieval)
class EventSerializer(serializers.ModelSerializer):
    
    product=ProductSerializer()
    product_image=ProductImageSerializer()
    
    class Meta:
    
        model=Event
        fields=['id','date_added','start_date','deadline','base_price','product','product_image']
   


#serializer to create Event
#-----------Note:only those people with is_auctioneer(status)=True should be able to create--------------
class EventCreateSerializer(serializers.ModelSerializer):
    
    start_date=serializers.DateTimeField(required=True)#validations for start_date and end_date
    deadline=serializers.DateTimeField(required=True)
    base_price=serializers.IntegerField(required=True,min_value=1,max_value=10000000)
    date_added=serializers.DateTimeField(read_only=True)
    product=ProductSerializer()    
    
    class Meta:
    
        model=Event
        fields=['start_date','deadline','date_added','base_price','product']

    
    def create(self,validated_data):
    
        request = self.context.get('request', None)
        owner=request.user
        
        if owner is not None:#not required
        
            owner_profile=get_object_or_404(Profile,user_id=owner.id)
            
            if owner_profile.is_auctioneer==True:

                start_date=validated_data.get("start_date")
                deadline=validated_data.get("deadline")
                base_price=validated_data.get("base_price")
                product_data=validated_data.pop("product")

                event_product=Product(**product_data)
                event=Event.objects.create(product=event_product,start_date=start_date,deadline=deadline,base_price=base_price,owner=owner)
                event_product.save()
            
                return event
            
            else:
            
                raise serializers.ValidationError("you are not an auctioneer")
        
        else:
            
            raise serializers.ValidationError("authentication crediantials are not provided")




    #custom validation for start date
    def validate_start_date(self,value):
        
        if value<=timezone.now()+timedelta(days=1,minutes=30):
            
            raise serializers.ValidationError("start date should be atleast one day ahead of today(INDIAN TIMEZONE)")
        
        return value

    #custom validation for start date and deadline
    def validate(self,data):
        
        if data['deadline']<data['start_date']+timedelta(hours=1,minutes=30):
            
            raise serializers.ValidationError(" deadline should be at least 2 hour ahead")
        
        return data


#Bid serializer(for retrieval)
class BidSerializer(serializers.ModelSerializer):
    
    bid_price=serializers.IntegerField(required=True,min_value=1,max_value=100000000)
    date_added=serializers.DateTimeField(read_only=True)
    
    class Meta:
    
        model=Bid
        fields=['bid_price','date_added']
    
    

"""  
 Note:the auctioneer should not be ble to bid on his own product
"""
class BidCreateSerializer(serializers.ModelSerializer):
    
    bid_price=serializers.IntegerField(required=True,min_value=1,max_value=100000000)
    current_datetime=serializers.DateTimeField(required=True,write_only=True)
    #this field will not be stored in database,just for storing time when  bid was placed
    #to compare if bid are placed within startsate and deadline of event
    
    class Meta:
    
        model=Bid
        fields=['bid_price','current_datetime']
    
    
    def create(self,validated_data):
    
        request = self.context.get('request', None)
        user=request.user
        event_id=self.context.get("event_id")
    
        """
        use get_object_or_404 instead of get()
        """
    
        #to check if event exists
        event_object=get_object_or_404(Event,id=event_id)
        current_datetime=validated_data.get('current_datetime')
    
        if current_datetime>=event_object.start_date and current_datetime<=event_object.deadline:

            print(event_object.id)
            
            if event_object.owner_id==user.id :
            
                raise serializers.ValidationError("you cannot bid on item you are auctioning")
            
            else:
            
                bid_price=validated_data.get("bid_price")
                Bid_object=Bid.objects.create(event=event_object,user=user,bid_price=bid_price)
            
                return Bid_object
        
        else:
            
            raise serializers.ValidationError("you can only bid between start_date and deadline")

    









