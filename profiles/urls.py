from django.urls import path
from .views import EditProfile, Profiles

urlpatterns = [
    path("user/<int:pk>/", Profiles.as_view(), name="profile"),
    path("edit/<int:pk>/", EditProfile.as_view(), name="edit_profile"),
]
