from django.contrib import admin
from .models import Profile,BidAppUser,ProfileImageModel
from django.contrib.auth.admin import UserAdmin


admin.site.register(BidAppUser, UserAdmin)
admin.site.register(Profile)
admin.site.register(ProfileImageModel)