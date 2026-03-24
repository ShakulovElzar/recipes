from django import forms
from djrichtextfield.widgets import RichTextWidget
from .models import Recipe

class RecipeForm(forms.ModelForm):
    ingredients = forms.CharField(widget=RichTextWidget())
    instructions = forms.CharField(widget=RichTextWidget())

    class Meta:
        model = Recipe
        fields = ['title', 'description', 'ingredients', 'instructions', 'image', 'image_alt', 'meal_type', 'cuisine_type', 'calories']

        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }

        labels = {
            'title': 'Recipe Title',
            'description': 'Description',
            'ingredients': 'Recipe Ingredients',
            'instructions': 'Recipe Instructions',
            'image': 'Recipe Image',
            'image_alt': 'Describe image',
            'meal_type': 'Meal Type',
            'cuisine_type': 'Cuisine Type',
            'calories': 'Calories',
        }