from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Profile
from .forms import ProfileForm


class Profiles(TemplateView):
    """Profiles view"""

    template_name = "profiles/profile.html"

    def get_context_data(self, **kwargs):
        profile = Profile.objects.get(user=self.kwargs["pk"])
        context = {
            "profile": profile,
            "form": ProfileForm(instance=profile),
        }


        return context


class EditProfile(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Edit profile view"""

    form_class = ProfileForm
    model = Profile

    def get_success_url(self):
        return self.object.get_absolute_url()

    def test_func(self):
        return self.request.user == self.get_object().user
