import random
from pokemons.models import Pokemon

pokemons = Pokemon.objects.all()

for pokemon in pokemons:
    pokemon.price = random.randint(1, 20)
    pokemon.save()
    print(f"Assigned ${pokemon.price} to {pokemon.name}")

print("Done assigning prices!")

# To run: python assign_money.py

