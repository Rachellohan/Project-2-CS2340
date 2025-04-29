import os
import django
from django.db.models import Count
from pokemons.models import Pokemon
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pokeTrade.settings')  
django.setup()

def delete_duplicate_pokemons():
    duplicates = Pokemon.objects.values('name').annotate(name_count=Count('id')).filter(name_count__gt=1)
    
    for duplicate in duplicates:
        duplicate_pokemons = Pokemon.objects.filter(name=duplicate['name'])

        pokemon_to_keep = None
        for pokemon in duplicate_pokemons:
            if pokemon.price < 20:
                pokemon_to_keep = pokemon
                break  
        if not pokemon_to_keep:
            pokemon_to_keep = duplicate_pokemons.first()

        for pokemon in duplicate_pokemons:
            if pokemon != pokemon_to_keep:
                print(f"Deleting duplicate: {pokemon.name} with ID {pokemon.id}")
                pokemon.delete()

    print("Duplicate cleanup done.")

delete_duplicate_pokemons()