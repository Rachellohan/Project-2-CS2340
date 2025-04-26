import os
import requests
import random
from pokemons.models import Pokemon
from django.contrib.auth.models import User

# Fetch the first 151 Pokémon
response = requests.get('https://pokeapi.co/api/v2/pokemon?limit=151')
data = response.json()

# Make sure you have a default owner (replace with real ID if needed)
DEFAULT_OWNER_ID = 1
default_owner = User.objects.get(id=DEFAULT_OWNER_ID)

for item in data['results']:
    poke_response = requests.get(item['url'])
    poke_data = poke_response.json()

    name = poke_data['name']
    image_url = poke_data['sprites']['front_default']
    money_value = random.randint(1, 20)
    description = f"{name.capitalize()} is a Pokémon from the Kanto region."

    # Download image and prepare it to be saved in the ImageField

    # Create the Pokémon object with the image
    pokemon = Pokemon(
        name=name,
        price=money_value,
        image = image_url,
        description=description,
        owner=default_owner
    )

    # Save the Pokémon object with the image
    pokemon.save()
    print(f"Saved {name} with ${money_value} and image")

print("Done saving all Pokémon!")
