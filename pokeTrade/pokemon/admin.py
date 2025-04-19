from django.contrib import admin
from .models import Pokemon, Review

class PokemonAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']

admin.site.register(Pokemon, PokemonAdmin)
admin.site.register(Review)