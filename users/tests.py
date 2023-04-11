from django.test import TestCase
from datetime import timedelta
from django.utils.timezone import now

from django.urls import reverse
from http import HTTPStatus

from users.models import User, EmailVerification


class UserRegistrationViewTestCase(TestCase):
    def setUp(self):
        self.path = reverse("users:registration")

        self.data = {
            "first_name": "Sergey",
            "last_name": "Demianenko",
            "username": "sergey",
            "email": "sdemianenko15@gmail.com",
            "password1": "qwerty_15@",
            "password2": "qwerty_15@",
        }

    def test_user_registration_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data["title"], "Store-Регистрация")
        self.assertTemplateUsed(response, "users/registration.html")

    def test_user_registration_succes(self):
        username = self.data["username"]
        self.assertFalse(User.objects.filter(username=username).exists())
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse("users:login"))
        self.assertTrue(User.objects.filter(username=username).exists())

        email_verification = EmailVerification.objects.filter(user__username=username)
        self.assertTrue(email_verification.exists())
        self.assertEqual(
            email_verification.first().expiration.date(),
            (now() + timedelta(hours=48)).date(),
        )

    def test_user_registration_error(self):
        user = User.objects.create(username=self.data["username"])
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(
            response, "Пользователь с таким именем уже существует.", html=True
        )
