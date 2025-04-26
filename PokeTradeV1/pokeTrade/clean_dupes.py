import os
import django
from django.db.models import Count
from pokemons.models import Pokemon

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pokeTrade.settings')  # Replace 'pokeTrade' with your project name
django.setup()

# Function to delete duplicates, keeping the first one with price < 20
def delete_duplicate_pokemons():
    # Find all Pokemon with a duplicate name
    duplicates = Pokemon.objects.values('name').annotate(name_count=Count('id')).filter(name_count__gt=1)
    
    # Iterate over each name that has duplicates
    for duplicate in duplicates:
        # Find all pokemons with the same name
        duplicate_pokemons = Pokemon.objects.filter(name=duplicate['name'])

        # Find the first one with price < 20
        pokemon_to_keep = None
        for pokemon in duplicate_pokemons:
            if pokemon.price < 20:
                pokemon_to_keep = pokemon
                break  # Keep the first one with price < 20

        # If no pokemon with price < 20, keep the first one
        if not pokemon_to_keep:
            pokemon_to_keep = duplicate_pokemons.first()

        # Delete the other duplicates
        for pokemon in duplicate_pokemons:
            if pokemon != pokemon_to_keep:
                print(f"Deleting duplicate: {pokemon.name} with ID {pokemon.id}")
                pokemon.delete()

    print("Duplicate cleanup done.")

# Run the script
delete_duplicate_pokemons()