from django.contrib import admin

from .models import Image, Member, MemberSkill, Skill

admin.site.register(Skill)
admin.site.register(MemberSkill)


class MemberSkillInline(admin.TabularInline):
    model = MemberSkill
    fields = ["skill", "level"]
    extra = 0


class ImageInline(admin.TabularInline):
    model = Image
    fields = ["url", "sort"]
    extra = 0


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    inlines = [MemberSkillInline, ImageInline]
    list_display = (
        "id",
        "username",
        "last_name",
        "first_name",
        "gender",
        "email",
        "is_active",
        "date_joined",
        "last_login",
    )
