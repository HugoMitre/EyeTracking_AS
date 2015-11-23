from django.test import TestCase
from .models import Image


class PhotoTests(TestCase):

    def test_human_size(self):

        photo = Image()
        self.assertEqual(photo.human_size(1024), '1 KB')