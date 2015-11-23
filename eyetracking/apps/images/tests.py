from django.test import TestCase
from .models import Photo

#Third-party app imports
from model_mommy import mommy
from model_mommy.recipe import Recipe, foreign_key


class PhotoTests(TestCase):

    def setUp(self):
        """Se crean fotos de prueba"""
        Photo.objects.create(first_name="Roberto", last_name="Covarrubias", age="24", gender="Male")
        Participant.objects.create(first_name="Luis Salvador", last_name="Lopez Hernandez", age="27", gender="Male")
        Participant.objects.create(first_name="Maria Oyuki", last_name="Fuentes Uc", age="24", gender="Female")

    def test_human_size(self):

        photo = Photo()
        self.image = mommy.make(Photo)
        self.assertEqual(photo.human_size(1024), '1 KB')

