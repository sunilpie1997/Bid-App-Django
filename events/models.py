from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator,MaxValueValidator
from django.core.exceptions import ValidationError
from datetime import datetime,timedelta
from django.utils import timezone



#function to validate end date

def validate_deadline(value):
    if value<=timezone.now()+timedelta(days=1,hours=1):
        raise ValidationError("deadline should be atleast one hour ahead of event start time")

#function to validate if start_date is greater than today's date by 1 day

def validate_start_date(value):
    if value<=timezone.now()+timedelta(days=1):
        raise ValidationError("start date should be atleast one day ahead of today")




class Event(models.Model):
    #function to add events by only those who are auctioneers
    #
    #
    owner=models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name="events")
    date_added=models.DateTimeField(auto_now_add=True,editable=False)
    start_date=models.DateTimeField(null=False,blank=False,validators=[validate_start_date])
    deadline=models.DateTimeField(null=False,blank=False,validators=[validate_deadline])
    base_price=models.IntegerField(null=False,blank=False,validators=[MinValueValidator(1,"minimum base price is 1"),MaxValueValidator(10000000,"maximum base price is 1 crore")])
    highest_bid_user=models.ForeignKey(get_user_model(),null=True,on_delete=models.CASCADE,blank=True)

    def __str__(self):
        return "owner:"+str(self.owner)+"   start date:"+self.start_date.strftime("%m/%d/%Y, %H:%M:%S")+"   base price:"+str(self.base_price)

    
#product model

class Product(models.Model):
    name=models.CharField(max_length=50,blank=False,null=False)
    category=models.CharField(max_length=50,blank=False,null=False)
    description= models.CharField(max_length=100,blank=False,null=False)
    event=models.OneToOneField(Event,on_delete=models.CASCADE,related_name="product",primary_key=True)
    image=models.ImageField(null=True,blank=True)

    def __str__(self):
        return "event:"+str(self.event)+"   product:"+self.name

#Bid model
class Bid(models.Model):

    
    user=models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name="bids")
    event=models.ForeignKey(Event,on_delete=models.CASCADE)
    bid_price=models.IntegerField(validators=[MinValueValidator(1,"minimum bid price is 1"),MaxValueValidator(100000000,"maximum bid_price is 10 crore")])
    #Bid model should have this field ...when bid was placed
    date_added=models.DateTimeField(auto_now_add=True,editable=False,null=True)
    def __str__(self):
        return str(self.user)+"   event:"+str(self.event)+"   bid:"+str(self.bid_price)

