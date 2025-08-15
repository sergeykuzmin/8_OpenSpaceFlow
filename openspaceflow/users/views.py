from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView

from .models import Member


class HomeListView(ListView):
    model = Member
    template_name = "users/home.html"


class MemberListView(ListView):
    model = Member


class MemberDetailView(LoginRequiredMixin, DetailView):
    model = Member
    context_object_name = "member"
