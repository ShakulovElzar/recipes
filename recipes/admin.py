from django.contrib import admin
from .models import Recipe

# Register your models here.

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'meal_type', 
                    'cuisine_type', 'calories', 
                    'posted_date', 'instructions', 
                    'ingredients', 'image')
    list_filter = ('meal_type',)