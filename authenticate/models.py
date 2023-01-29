from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
# Create your models here.
class Signup(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="users")
    image = models.ImageField(upload_to="profile_photos/",null=True)
    phone = models.CharField(max_length=215,blank=True)



