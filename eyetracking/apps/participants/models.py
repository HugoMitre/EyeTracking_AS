from django.core.urlresolvers import reverse
from django.db import models


class Participant(models.Model):
    first_name = models.CharField(verbose_name='Full Name', max_length=255)
    last_name = models.CharField(max_length=255)
    age = models.PositiveSmallIntegerField(verbose_name='Age', default=0)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(verbose_name='Gender', max_length=1, choices=GENDER_CHOICES)

    def __str__(self):
        return self.first_name

    def get_absolute_url(self):
        return reverse('participants:detail', args=[str(self.id)])
