from datetime import datetime

from django.core.exceptions import ValidationError
from django.test import Client, TestCase
from django.utils import timezone
from spaces.models import Space

from ..models import Member, MemberSkill, Skill


def setUpModule():
    # create members
    Member.objects.create(
        username="testuser1",
        email="test1@example.com",
        password="password",
        gender="Male",
        employment_date=timezone.make_aware(datetime(2025, 8, 1, 8, 8, 8)),
        is_active=True,
    )
    Member.objects.create(
        username="testuser2",
        email="test2@example.com",
        password="password",
        gender="Male",
        employment_date=timezone.make_aware(datetime(2025, 8, 2, 8, 8, 8)),
        is_active=False,
    )
    Member.objects.create(
        username="testuser3",
        email="test3@example.com",
        password="password",
        gender="Male",
        employment_date=timezone.make_aware(datetime(2025, 8, 3, 8, 8, 8)),
        is_active=True,
        is_staff=True,
    )
    Member.objects.create(
        username="testuser4",
        email="test4@example.com",
        password="password",
        gender="Male",
        employment_date=timezone.make_aware(datetime(2025, 8, 4, 8, 8, 8)),
        is_active=True,
        is_staff=False,
    )

    # create desks
    Space.objects.create(number=1)
    Space.objects.create(number=2)
    Space.objects.create(number=3)
    Space.objects.create(number=4)
    Space.objects.create(number=5)

    # register skills
    Skill.objects.create(name="Frontend")
    Skill.objects.create(name="Backend")
    Skill.objects.create(name="Testing")
    Skill.objects.create(name="Manager")

    # set skills to users
    MemberSkill.objects.create(level=5, member_id=1, skill_id=1)
    MemberSkill.objects.create(level=3, member_id=2, skill_id=2)
    MemberSkill.objects.create(level=6, member_id=3, skill_id=3)
    MemberSkill.objects.create(level=2, member_id=4, skill_id=4)


class TestRoutes(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = Member.objects.create(
            username="testuser",
            email="test@example.com",
            password="password",
            gender="Male",
            employment_date=timezone.make_aware(datetime(2025, 8, 8, 8, 8, 8)),
        )
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.user)

        MemberSkill.objects.create(level=8, member_id=5, skill_id=1)

    @classmethod
    def tearDownClass(cls):
        Member.objects.all().delete()
        MemberSkill.objects.all().delete()
        Skill.objects.all().delete()
        Space.objects.all().delete()

    def test_member_page_auth(self):
        url = "/member/1/"
        response = self.auth_client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_member_page_context_positive(self):
        url = "/member/1/"
        response = self.auth_client.get(url)
        expected_object = Member.objects.get(id=1)
        self.assertEqual(expected_object, response.context["member"])

    def test_member_page_context_negative(self):
        url = "/member/1/"
        response = self.auth_client.get(url)
        expected_object = Member.objects.get(id=2)
        self.assertNotEqual(expected_object, response.context["member"])

    def test_homepage_context_positive(self):
        url = ""
        response = self.client.get(url)
        expected_object = Member.objects.get(id=1)
        self.assertIn(expected_object, response.context["object_list"])
        self.assertEqual(5, response.context["object_count"])

    def test_homepage_context_negative(self):
        url = ""
        response = self.client.get(url)
        unexpected_objects = Member.objects.filter(id__in=[2, 3])
        for obj in unexpected_objects:
            self.assertNotIn(obj, response.context["object_list"])

    def test_members_context_positive(self):
        url = "/members/"
        response = self.client.get(url)
        expected_object = Member.objects.get(id=1)
        self.assertIn(expected_object, response.context["object_list"])

    def test_members_context_negative(self):
        url = "/members/"
        response = self.client.get(url)
        unexpected_objects = Member.objects.filter(id__in=[2, 3])
        for obj in unexpected_objects:
            self.assertNotIn(obj, response.context["object_list"])

    def test_members_validation_positive(self):
        # try to seat members
        try:
            user1 = Member.objects.get(id=1)
            user1.place_id = 1
            user1.save()

            user1 = Member.objects.get(id=2)
            user1.place_id = 2
            user1.save()

            user1 = Member.objects.get(id=3)
            user1.place_id = 5
            user1.save()

            user1 = Member.objects.get(id=4)
            user1.place_id = 4
            user1.save()

            user1 = Member.objects.get(id=5)
            user1.place_id = 3
            user1.save()

        except ValidationError as e:
            self.assertEqual(True, False)

    def test_members_validation_negative(self):
        with self.assertRaises(ValidationError) as err:
            # try to seat members incorrectly
            user1 = Member.objects.get(id=1)
            user1.place_id = 1
            user1.save()

            user1 = Member.objects.get(id=2)
            user1.place_id = 2
            user1.save()

            user1 = Member.objects.get(id=3)
            user1.place_id = 3
            user1.save()

            user1 = Member.objects.get(id=4)
            user1.place_id = 4
            user1.save()

            user1 = Member.objects.get(id=5)
            user1.place_id = 5
            user1.save()

        self.assertIn(
            "It is forbidden to seat testers and programmers next to each other",
            err.exception.message_dict["__all__"],
        )
