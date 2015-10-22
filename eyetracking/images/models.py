from django.db import models
from uuid_upload_path import upload_to
from django_resized import ResizedImageField


class Image(models.Model):

    name = models.CharField(verbose_name="Name", max_length=200)
    resolution = models.CharField(verbose_name="Resolution", max_length=100)
    size = models.IntegerField(verbose_name="Size")


class Photo(models.Model):

    image = models.ImageField(upload_to=upload_to, height_field='height', width_field='width')
    resized_image = ResizedImageField(size=[500, 300], quality=90, upload_to=upload_to)
    original_name = models.CharField(max_length=255, default='default')
    size = models.CharField(max_length=30, default='')
    height=models.PositiveIntegerField(default=0)
    width=models.PositiveIntegerField(default=0)

    @classmethod
    def humansize(cls, number_bytes):
        suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
        if number_bytes == 0: return '0 B'
        i = 0
        while number_bytes >= 1024 and i < len(suffixes)-1:
            number_bytes /= 1024.
            i += 1
        f = ('%.2f' % number_bytes).rstrip('0').rstrip('.')
        return '%s %s' % (f, suffixes[i])
