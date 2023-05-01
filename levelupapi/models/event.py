from django.db import models
from django.db.models import Count

class Event(models.Model):
   name = models.CharField(max_length=155)
   organizer = models.ForeignKey("Gamer", on_delete=models.CASCADE, related_name='attendees')
   game = models.ForeignKey("Game", on_delete=models.CASCADE, related_name='events')
   description = models.CharField(max_length=200, default="Come Join us")
   date_and_time = models.CharField(max_length=200, default="Monday at 7pm")
   attendees = models.ManyToManyField("Gamer", related_name='organizer')

   @property
   def joined(self):
      return self.__joined

   @joined.setter
   def joined(self, value):
      self.__joined = value