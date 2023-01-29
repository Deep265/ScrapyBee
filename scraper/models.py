from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Links(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='links')
    file = models.FileField(upload_to='link_files/')



