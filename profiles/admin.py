from django.contrib import admin
from .models import Profile

# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    """Profile admin"""

    list_display = ("pk", "user", "bio", "image")


admin.site.register(Profile, ProfileAdmin)
