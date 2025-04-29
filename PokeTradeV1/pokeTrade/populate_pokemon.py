import requests
import random
from pokemons.models import Pokemon
from django.contrib.auth.models import User

default_owner = User.objects.get(id=1)

response = requests.get('https://pokeapi.co/api/v2/pokemon?limit=151')
data = response.json()
for item in data['results']:
    poke_response = requests.get(item['url'])
    poke_data = poke_response.json()

    name = poke_data['name']
    image_url = poke_data['sprites']['front_default']
    money_value = random.randint(1, 20)
    description = f"{name.capitalize()} is a Pokémon from the Kanto region."

    types = [t['type']['name'] for t in poke_data['types']]
    type_string = ', '.join(types)
    abilities = [a['ability']['name'] for a in poke_data['abilities']]
    ability_string = ', '.join(abilities)

    stats = [f"{s['stat']['name']}: {s['base_stat']}" for s in poke_data['stats']]
    stats_string = ', '.join(stats)
    moves = [m['move']['name'] for m in poke_data['moves'][:5]]
    move_string = ', '.join(moves)
    pokemon = Pokemon(
        name=name,
        price=money_value,
        image=image_url,
        description=description,
        owner=default_owner,
        types=type_string,
        abilities=ability_string,
        stats=stats_string,
        moves=move_string
    )
    pokemon.save()
    print(f"Saved {name}")
