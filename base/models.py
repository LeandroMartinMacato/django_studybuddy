from django.db import models
# from django.contrib.auth.models import User # base Django Model
from django.contrib.auth.models import AbstractUser

class  User(AbstractUser):
    name = models.CharField(max_length=200 , null=True)
    email = models.EmailField(null=True , unique=True)
    bio = models.TextField(null=True)

    avatar = models.ImageField(null=True , default="avatar.svg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Room(models.Model):
    host = models.ForeignKey(User , on_delete=models.SET_NULL , null=True)
    topic = models.ForeignKey(Topic , on_delete=models.SET_NULL , null=True) # When the topic is deleted room will remain
    name = models.CharField(max_length=200)
    description = models.TextField(null=True ,blank=True, max_length=200) # Null meaning it can be blank
    participants = models.ManyToManyField(User , related_name="participants" , blank=True)
    updated = models.DateTimeField(auto_now=True) #Automatic DateTimeField | Everytime we save
    created = models.DateTimeField(auto_now_add=True) #When we first save

    class Meta:
        ordering = ['-updated', '-created'] # if with "-" it will be reversed

    def __str__(self):
        return self.name

class Message(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE) # A message only has one user
    room = models.ForeignKey(Room , on_delete=models.CASCADE) # CASCADE Means if room is deleted the Message will also be deleted
    body = models.TextField(max_length=250)
    updated = models.DateTimeField(auto_now=True) #Automatic DateTimeField | Everytime we save
    created = models.DateTimeField(auto_now_add=True) #When we first save
    class Meta:
        ordering = ['-updated', '-created'] # if with "-" it will be reversed

    def __str__(self):
        return self.body[0:50]