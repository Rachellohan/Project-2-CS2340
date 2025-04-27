from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='pokemons.index'),
    path('<int:id>/', views.show, name='pokemons.show'),
    path('<int:id>/review/create/', views.create_review, name='pokemons.create_review'),
    path('<int:id>/review/<int:review_id>/edit/', views.edit_review, name='pokemons.edit_review'),
    path('<int:id>/review/<int:review_id>/delete/', views.delete_review, name='pokemons.delete_review'),
    path('browse/', views.index, name='store.browse'),
    path('fetch_pokemons/', views.fetch_pokemons, name='fetch_pokemons'),
]