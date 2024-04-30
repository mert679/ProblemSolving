from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import datetime


class User(AbstractUser):
    pass

class Room(models.Model):
    name = models.CharField(max_length=100)
    createdAt = models.DateTimeField(auto_now_add=True)
    img_question = models.ImageField(upload_to="questions", null=False, blank=False)
    users = models.ManyToManyField(User, related_name='rooms')

    def can_join(self):
        return self.users.count() <= 3
    
    def remaining_time(self):
        time_difference = timezone.now() - self.createdAt
        ten_minutes = datetime.timedelta(minutes=50)
        remaining = ten_minutes - time_difference
        return max(remaining, datetime.timedelta(0))




class MessageRoom(models.Model):  
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ('date_added',)

class DrawingData(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='drawing_data')
    coordinates = models.TextField() 

    created_at = models.DateTimeField(auto_now_add=True)

    