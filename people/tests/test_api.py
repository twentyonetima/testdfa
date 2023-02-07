import io
import json
from unittest import mock

from PIL import Image
from django.contrib.auth.models import User
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from people.serializers import UserSerializer


class UserAPITestCase(APITestCase):
    def setUp(self):
        self.superuser1 = User.objects.create_superuser(username='superuser1', password='root1234', is_staff=True)
        self.superuser1.save()
        self.superuser2 = User.objects.create_superuser(username='superuser2', password='root1234', is_staff=True)
        self.superuser2.save()
        self.client = APIClient()
        self.client.force_authenticate(user=self.superuser1)
        self.client = APIClient()
        self.client.force_authenticate(user=self.superuser2)

    def test_get(self):
        url = reverse('user-list')
        response = self.client.get(url)
        serializer_data = UserSerializer([self.superuser1, self.superuser2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_get_not_superuser(self):
        self.user1 = User.objects.create_user(username='user1', password='qwer1234')
        self.user1.save()
        self.user2 = User.objects.create_user(username='user2', password='qwerasdf1234')
        self.user2.save()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user1)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user2)
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_create(self):
        self.assertEqual(2, User.objects.all().count())
        url = reverse('user-list')
        data = {
            'username': 'testuser1',
            'password': 'testpassword1',
            'email': 'testuser1@user.com'
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(3, User.objects.all().count())

    def test_update(self):
        url = reverse('user-detail', args=(self.superuser1.id,))
        data = {
            'username': self.superuser1.username,
            'email': self.superuser1.email,
            'first_name': 'First name 1',
            'last_name': 'Last name 1',
        }
        json_data = json.dumps(data)
        response = self.client.put(url, data=json_data,
                                   content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.superuser1.refresh_from_db()
        self.assertEqual('First name 1', self.superuser1.first_name)
        self.assertEqual('Last name 1', self.superuser1.last_name)


class CurrentUserAPITestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='test1', password='test1')
        self.user1.save()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user1)

    def test_get(self):
        url = reverse('current_user')
        response = self.client.get(url)
        serializer_data = UserSerializer(self.user1).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_update(self):
        url = reverse('current_user')

        data = {
            'username': self.user1.username,
            'email': self.user1.email,
            'first_name': 'First name 1',
            'last_name': 'Last name 1',
        }
        json_data = json.dumps(data)
        response = self.client.put(url, data=json_data,
                                   content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.user1.refresh_from_db()
        self.assertEqual('First name 1', self.user1.first_name)
        self.assertEqual('Last name 1', self.user1.last_name)

    def test_delete(self):
        self.assertEqual(1, User.objects.all().count())
        url = reverse('current_user')
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(0, User.objects.all().count())


class PhotoAPITestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='test1', password='test1')
        self.user1.save()

        file_mock = mock.MagicMock(File)
        file_mock.name = 'photo.jpg'

        image = io.BytesIO()
        Image.new('RGB', (1152, 2048)).save(image, 'JPEG')
        image.seek(0)
        image_file = SimpleUploadedFile('image.jpg', image.getvalue())

        self.photo = {
            'creator': self.user1.username,
            'name': 'test name',
            'description': 'test for Photo',
            'photos': image_file,

        }

    def test_get(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user1)
        url = reverse('photo')
        response = self.client.get(url, self.photo, format='multipart')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_invalid_get(self):
        url = reverse('photo')
        response = self.client.get(url, self.photo, format='multipart')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_post(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user1)
        url = reverse('photo')
        response = self.client.post(url, self.photo, format='multipart')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_invalid_post(self):
        url = reverse('photo')
        response = self.client.post(url, self.photo, format='multipart')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
