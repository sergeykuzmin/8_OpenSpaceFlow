from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views.generic import DetailView, ListView
from rest_framework import permissions, viewsets
from rest_framework.pagination import PageNumberPagination

from .models import Member, MemberSkill
from .serializers import MemberSerializer


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


class MemberPagination(PageNumberPagination):
    page_size = 10
    page_query_param = "page"


class CustomLogic(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True

        # admin can everything
        if request.user.is_superuser:
            return True

        # staff can only change the place
        if request.user.is_staff and request.method is "PUT":
            return True

        return False


class MemberViewSet(viewsets.ModelViewSet):
    serializer_class = MemberSerializer
    pagination_class = MemberPagination
    queryset = (
        Member.objects.prefetch_related("member_skills")
        .filter(is_active=True, is_superuser=False, is_staff=False)
        .all()
    )
    permission_classes = [CustomLogic]

    def filter_queryset(self, queryset):
        skill = self.request.query_params.get("skill", None)

        if skill:
            # add filtration by skill name
            queryset = queryset.filter(member_skills__skill__name=skill)

        experience = self.request.query_params.get("experience", None)

        if experience:
            # calc experience days for now to compare this date with member.employment_date
            experience_date = timezone.now() - timedelta(days=int(experience))
            queryset = queryset.filter(employment_date__lte=experience_date)

        return super().filter_queryset(queryset)
