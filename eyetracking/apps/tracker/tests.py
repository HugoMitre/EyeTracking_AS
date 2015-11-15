from django.test import TestCase
from .models import Photo
import pytest

# Create your tests here.
class PhotoTests(TestCase):
    def test_human_size(self):
        photo = Photo()
        self.assertEqual(photo.human_size(1024), '1 KB')

@pytest.mark.django_db
def test_something(client):
        response = client.get('/')
        assert response.status_code == 200
