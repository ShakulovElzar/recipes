from django.contrib import messages
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q

from .models import Recipe, Comment
from .forms import CommentForm, RecipeForm

class Recipes(ListView):
    """Recipes view"""

    template_name = "recipes/recipes.html"
    model = Recipe
    context_object_name = "recipes"
    paginate_by = 6

    def get_queryset(self, *kwargs):
        query = self.request.GET.get("q")
        if query:
            recipes = self.model.objects.filter(
                Q(title__icontains=query) | 
                Q(description__icontains=query) |
                Q(instructions__icontains=query) |
                Q(cuisine_type__icontains=query) |
                Q(ingredients__icontains=query) | 
                Q(meal_type__icontains=query) 
            )
        else: 
            recipes = self.model.objects.all()
        return recipes 

class RecipeDetail(DetailView):
    """Recipe detail view"""

    template_name = "recipes/recipe_detail.html"
    model = Recipe
    context_object_name = "recipe"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.views += 1
        self.object.save()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = self.object.comments.all()
        context["comment_form"] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to post a comment.")
            return redirect("account_login")

        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.recipe = self.object
            comment.user = request.user
            comment.save()
            messages.success(request, "Your comment was added successfully.")
        else:
            messages.error(request, "There was a problem with your comment.")

        return redirect("recipe_detail", pk=self.object.pk)

class DeleteComment(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Delete a comment"""

    model = Comment

    def get_success_url(self):
        return reverse("recipe_detail", kwargs={"pk": self.object.recipe.pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.user or self.request.user.is_superuser

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
    
