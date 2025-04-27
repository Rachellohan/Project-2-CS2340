import random
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, CustomErrorList
from pokemons.models import Pokemon

# Helper function to assign initial Pokémon
def assign_initial_pokemon(user):
    starter_pokemon = ['bulbasaur', 'charmander', 'squirtle']

    for name in starter_pokemon:
        response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{name}')
        if response.status_code == 200:
            data = response.json()
            Pokemon.objects.create(
                name=data['name'],
                image=data['sprites']['front_default'],
                owner=user,
                price=random.randint(1, 20)  # 🎯 Random price between 1 and 20
            )

@login_required
def logout(request):
    auth_logout(request)
    return redirect('home.index')

def login(request):
    template_data = {}
    template_data['title'] = 'Login'
    if request.method == 'GET':
        return render(request, 'accounts/login.html', {'template_data': template_data})
    elif request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            template_data['error'] = 'The username or password is incorrect.'
            return render(request, 'accounts/login.html', {'template_data': template_data})
        else:
            auth_login(request, user)
            return redirect('home.index')

def signup(request):
    template_data = {}
    template_data['title'] = 'Sign Up'

    if request.method == 'GET':
        template_data['form'] = CustomUserCreationForm()
        return render(request, 'accounts/signup.html', {'template_data': template_data})
    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST, error_class=CustomErrorList)
        if form.is_valid():
            user = form.save()
            assign_initial_pokemon(user)  # Assign starter Pokémon with random price
            return redirect('accounts.login')
        else:
            template_data['form'] = form
            return render(request, 'accounts/signup.html', {'template_data': template_data})

@login_required
def orders(request):
    template_data = {}
    template_data['title'] = 'Orders'
    template_data['orders'] = request.user.order_set.all()
    return render(request, 'accounts/orders.html', {'template_data': template_data})

@login_required
def profile(request):
    teams = ['Team Valor', 'Team Instinct', 'Team Mystic']
    random_team = random.choice(teams)
    user_pokemons = Pokemon.objects.filter(owner=request.user)

    return render(request, 'accounts/profile.html', {
        'template_data': {
            'user': request.user,
            'team': random_team,
            'total_pokemon': user_pokemons.count(),
            'pokemons': user_pokemons,
        }
    })

@login_required
def trade(request, pokemon_id):
    user_pokemon = get_object_or_404(Pokemon, id=pokemon_id, owner=request.user)
    available_pokemon = Pokemon.objects.filter(price=user_pokemon.price).exclude(owner=request.user)

    if request.method == 'POST':
        selected_pokemon_id = request.POST.get('selected_pokemon')
        selected_pokemon = get_object_or_404(Pokemon, id=selected_pokemon_id)
        selected_pokemon.owner = request.user
        selected_pokemon.save()
        user_pokemon.delete()
        return redirect('accounts.profile')

    return render(request, 'accounts/trade_pokemon.html', {
        'template_data': {
            'user_pokemon': user_pokemon,
            'available_pokemon': available_pokemon
        }
    })
