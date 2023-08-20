from django.test import TestCase
from core.models import User


class UserCreate(TestCase):
    def test_create_user(self):
        User.objects.create_user(username="a",
                                 first_name="b",
                                 last_name="c",
                                 email="qwe@gmail.com",
                                 password="1234567qw"
                                 )

