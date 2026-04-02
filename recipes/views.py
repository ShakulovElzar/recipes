from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q

from .models import Recipe
from .forms import RecipeForm

class Recipes(ListView):
    """Recipes view"""

    template_name = "recipes/recipes.html"
    model = Recipe
    context_object_name = "recipes"

    def get_queryset(self, *kwargs):
        query = self.request.GET.get("q")
        if query:
            recipes = self.model.objects.filter(
                Q(title__icontains=query) | 
                Q(description__icontains=query) |
                Q(instructions__icontains=query) |
                Q(cuisine_type__icontains=query) 
            )
        else: 
            recipes = self.model.objects.all()
        return recipes 

class RecipeDetail(DetailView):
    """Recipe detail view"""

    template_name = "recipes/recipe_detail.html"
    model = Recipe
    context_object_name = "recipe"

    def get_object(self, queryset=None):
        recipe = super().get_object(queryset)
        recipe.views += 1
        recipe.save()
        return recipe


class AddRecipe(LoginRequiredMixin, CreateView):
    """Add recipe view"""

    template_name = "recipes/add_recipe.html"
    model = Recipe
    form_class = RecipeForm
    success_url = "/recipes/"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AddRecipe, self).form_valid(form)
    

class DeleteRecipe(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    """Delete a recipe"""

    model = Recipe
    success_url = "/recipes/"

    def test_func(self):
        return self.request.user == self.get_object().user
    

class EditRecipe(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Edit a recipe"""

    model = Recipe
    form_class = RecipeForm
    template_name = "recipes/edit_recipe.html"
    success_url = "/recipes/"

    def test_func(self):
        return self.request.user == self.get_object().user
    
class LikeRecipe(LoginRequiredMixin, UserPassesTestMixin, View):
    """Like or unlike a recipe"""

    def test_func(self):
        recipe = get_object_or_404(Recipe, pk=self.kwargs["pk"])
        return self.request.user != recipe.user

    def post(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, pk=self.kwargs["pk"])

        if recipe.likes.filter(id=request.user.id).exists():
            recipe.likes.remove(request.user)
        else:
            recipe.likes.add(request.user)

        return redirect("recipe_detail", pk=recipe.pk)