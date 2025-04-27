from django.contrib.auth.models import User
from django.db import models

class Pokemon(models.Model):
    name = models.CharField(max_length=100)
    image = models.URLField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pokemons', null=True, blank=True)
