from django.db import models

class GameType(models.Model):
   name = models.CharField(max_length=155)