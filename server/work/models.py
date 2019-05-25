from django.db import models

# Create your models here.
class Image(models.Model):
    user = models.CharField(max_length = 50)
    name = models.CharField(max_length = 50)
    pic = models.ImageField(upload_to = '')

    def __str__(self):
        return self.name

class Text(models.Model):
    user = models.CharField(max_length = 50)
    text = models.CharField(max_length = 50)
    
    def __str__(self):
        return self.text