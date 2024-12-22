from django.shortcuts import render

from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy

from .models import Profile
from .forms import ProfileUpdateForm


class ProfileUpdateView(UpdateView):
    template_name = 'accounts/profile-form.html'
    model = Profile
    form_class = ProfileUpdateForm
    success_url = reverse_lazy('list-training')


