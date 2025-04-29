from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.signup, name='accounts.signup'),
    path('login/', views.login, name='accounts.login'),
    path('logout/', views.logout, name='accounts.logout'),
    path('orders/', views.orders, name='accounts.orders'),
    path('profile/<int:user_id>/', views.other_profile, name='accounts.other_profile'),
    path('profile/', views.profile, name='accounts.profile'),
    path('trade/<int:pokemon_id>/', views.trade, name='accounts.trade'),
]