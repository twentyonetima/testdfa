from django.contrib.auth.models import User
from django.test import TestCase

from people.serializers import UserSerializer


class UserSerializerTestCase(TestCase):
    def test_user_serializer(self):
        user1 = User.objects.create_user(username='user1', first_name='Name 1',
                                         last_name='Last name 1', email='user1@user.com')
        user2 = User.objects.create_user(username='user2', first_name='Name 2',
                                         last_name='Last name 2', email='user2@user.com')
        data = UserSerializer([user1, user2], many=True).data
        expected_data = [
            {
                'username': 'user1',
                'first_name': 'Name 1',
                'last_name': 'Last name 1',
                'email': 'user1@user.com',
            },
            {
                'username': 'user2',
                'first_name': 'Name 2',
                'last_name': 'Last name 2',
                'email': 'user2@user.com',
            },
        ]
        self.assertEqual(expected_data, data)
