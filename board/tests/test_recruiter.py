import io

from PIL import Image
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
import pytest


@pytest.mark.django_db
class TestRecruiterCreate:
    @staticmethod
    def generate_photo_file():
        """Generating image file for testing"""
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file

    @staticmethod
    def creating_user():
        """Creating new user """
        user = get_user_model().objects.create(email='test25@abv.bg', first_name='testname', last_name='testlastname',
                                               password='')
        user.set_password('A239676a')
        user.save()
        return user

    def test_creating_user_and_returning_it_for_testing(self):
        user = self.creating_user()

        assert user.email == 'test25@abv.bg'

    def test_if_recruiter_is_create_should_return_201(self):
        """sending post request to create recruiter profile and should be created"""
        self.creating_user()
        client = APIClient()
        # Login to get access token
        response = client.post('/api/auth/jwt/create/', data={'email': 'test25@abv.bg', 'password': 'A239676a'}, )

        token = response.data.get("access")
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        photo_file = self.generate_photo_file()

        data = {
            "profile_pic": photo_file,
            "company": "sssssss",
            "position": "ssssssss",
            "phone_number": "+359893513462"
        }

        response = client.post('/api/recruiter/', data, format='multipart')

        assert response.status_code == status.HTTP_201_CREATED

        # Checking after creating recruiter profile if user is_recruiter should be True
        user = get_user_model().objects.get(email="test25@abv.bg")
        assert user.is_recruiter == True

    def test_user_with_no_profile_should_is_recruiter_to_be_false(self):
        user = self.creating_user()
        assert user.is_recruiter == False

    def test_get_all_recruiters_should_return_200(self):
        client = APIClient()
        response = client.get('/api/recruiter/')
        assert response.status_code == status.HTTP_200_OK

    def test_get_me_recruiter_should_return_200(self):
        self.creating_user()
        client = APIClient()
        response = client.post('/api/auth/jwt/create/', data={'email': 'test25@abv.bg', 'password': 'A239676a'}, )

        token = response.data.get("access")
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        photo_file = self.generate_photo_file()

        data = {
            "profile_pic": photo_file,
            "company": "sssssss",
            "position": "ssssssss",
            "phone_number": "+359893513462"
        }

        client.post('/api/recruiter/', data, format='multipart')

        response = client.get('/api/recruiter/me/')

        assert response.status_code == status.HTTP_200_OK


