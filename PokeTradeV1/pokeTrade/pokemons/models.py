import random
from django.db import models
from django.contrib.auth.models import User

class Pokemon(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField(default=0)
    description = models.TextField()
    image = models.URLField()  
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default="5")

    def __str__(self):
        return str(self.id) + ' - ' + self.name
    
    def save(self, *args, **kwargs):
        if self.price == 0:
            self.price = random.randint(1, 20)
        super().save(*args, **kwargs)

class Review(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + ' - ' + self.pokemon.name
