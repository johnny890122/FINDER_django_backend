from django.db import models
import uuid
from django.core.validators import MinValueValidator

class Network(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)

class Tool(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)

class Player(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    # age = models.IntegerField(validators=[MinValueValidator(0)], blank=True)

class Game(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    network = models.IntegerField()

class Round(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    round_number = models.IntegerField()
    class Meta:
        unique_together = (('game', 'round_number'),)

    tool = models.IntegerField()
    robustness = models.FloatField(validators=[MinValueValidator(0.0)], null=True)
    payoff = models.FloatField(validators=[MinValueValidator(0.0)], null=True)
    chosen_node = models.IntegerField(null=True)
    isEnd = models.BooleanField(default=False)
