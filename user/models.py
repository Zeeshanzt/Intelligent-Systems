from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class profile(models.Model):
    staff = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    address = models.CharField( max_length=100)
    phone = models.CharField( max_length=50, null= True)
    image = models.ImageField(default= 'avatar.jfif', upload_to= 'Profile_Images')

    def __str__(self):
        return f'{self.staff.username}-Profile'
