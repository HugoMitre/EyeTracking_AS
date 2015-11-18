from django.test import TestCase
from .models import Tracker
from django_faker import Faker

# Create your tests here.
class TrackerTests(TestCase):
    def test_instance_tracker(self):
        tracker = Tracker()

        populator = Faker.getPopulator()
        populator.addEntity(Game,5)
        populator.addEntity(Player,10)
        insertedPks = populator.execute()

        self.assertTrue(tracker)
        self.assertTrue(insertedPks)



