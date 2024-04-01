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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE)
    round_number = models.IntegerField(validators=[MinValueValidator(1)])
    round_payoff = models.FloatField(validators=[MinValueValidator(0.0)])
    chosen_node = models.IntegerField()
