from django.contrib import admin

from .models import Member, MemberSkill, Skill

# Register your models here.
# admin.site.register(Member)
admin.site.register(Skill)
admin.site.register(MemberSkill)


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
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
    # fields = ('username', 'skill_level_field')

    # filter_horizontal = ('skill_level',)
    raw_id_fields = ("skill_level",)
