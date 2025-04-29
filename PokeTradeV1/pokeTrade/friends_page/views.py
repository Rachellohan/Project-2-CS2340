from django.shortcuts import get_object_or_404, render, redirect
from .models import Friend, User

def index(request):
    user = request.user
    if not request.user.is_authenticated:
        return redirect('accounts.login')
    all_players = User.objects.exclude(id=user.id)
    friend_ids = Friend.objects.filter(user=user).values_list('friend_id', flat=True)
    current_friends = User.objects.filter(id__in=friend_ids)

    template_data = {
        'title': 'Friends',
        'players': all_players,
        'friends': current_friends,
    }
    return render(request, 'friends_page/index.html', {'template_data': template_data})

def add_friend(request, id):
     friend = get_object_or_404(User, id=id)
     user = request.user
 
     Friend.objects.create(
         user=user,
         friend=friend
     )
     
     return redirect('friends_page:index')
