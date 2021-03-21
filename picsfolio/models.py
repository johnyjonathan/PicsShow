from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserImage(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="piscfolio/images", default='default.jpg')
    user = models.ForeignKey(User, on_delete=models.CASCADE,default='1')
    description = models.TextField(blank=True, max_length='1000')

    def __str__(self):
        return self.name
