from django.test import Client, TestCase

from ..models import Member


class TestRoutes(TestCase):
    def test_home_page(self):
        url = ""
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_members_page(self):
        url = "/members/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_member_page_redirect(self):
        url = "/member/1/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
