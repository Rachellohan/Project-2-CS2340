from django.urls import path
from . import views

app_name = "friends_page"

urlpatterns = [
    path('', views.index, name='index'),
]