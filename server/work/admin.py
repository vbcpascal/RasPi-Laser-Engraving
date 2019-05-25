from django.contrib import admin

# Register your models here.
from .models import Image, Text
admin.site.register(Image)
admin.site.register(Text)
