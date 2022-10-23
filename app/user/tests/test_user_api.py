from unittest import TestCase
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import APIClient
from rest_framework import status

CREATW_USER_URL = reverse('user:create')


def creat_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        payload = {
            'email': 'test@user.com',
            'password': 'testuser123',
            'name': 'Test name'
        }
        res = self.client.post(CREATW_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        payload = {
            'email': 'test@user.com',
            'password': 'testuser123',
            'name': 'Test name'
        }
        creat_user(payload)
        res = self.client.post(CREATW_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_small_error(self):
        payload = {
            'email': 'test@user.com',
            'password': 'te',
            'name': 'Test name'
        }
        creat_user(payload)
        res = self.client.post(CREATW_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']).exists()
        self.assertFalse(user_exists)
