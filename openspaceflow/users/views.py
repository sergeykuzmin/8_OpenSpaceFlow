from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView

from .models import Member, MemberSkill


class HomeListView(ListView):
    model = Member
    template_name = "users/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_count"] = self.model.objects.count()
        context["object_list"] = (
            self.model.objects.prefetch_related("images")
            .prefetch_related("member_skills")
            .filter(is_active=True, is_superuser=False, is_staff=False)
            .order_by("-employment_date")
            .all()[:4]
        )

        return context


class MemberListView(ListView):
    model = Member
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = (
            queryset.filter(is_active=True, is_superuser=False, is_staff=False)
            .prefetch_related("images")
            .order_by("-employment_date")
        )

        return queryset


class MemberDetailView(LoginRequiredMixin, DetailView):
    model = Member
    context_object_name = "member"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["member"] = (
            self.model.objects.prefetch_related("images")
            .filter(
                id=self.kwargs["pk"], is_active=True, is_superuser=False, is_staff=False
            )
            .first()
        )

        return context
