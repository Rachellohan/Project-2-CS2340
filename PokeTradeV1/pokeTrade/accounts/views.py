import random
import requests
from django.shortcuts import render
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from .forms import CustomUserCreationForm, CustomErrorList
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from pokemons.models import Pokemon

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
        user = authenticate(request, username = request.POST['username'], password = request.POST['password'])
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
            form.save()
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
    total_pokemon = Pokemon.objects.filter(owner=request.user).count()

    return render(request, 'accounts/profile.html', {
        'template_data': {
            'user': request.user,
            'team': random_team,
            'total_pokemon': total_pokemon  
        }
    })

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