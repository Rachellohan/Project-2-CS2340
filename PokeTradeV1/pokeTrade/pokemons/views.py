import requests
from django.shortcuts import render, redirect, get_object_or_404
from .models import Pokemon, Review
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Pokemon, Review
<<<<<<< HEAD
=======
from django.http import JsonResponse

>>>>>>> add_money_act


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
        pokemon = Pokemon.objects.get(pk=id)
    except Pokemon.DoesNotExist:
        # Try to fetch from PokeAPI
        url = f"https://pokeapi.co/api/v2/pokemon/{id}/"
        response = requests.get(url)

        if response.status_code != 200:
            return render(request, "404.html", status=404)

        data = response.json()

        # You need a default user to associate with the new Pokémon (e.g., user with ID 1)
        default_user = User.objects.first()

        pokemon = Pokemon.objects.create(
            id=id,
            name=data['name'].capitalize(),
            price=5.00,
            description="Imported from PokéAPI",
            image=data['sprites']['front_default'],
            owner=default_user  # or assign a fallback like request.user if logged in
        )

    reviews = Review.objects.filter(pokemon=pokemon)

    return render(request, "pokemons/show.html", {
        "template_data": {
            "pokemon": pokemon,
            "reviews": reviews
        }
    })