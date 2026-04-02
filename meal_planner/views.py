import datetime, calendar, random
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django_reorder.reorder import reorder
from django.db.models import Q
from django.urls import reverse

from .models import Meal
from recipes.models import Recipe


# Create your views here.


class MealPlanner(LoginRequiredMixin, TemplateView):
    """Meal planner view"""

    template_name = "meal_planner/meal_planner.html"

    def get_context_data(self, **kwargs):
        today = datetime.date.today()
        date_in_month = calendar.monthrange(today.year, today.month)[1]

        days = [
            datetime.date(today.year, today.month, day)
            for day in range(1, date_in_month + 1)
        ]

        meals = (
            Meal.objects.filter(user=self.request.user, meal_date__in=days)
            .order_by(reorder(meal_type=["breakfast", "lunch", "dinner"]))
        )

        context = {
            "days": days,
            "meals": meals,
        }

        return context


class GetMeal(TemplateView):
    """Get random meal view"""

    template_name = "meal_planner/create_meal.html"

    def get_context_data(self, **kwargs):
        calories = self.request.GET.get("calories")
        query = self.request.GET.get("search")

        if query:
            calories = int(calories) if calories else 9999

            recipes = Recipe.objects.filter(
                (Q(description__icontains=query)
                 | Q(title__icontains=query)
                 | Q(ingredients__icontains=query)
                 | Q(cuisine_type__icontains=query)
                 | Q(instructions__icontains=query))
                & Q(calories__lte=calories)
                & Q(meal_type=kwargs["meal_type"])
            )
        elif calories:
            recipes = Recipe.objects.filter(
                Q(calories__lte=int(calories)) & Q(meal_type=kwargs["meal_type"])
            )
        else:
            recipes = Recipe.objects.filter(meal_type=kwargs["meal_type"])
            
        recipes_list = list(recipes)
        if recipes_list:
            recipe = random.choice(recipes_list)
            context = {
                "meal_date": kwargs["meal_date"],
                "meal_type": kwargs["meal_type"],
                "recipe": recipe,
            }
        else:
            context = {
                "meal_date": kwargs["meal_date"],
                "meal_type": kwargs["meal_type"],
            }

        return context
    

class AddMeal(View):
    def post(self, *args, **kwargs):
        pk = kwargs["pk"]
        recipe = Recipe.objects.get(pk=pk)
        meal_date = kwargs["meal_date"]
        meal_type = kwargs["meal_type"]

        meal, created = Meal.objects.update_or_create(
            meal_date=meal_date,
            meal_type=meal_type,
            defaults={
                "user": self.request.user,
                "recipe": recipe,
                "meal_date": meal_date,
            },
        )

        return HttpResponseRedirect(reverse("meal_planner"))