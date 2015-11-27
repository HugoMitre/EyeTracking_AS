from django.test import TestCase
from .models import Image

#Third-party app imports
from model_mommy import mommy
from model_mommy.recipe import Recipe, foreign_key


class PhotoTests(TestCase):

    def test_human_size(self):


        photo = Image()
        self.assertEqual(photo.human_size(1024), '1 KB')
