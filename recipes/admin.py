from django.contrib import admin
from .models import Recipe, Comment

# Register your models here.


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "user",
        "meal_type",
        "cuisine_type",
        "calories",
        "posted_date",
        "instructions",
        "ingredients",
        "image",
    )
    list_filter = ("meal_type",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user', 'created_on')
    search_fields = ('recipe__title', 'user__username', 'body')
    list_filter = ('created_on',)
