import random
import os
import django
from pokemons.models import Pokemon

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pokeTrade.settings')

django.setup()

pokemons = Pokemon.objects.all()

for pokemon in pokemons:
    if (pokemon.price > 20):
        pokemon.price = random.randint(1, 20)
        pokemon.save()
        print(f"Assigned ${pokemon.price} to {pokemon.name}")
print("Done assigning prices!")

