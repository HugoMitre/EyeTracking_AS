from django.db import models


class Image(models.Model):

    name = models.CharField(verbose_name="Name", max_length=200)
    resolution = models.CharField(verbose_name="Resolution", max_length=100)
    size = models.IntegerField(verbose_name="Size")
