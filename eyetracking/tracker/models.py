from django.db import models

# Create your models here.
class Tracker(models.Model):
    ip = models.CharField(max_length=16)
    port = models.PositiveSmallIntegerField()
    frame_rate = models.PositiveSmallIntegerField()