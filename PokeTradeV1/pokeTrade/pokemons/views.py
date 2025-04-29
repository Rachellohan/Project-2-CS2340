import requests
from django.shortcuts import render, redirect, get_object_or_404
from .models import Pokemon, Review
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Pokemon, Review

from django.http import JsonResponse



def index(request):
    search_term = request.GET.get('search')
    if search_term:
        pokemons = Pokemon.objects.filter(name__icontains=search_term)
    else:
        pokemons = Pokemon.objects.all()

    template_data = {}
    template_data['title'] = 'Pokemons'
    template_data['pokemons'] = pokemons
    return render(request, 'pokemons/index.html', {'template_data': template_data})

def show(request, id):
    pokemon = Pokemon.objects.get(id=id)
    reviews = Review.objects.filter(pokemon=pokemon)

    template_data = {}
    template_data['title'] = pokemon.name
    template_data['pokemon'] = pokemon
    template_data['reviews'] = reviews
    return render(request, 'pokemons/show.html', {'template_data': template_data})

def fetch_pokemons(request):
    search_term = request.GET.get('search', '')  # Default to an empty string if no search term

    # Query Pokémon from the database
    pokemons = Pokemon.objects.all()  # Fetch all Pokémon
    if search_term:
        pokemons = pokemons.filter(name__icontains=search_term)  # Filter based on the search term

    # Prepare the data to send to the frontend
    pokemons_data = [
        {
            'id': pokemon.id,
            'name': pokemon.name,
            'image': pokemon.image,  
            'price': pokemon.price,
        }
        for pokemon in pokemons
    ]

    return JsonResponse({'results': pokemons_data})

@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment'] != '':
        pokemon = Pokemon.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment']
        review.pokemon = pokemon
        review.user = request.user
        review.save()
        return redirect('pokemons.show', id=id)
    else:
        return redirect('pokemons.show', id=id)

@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('pokemons.show', id=id)

    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'pokemons/edit_review.html', {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.save()
        return redirect('pokemons.show', id=id)
    else:
        return redirect('pokemons.show', id=id)

@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    review.delete()
    return redirect('pokemons.show', id=id)


def show(request, id):
    try:
        # Try to get the Pokemon from the database
        pokemon = Pokemon.objects.get(pk=id)
    except Pokemon.DoesNotExist:
        # If the Pokémon is not found in the DB, fetch it from PokéAPI
        url = f"https://pokeapi.co/api/v2/pokemon/{id}/"
        response = requests.get(url)

        if response.status_code != 200:
            return render(request, "404.html", status=404)

        data = response.json()

        # Extract types
        types = [t['type']['name'] for t in data['types']]
        type_string = ', '.join(types)

        # Extract abilities
        abilities = [a['ability']['name'] for a in data['abilities']]
        ability_string = ', '.join(abilities)

        # Extract stats
        stats = {s['stat']['name']: s['base_stat'] for s in data['stats']}
        stats_string = str(stats)  # Convert the stats dictionary to a string (or JSON if preferred)

        # Extract moves (just first 5 for brevity)
        moves = [m['move']['name'] for m in data['moves'][:5]]
        move_string = ', '.join(moves)

        # Get the default owner
        default_user = User.objects.first()

        # Create new Pokémon entry in the database
        pokemon = Pokemon.objects.create(
            id=id,
            name=data['name'].capitalize(),
            price=5.00,
            description="Imported from PokéAPI",
            image=data['sprites']['front_default'],
            owner=default_user,
            types=type_string,
            abilities=ability_string,
            stats=stats_string,  # Save stats as a string
            moves=move_string
        )

    # Get the reviews associated with this Pokémon
    reviews = Review.objects.filter(pokemon=pokemon)

    return render(request, "pokemons/show.html", {
        "template_data": {
            "pokemon": pokemon,
            "reviews": reviews
        }
    })


def pokemon_list(request):
    sort_by = request.GET.get('sort_by', 'name')  # Default sort by name

    # Define possible fields to sort by
    if sort_by == 'price':
        pokemons = Pokemon.objects.all().order_by('price')
    elif sort_by == 'stats':
        # Assuming stats is a JSON field or you have a specific way to store stats for sorting
        # If stats are stored as JSON, you might need to sort based on a specific key in the stats (e.g., 'attack')
        pokemons = Pokemon.objects.all().order_by('stats')  # This is just an example, adjust according to your model
    else:
        pokemons = Pokemon.objects.all()

    return render(request, 'pokemon_list.html', {'pokemons': pokemons, 'sort_by': sort_by})