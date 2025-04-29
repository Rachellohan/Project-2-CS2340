from django.urls import path
from . import views

app_name = "friends_page"

urlpatterns = [
    path('', views.index, name='index'),
    path('add_friend/<int:id>/', views.add_friend, name='add_friend'),
]
