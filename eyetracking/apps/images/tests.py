from django.test import TestCase
from .models import Photo


class PhotoTests(TestCase):

    def test_human_size(self):

        photo = Photo()
        self.assertEqual(photo.human_size(1024), '1 KB')