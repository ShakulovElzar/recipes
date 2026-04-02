from django.db import models
from django.contrib.auth.models import User
from recipes.models import Recipe

# Create your models here.


class Meal(models.Model):
    """Meal model"""

    user = models.ForeignKey(User, related_name="meal_owner", on_delete=models.CASCADE)
    recipe = models.ForeignKey(
        Recipe, related_name="user_meal", on_delete=models.CASCADE
    )
    meal_type = models.CharField(max_length=50)
    meal_date = models.DateField()

    def __str__(self):
        return f"{self.user.username}'s {self.meal_type} meal for {self.meal_date}"
