from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


class BidAppUser(AbstractUser):
    pass


class Profile(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="profile",primary_key=True)
    bio=models.CharField(max_length=100,blank=True,null=True)
    contact_no_regex = RegexValidator(regex=r'^[1-9][0-9]{9}$', message="Phone no. must be of 10 digits starting from [1-9].")
    contact_no=models.CharField(validators=[contact_no_regex],unique=True,max_length=10)
    address=models.CharField(max_length=100)
    pincode_regex = RegexValidator(regex=r'^[1-9][0-9]{5}$', message="Pincode must be of six digits starting from [1-9].")
    pincode = models.CharField(validators=[pincode_regex], max_length=6)
    is_auctioneer=models.BooleanField(default=False)#only admin will set this value
    is_bidder=models.BooleanField(default=False)#only admin will set this value

    def __str__(self):
        return str(self.user)


class ProfileImageModel(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="profile_image",primary_key=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    image = models.FileField()

    def __str__(self):
        return str(self.user)
    


#ProfileImageModel object  should be created after user object creation
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile_image(sender, instance, created, **kwargs):
    if created:
        ProfileImageModel.objects.create(user=instance)
    instance.profile_image.save()
