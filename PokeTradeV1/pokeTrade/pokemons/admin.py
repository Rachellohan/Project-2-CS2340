from django.contrib import admin
from .models import Pokemon, Review
from django.utils.html import mark_safe

class PokeAdmin(admin.ModelAdmin):
    list_display = ('id', 'image_tag', 'price', 'name', 'types', 'abilities', 'stats', 'owner')  # Update list_display to use image_tag
    ordering = ['name']
    search_fields = ['name']
    list_filter = ('owner', 'price')


    def image_tag(self, obj):
        return mark_safe(f'<img src="{obj.image}" width="50px" height="50px" />')  # Display image as thumbnail
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

admin.site.register(Pokemon, PokeAdmin)
admin.site.register(Review)
