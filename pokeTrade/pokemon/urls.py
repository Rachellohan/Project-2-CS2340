from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='pokemon.index'),
    path('<int:id>/', views.show, name='pokemon.show'),
    path('<int:id>/review/create/', views.create_review, name='pokemon.create_review'),
    path('<int:id>/review/<int:review_id>/edit/', views.edit_review, name='pokemon.edit_review'),
    path('<int:id>/review/<int:review_id>/delete/', views.delete_review, name='pokemon.delete_review'),
]