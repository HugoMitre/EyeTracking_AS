from django.core.urlresolvers import reverse
from django.db import models
from apps.images.models import Image


class AOI(models.Model):

    image = models.ForeignKey(Image)
    name = models.CharField(verbose_name="Name", max_length=255)
    top = models.PositiveSmallIntegerField()
    left = models.PositiveSmallIntegerField()
    height = models.PositiveSmallIntegerField()
    width = models.PositiveSmallIntegerField()
    TYPE_CHOICES = (
        ('rect', 'Rectangle'),
        ('ellipse', 'Ellipse'),
    )
    type = models.CharField(verbose_name='Gender', max_length=7, choices=TYPE_CHOICES)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('aoi:detail', args=[str(self.id)])
