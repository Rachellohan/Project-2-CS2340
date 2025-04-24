from django.shortcuts import render, redirect, get_object_or_404
from .models import Pokemon, Review
from django.contrib.auth.decorators import login_required

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