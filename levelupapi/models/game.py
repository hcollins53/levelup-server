from django.db import models

class Game(models.Model):
   name = models.CharField(max_length=155)
   game_type = models.ForeignKey("GameType", on_delete=models.CASCADE)
   creator = models.ForeignKey("Gamer", on_delete=models.CASCADE)
   number_of_players = models.IntegerField(default=4)
   skill_level = models.CharField(max_length=20, default="beginner")