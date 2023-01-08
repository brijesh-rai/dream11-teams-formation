from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=50)
    team_code = models.CharField(max_length=10,primary_key=True)
    
    def __str__(self):
        return self.team_code
    
class Position(models.Model):
    pos = models.CharField(max_length=10,primary_key=True)
    
    def __str__(self):
        return self.pos

class Player(models.Model):
    name = models.CharField(max_length=100)
    is_playing = models.BooleanField(default=False)
    credit = models.FloatField()
    pos = models.ForeignKey(Position, on_delete=models.CASCADE)
    team_code = models.ForeignKey(Team, on_delete=models.CASCADE,)
    cap = models.BooleanField(default=True)
    v_cap = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name