from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import status
from PIL import Image
from rest_framework.parsers import FileUploadParser,MultiPartParser,FormParser
from rest_framework.permissions import IsAdminUser,IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.models import Profile,ProfileImageModel
from .serializers import UserByAdminSerializer,UserCreateSerializer,UserSerializer,ProfileImageSerializer
from .parsers import ImageUploadParser
User = get_user_model()#custom user model

   

class ProfileImageView(generics.RetrieveAPIView):
    queryset=ProfileImageModel.objects.all()
    serializer_class=ProfileImageSerializer
    permission_classes=[IsAuthenticated]
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset,user_id=self.request.user.id)
        return obj

      

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
    parser_classes=(MultiPartParser,FormParser)
    permission_classes=[IsAuthenticated]

    def post(self,request,filename,format=None):
        if 'file' not in request.data:
            return Response({"detail":"no image received"},status=status.HTTP_400_BAD_REQUEST)
        profileImage=request.data['file']

        if(profileImage.size>100000):
            return Response({"detail":"max file size supported is 100 kb"},status=status.HTTP_400_BAD_REQUEST)
        if(len(profileImage.name)>50):
            return Response({"detail":"file name too long. Max length is 50 chars"})
        """
        try:
            img=Image.open(profileImage)
            img.verify()
        except:
            return Response({"detail":"unsupported image format"},status=status.HTTP_400_BAD_REQUEST)

        """
        imageObject=get_object_or_404(ProfileImageModel,user_id=request.user.id)
        imageObject.image=profileImage
        imageObject.save(force_update=True)
        image_url = imageObject.image.url
        return Response({"image_url":image_url},status=status.HTTP_202_ACCEPTED)