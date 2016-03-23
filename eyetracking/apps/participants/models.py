from django.core.urlresolvers import reverse
from django.db import models
import numpy as np


class Participant(models.Model):
    first_name = models.CharField(verbose_name='Full Name', max_length=255)
    last_name = models.CharField(max_length=255)
    age = models.PositiveSmallIntegerField(verbose_name='Age', default=0)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(verbose_name='Gender', max_length=1, choices=GENDER_CHOICES)
    comments = models.TextField(blank=True)

    def __str__(self):
        return self.first_name

    def get_absolute_url(self):
        return reverse('participants:detail', args=[str(self.id)])

    def get_total(self):

        return Participant.objects.count()

    def count_gender(self, total):
        male = Participant.objects.filter(gender='M').count()
        female = total - male

        return  male, female

    def mean(self):
        participants_age = Participant.objects.values_list('age', flat=True)

        return np.mean(participants_age)

    def sd(self):
        participants_age = Participant.objects.values_list('age', flat=True)

        return np.std(participants_age)
