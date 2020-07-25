from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view 
from rest_framework import generics
from rest_framework import status
from PIL import Image
from rest_framework.parsers import FileUploadParser,MultiPartParser
from rest_framework.permissions import IsAdminUser,IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.models import Profile
from .serializers import UserByAdminSerializer,UserCreateSerializer,UserSerializer
from .parsers import ImageUploadParser
User = get_user_model()#custom user model

   
      

class UserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer
    permission_classes=[IsAuthenticated]
    def get_object(self):
        """
        Returns the object the view is displaying.

        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset,username=self.request.user.username)
        return obj
  


class UserCreateAPIView(generics.CreateAPIView):
    queryset=User.objects.all()
    serializer_class=UserCreateSerializer
    permission_classes=[AllowAny]

#only by admin
class UserByAdminAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset=User.objects.all()
    serializer_class=UserByAdminSerializer
    permission_classes=[AllowAny]
    lookup_field="username"

class ProfileImageUploadView(APIView):
    parser_class=(MultiPartParser,)
    permission_classes=[IsAuthenticated]

    def patch(self,request,filename,format=None):
        if 'file' not in request.data:
            return Response({"detail":"no image received"},status=status.HTTP_400_BAD_REQUEST)
        profileImage=request.data['file']
        print("first stage crossed")

        if(profileImage.size>1000000):
            return Response({"detail":"max file size supported is 1 mb"},status=status.HTTP_400_BAD_REQUEST)
        print("second stage crossed")
        if(len(profileImage.name)>30):
            return Response({"detail":"file name too long. Max length is 30 chars"})
        print("third stage crossed")   
        try:
            img=Image.open(profileImage)
            img.verify()
            print("fourth stage crossed")
        except:
            return Response({"detail":"unsupported image format"},status=status.HTTP_400_BAD_REQUEST)
            print("fourth stage crossed part 2")
        profile_object=get_object_or_404(Profile,user_id=request.user.id)#get profile
        profile_object.image.save(profileImage.name,profileImage,save=True)
        return Response(status=status.HTTP_202_ACCEPTED)


