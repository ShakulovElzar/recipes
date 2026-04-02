from django.db import models
from django.urls import reverse
from djrichtextfield.models import RichTextField

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django_resized import ResizedImageField


class Profile(models.Model):
    """Profile model"""

    user = models.ForeignKey(User, related_name="Profile", on_delete=models.CASCADE)
    image = ResizedImageField(
        size=[300, 300],
        quality=75,
        upload_to="profiles/",
        force_format="WEBP",
        blank=False,
    )
    bio = RichTextField(max_length=2500, blank=True, null=True)

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse("profile", kwargs={"pk": self.user.pk})


@receiver(post_save, sender=User)
def create_user_profile(instance, created, **kwargs):
    """Create or update the user profile"""
    if created:
        Profile.objects.create(user=instance)
