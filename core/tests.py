from django.test import TestCase
from django.contrib.auth.models import User


class UserTest(TestCase):

    def test_create_user(self):
        user = User.objects.create_user(username="testuser", password="123")
        self.assertEqual(user.username, "testuser")

    def test_user_password(self):
        user = User.objects.create_user(username="testuser", password="123")
        self.assertTrue(user.check_password("123"))

    def test_user_count(self):
        User.objects.create_user(username="u1", password="123")
        User.objects.create_user(username="u2", password="123")
        self.assertEqual(User.objects.count(), 2)

    def test_addition(self):
        self.assertEqual(1 + 1, 2)

    def test_uppercase(self):
        self.assertEqual("hello".upper(), "HELLO")