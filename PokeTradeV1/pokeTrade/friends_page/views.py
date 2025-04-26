<<<<<<< HEAD
from django.shortcuts import render, redirect
from .models import Friend, User

def index(request):
    user = request.user
    if not request.user.is_authenticated:
        return redirect('accounts.login')
    all_players = User.objects.exclude(id=user.id)

    current_friends = Friend.objects.filter(user=user).values_list('friend_id', flat=True)

    template_data = {
        'title': 'Friends',
        'players': all_players,
        'friends': current_friends,
    }
=======
from django.shortcuts import render

def index(request):
    template_data = {}
    template_data['title'] = 'Friends'
>>>>>>> d5e5002 (pycache files)
    return render(request, 'friends_page/index.html', {'template_data': template_data})
