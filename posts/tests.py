from django.contrib.auth.models import User
from django.core import mail
from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient

from posts.models import Post
from wall.settings import SEND_EMAIL


class PostViewTestCase(TestCase):
    def setUp(self):
        self.token = None
        self.post_list_url = reverse('post-list')
        self.obtain_token_url = reverse('obtain-token')

        self.client = APIClient()
        self.user = User.objects.create(username="test_user1")
        self.user.set_password('password')
        self.user.save()

    def login(self):
        data = {
            'username': 'test_user1',
            'password': 'password'
        }

        response = self.client.post(self.obtain_token_url, data=data)
        self.token = response.data['access']
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer {}'.format(self.token))

    def test_list_posts(self):
        response = self.client.get(self.post_list_url)

        self.assertEqual(response.status_code, 200)

        post_data = [{'title': 'test1', 'body': 'test1', 'user': self.user},
                     {'title': 'test2', 'body': 'test2', 'user': self.user}]
        
        for data in post_data:
            post = Post(**data)
            post.save()

        # not logged in
        response = self.client.get(self.post_list_url)
        payload = response.json()

        self.assertEqual(len(payload), 2)

        # now logged in
        self.login()

        response = self.client.get(self.post_list_url)
        payload = response.json()

        self.assertEqual(len(payload), 2)

    def test_create_posts(self):
        data = {
            'title': 'New post',
            'body': 'This post has words in it.',
            'user': self.user.pk
        }

        # not logged in
        response = self.client.post(self.post_list_url, data=data,
                                    format='json')

        self.assertEqual(response.status_code, 401)

        # logged in
        self.login()

        response = self.client.post(self.post_list_url, data=data,
                                    format='json')

        self.assertEqual(response.status_code, 201)


class UserTest(TestCase):
    def setUp(self):
        self.user_create_url = reverse('user-list')

    def test_user_creation(self):
        self.client = APIClient()

        data = {
            'email': 'fake@email.com',
            'username': 'test_user',
            'password': 'adlkjdlkjdldakjdlkajd'

        }

        response = self.client.post(self.user_create_url, data=data)

        self.assertEqual(response.status_code, 201)

        # if SEND_EMAIL is True we expect an email, otherwise we don't
        self.assertEqual(len(mail.outbox), int(SEND_EMAIL))
