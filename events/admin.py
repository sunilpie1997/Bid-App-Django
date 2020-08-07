from django.contrib import admin
from .models import Event,Product,Bid,ProductImageModel
# Register your models here.

admin.site.register(Event)
admin.site.register(Product)
admin.site.register(Bid)
admin.site.register(ProductImageModel)
