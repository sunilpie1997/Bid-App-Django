from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from accounts.models import Profile
from django.contrib.auth import get_user_model
    
User = get_user_model()#custom user model

def validate_contact_no(user,contact_no):#user will be 'None' when creating user and will be an instance of 'User' while upadting user
    if(isinstance(user,User)):
        print("come here, i will catch you")
        value_count=Profile.objects.exclude(contact_no=user.profile.contact_no).count()
        if(value_count>0):#excluding current instance's contact_no for uniqueness(see limitation of updating nested serializers)
            #count() is more efficient than len()
            return False
        return True
    else:
        value_count=Profile.objects.filter(contact_no=contact_no).count()
        if(value_count>0):
            return False
        else:
            return True


#profile serializer(for retrieval and creation and full updation)-->by user
class ProfileSerializer(serializers.ModelSerializer):
    
    image=serializers.ImageField(read_only=True)
    contact_no =serializers.RegexField("^[1-9][0-9]{9}$",required=True)
    address = serializers.CharField(max_length=100,min_length=10,required=True)
    pincode = serializers.RegexField("^[1-9][0-9]{5}$",required=True)
    bio=serializers.CharField(max_length=100,allow_null=True)#request should contain "bio":null if user is not interested in adding 'bio'
    is_auctioneer=serializers.BooleanField(read_only=True)#django will 'REJECT' if provided in request
    is_bidder=serializers.BooleanField(read_only=True)
    class Meta:
        model=Profile
        fields=['contact_no','address','pincode','is_auctioneer','bio','image','is_bidder']


# user serializer (for retrieval and Full updation by individual user)except password
class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,max_length=50,validators=[UniqueValidator(queryset=User.objects.all(),message="Account with this email already exists")])
    username = serializers.CharField(required=True,max_length=30,validators=[UniqueValidator(queryset=User.objects.all(),message="This username is already taken")])
    first_name = serializers.CharField(min_length=3,required=True,max_length=30)
    last_name = serializers.CharField(min_length=3,required=True,max_length=30)
    profile=ProfileSerializer()
    class Meta:
        model=User
        fields=['username','email','first_name','last_name','profile']

    def update(self,instance,validated_data):
        instance.email=validated_data.get("email")
        instance.username=validated_data.get("username")
        instance.first_name=validated_data.get("first_name")
        instance.last_name=validated_data.get("last_name")
        profile_data=validated_data.pop("profile")
        instance.profile.contact_no=profile_data.get("contact_no")
        if(not validate_contact_no(instance,None)):
            raise serializers.ValidationError("account with this contact no. exists")

        instance.profile.address=profile_data.get("address")
        instance.profile.pincode=profile_data.get("pincode")
        instance.profile.bio=profile_data.get("bio")
        instance.profile.save(force_update=True)#to make sure it is not created:))
        instance.save(force_update=True)
        return instance


    


#user serializer (for creation)
#--->profile is also created along.
class UserCreateSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(required=True,max_length=50,validators=[UniqueValidator(queryset=User.objects.all(),message="Account with this email already exists")])
    username = serializers.CharField(required=True,max_length=30,validators=[UniqueValidator(queryset=User.objects.all(),message="This username is already taken")])
    password = serializers.CharField(min_length=8,write_only=True,required=True,max_length=30)
    first_name = serializers.CharField(min_length=3,required=True,max_length=30)
    last_name = serializers.CharField(min_length=3,required=True,max_length=30)
    profile=ProfileSerializer()#for creation
    class Meta:
        model=User
        fields=['username','email','first_name','last_name','password','profile']
    
    def create(self,validated_data):
        email=validated_data["email"]
        username=validated_data["username"]
        first_name=validated_data["first_name"]
        last_name=validated_data["last_name"]
        password=validated_data["password"]
        profile_data=validated_data.pop("profile")

        if(not validate_contact_no(None,profile_data["contact_no"])):
            raise serializers.ValidationError("account with this contact no. exists")

        user_profile=Profile(**profile_data)
        #user is created and saved
        user=User.objects.create_user(profile=user_profile,email=email,username=username,first_name=first_name,last_name=last_name,password=password)
        #after user is created and saved,profile is also saved in database 
        user_profile.save()
        return user


#for full profile update by admin
class ProfileUpdateSerializer(serializers.ModelSerializer):
    image=serializers.ImageField(read_only=True)
    contact_no =serializers.RegexField("^[1-9][0-9]{9}$",required=True)
    #,validators=[UniqueValidator(queryset=Profile.objects.all(),message="Account with this contact no exists")]
    #limitation of validators in django rest framework
    address = serializers.CharField(max_length=100,min_length=10,required=True)
    pincode = serializers.RegexField("^[1-9][0-9]{5}$",required=True)
    bio=serializers.CharField(max_length=100,allow_null=True)
    is_auctioneer=serializers.BooleanField()
    is_bidder=serializers.BooleanField()
    class Meta:
        model=Profile
        fields=['contact_no','address','pincode','is_auctioneer','bio','image','is_bidder']
    
    def validate_contact_no(self,value):
        value_count=Profile.objects.filter(contact_no=value).count()
        if(value_count>1):#1 will indiacate only one occurence of given contact_no
        #count() is more efficient than len()
            raise serializers.ValidationError("account with this contact no. exists")
        return value

#for retrieve ,update and delete by admin only
class UserByAdminSerializer(serializers.ModelSerializer):
    
#username is read only because we are using username to search the user,so option of updating username should not be there
    email = serializers.EmailField(required=True,max_length=50,validators=[UniqueValidator(queryset=User.objects.all(),message="Account with this email already exists")])
    username = serializers.CharField(read_only=True,max_length=30,validators=[UniqueValidator(queryset=User.objects.all(),message="This username is already taken")])
    first_name = serializers.CharField(required=True,min_length=3,max_length=30)
    last_name = serializers.CharField(required=True,min_length=3,max_length=30)
    profile=ProfileUpdateSerializer()
    class Meta:
        model=User
        fields=['username','email','first_name','last_name','profile']

    def update(self,instance,validated_data):
        instance.email=validated_data.get("email")
        instance.first_name=validated_data.get("first_name")
        instance.last_name=validated_data.get("last_name")
        profile_data=validated_data.pop("profile")
        instance.profile.contact_no=profile_data.get("contact_no")
        instance.profile.address=profile_data.get("address")
        instance.profile.pincode=profile_data.get("pincode")
        instance.profile.is_auctioneer=profile_data.get("is_auctioneer")
        instance.profile.is_bidder=profile_data.get("is_bidder")
        instance.profile.bio=profile_data.get("bio")
        print("hello"+profile_data.get("address"))
        #instance.profile.save(force_update=True)
        instance.profile.save(force_update=True)#to make sure it is not created:))
        instance.save(force_update=True)
        return instance