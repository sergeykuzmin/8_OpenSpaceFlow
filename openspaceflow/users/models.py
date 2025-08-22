from datetime import date, timedelta

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils import timezone


class Skill(models.Model):
    name = models.CharField("Name", max_length=128, blank=False)
    modified = models.DateTimeField(auto_now=True, null=True)
    created = models.DateTimeField(auto_created=True, null=True)

    def __str__(self):
        return self.name


class Member(AbstractUser):
    gender = models.CharField(
        "Gender",
        max_length=10,
        choices=[("Male", "Male"), ("Female", "Female")],
        default="Male",
    )
    middle_name = models.CharField("Middle name", max_length=128, blank=True)
    info = models.TextField(blank=True, max_length=1024, verbose_name="Description")

    skill_level = models.ManyToManyField(Skill, through="MemberSkill")
    place = models.OneToOneField(
        "spaces.Space",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        unique=True,
    )
    modified = models.DateTimeField(auto_now=True, null=True)
    employment_date = models.DateTimeField(
        auto_created=True, null=True, auto_now_add=True
    )

    @property
    def experience(self):
        time_difference = timezone.now() - (
            timezone.now() if self.employment_date is None else self.employment_date
        )
        return time_difference.days if time_difference.days >= 0 else 0

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    def clean(self):
        cleaned_data = super().clean()

        # if there is no place set
        if self.place is None:
            return cleaned_data

        # get current skills ordering by level to get best skill
        user = (
            MemberSkill.objects.select_related("skill")
            .filter(member_id=self.id)
            .order_by("-level")
            .first()
        )

        if not hasattr(user, "skill"):
            return cleaned_data

        find_skill = ["Testing"]

        # if current member has 'Testing' skill so needs to find 'Backend' or 'Frontend' otherwise - 'Testing'
        if user.skill.name == "Testing":
            find_skill = ["Backend", "Frontend"]
        elif user.skill.name == "Manager":
            find_skill = ["no_one"]

        place_left = int(self.place.number) - 1
        place_right = int(self.place.number) + 1

        members_count = (
            Member.objects.select_related("place")
            .filter(Q(place__number=place_left) | Q(place__number=place_right))
            .prefetch_related("skill_level")
            .filter(skill_level__name__in=find_skill)
            .count()
        )

        if members_count > 0:
            raise ValidationError(
                "It is forbidden to seat testers and programmers next to each other",
                "testers and programmers",
            )

        return cleaned_data

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class MemberSkill(models.Model):
    member = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name="member_skills"
    )
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    level = models.IntegerField(default=1, verbose_name="Skill level")
    created = models.DateTimeField(auto_created=True, null=True)

    def __str__(self):
        return f"{self.member} - {self.skill}: {self.level}"


class Image(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="images")
    url = models.ImageField("Url", upload_to="members/", blank=True)
    sort = models.IntegerField(default=1, verbose_name="Order", unique=True)
    modified = models.DateTimeField(auto_now=True, null=True)
    created = models.DateTimeField(null=True)
