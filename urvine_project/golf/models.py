from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    pass

class Reservation(models.Model):
    name = models.CharField(max_length=50)
    room = models.CharField(max_length=50)
    time = models.CharField(max_length=50)
    home = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

    