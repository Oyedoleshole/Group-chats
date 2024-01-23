from django.db import models

class Room(models.Model):
    name = models.CharField(max_length=200, blank=True)
    uid = models.CharField(max_length=200, null=True)
    room_name = models.CharField(max_length=255)

    def __str__(self):
        return self.room_name
    
class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    sender = models.CharField(max_length=250)
    message = models.TextField()
    thread_name = models.CharField(null=True,blank=True, max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True, null=True,blank=True)

    def __str__(self):
        return str(self.room)
    
class Video(models.Model):
    video = models.FileField()

    def __str__(self):
        return str(self.video)