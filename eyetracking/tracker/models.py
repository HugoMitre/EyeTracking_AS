from django.db import models


class Tracker(models.Model):
    ip = models.CharField(max_length=16)
    port = models.PositiveSmallIntegerField()


class TrackerData(models.Model):
    timestamp = models.CharField(max_length=200)
    time = models.IntegerField()
    fix = models.BooleanField()
    state = models.PositiveSmallIntegerField()
    raw_x = models.PositiveSmallIntegerField()
    raw_y = models.PositiveSmallIntegerField()
    avg_x = models.PositiveSmallIntegerField()
    avg_y = models.PositiveSmallIntegerField()
    pupil_size = models.FloatField()
    left_raw_x = models.PositiveSmallIntegerField()
    left_raw_y = models.PositiveSmallIntegerField()
    left_avg_x = models.PositiveSmallIntegerField()
    left_avg_y = models.PositiveSmallIntegerField()
    left_pupil_size = models.FloatField()
    left_pupil_x = models.PositiveSmallIntegerField()
    left_pupil_y = models.PositiveSmallIntegerField()
    right_raw_x = models.PositiveSmallIntegerField()
    right_raw_y = models.PositiveSmallIntegerField()
    right_avg_x = models.PositiveSmallIntegerField()
    right_avg_y = models.PositiveSmallIntegerField()
    right_pupil_size = models.FloatField()
    right_pupil_x = models.PositiveSmallIntegerField()
    right_pupil_y = models.PositiveSmallIntegerField()
