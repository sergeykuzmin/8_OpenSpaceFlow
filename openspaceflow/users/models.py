from django.contrib.auth.models import AbstractUser
from django.db import models


class Skill(models.Model):
    name = models.CharField("Name", max_length=128, blank=False)
    modified = models.DateTimeField(auto_now=True, null=True)
    created = models.DateTimeField(auto_created=True, null=True)

    def __str__(self):
        return self.name


class Member(AbstractUser):
    gender = models.CharField(
        "Gender", max_length=10, choices=[("Male", "Male"), ("Female", "Female")]
    )
    middle_name = models.CharField("Middle name", max_length=128, blank=True)
    info = models.TextField(blank=True, max_length=1024, verbose_name="Description")

    skill_level = models.ManyToManyField(Skill, through="MemberSkill")
    place = models.ForeignKey(
        "spaces.Space", on_delete=models.SET_NULL, blank=True, null=True
    )
    modified = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


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
