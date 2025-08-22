from rest_framework import serializers

from .models import Member, MemberSkill, Skill


class SkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["name"]


class MemberSkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberSkill
        fields = ["member_skills", "level"]


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "password",
            "employment_date",
            "gender",
            "info",
            "place",
        ]
