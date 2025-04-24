from django.contrib import admin
from .models import Pokemon, Review

class PokeAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']

admin.site.register(Pokemon, PokeAdmin)
admin.site.register(Review)