from django.db import models
from django.contrib.auth.models import User
from djrichtextfield.models import RichTextField
from django_resized import ResizedImageField
from cloudinary_storage.storage import MediaCloudinaryStorage

# Create your models here.

MEAL_TYPES = (
    ("breakfast", "Breakfast"),
    ("lunch", "Lunch"),
    ("dinner", "Dinner"),
    ("snack", "Snack"),
    ("dessert", "Dessert"),
)

CUISINE_TYPES = (
    ("african", "African"),
    ("american", "American"),
    ("asian", "Asian"),
    ("european", "European"),
    ("latin_american", "Latin American"),
    ("middle_eastern", "Middle Eastern"),
    ("italian", "Italian"),
    ("french", "French"),
    ("indian", "Indian"),
    ("thai", "Thai"),
    ("japanese", "Japanese"),
    ("mediterranean", "Mediterranean"),
    ("other", "Other"),
)


class Recipe(models.Model):
    """ "
    Model to create and manage recipes
    """

    user = models.ForeignKey(
        User, related_name="recipe_owner", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=300, null=False, blank=False)
    description = models.CharField(max_length=500, null=False, blank=False)
    instructions = RichTextField(max_length=5000, null=False, blank=False)
    ingredients = RichTextField(max_length=5000, null=False, blank=False)
    image = ResizedImageField(
        size=[400, None],
        quality=75,
        upload_to="recipes/",
        force_format="WEBP",
        null=False,
        blank=False,
        storage=MediaCloudinaryStorage(),
    )
    image_alt = models.CharField(max_length=100, null=False, blank=False)
    meal_type = models.CharField(max_length=50, choices=MEAL_TYPES, default="breakfast")
    cuisine_type = models.CharField(
        max_length=50, choices=CUISINE_TYPES, default="other"
    )
    calories = models.IntegerField()
    views = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(User, related_name="liked_recipes", blank=True)
    posted_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-posted_date"]

    def __str__(self):
        return str(self.title)
