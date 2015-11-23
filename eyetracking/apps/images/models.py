from django.db import models
from uuid_upload_path import upload_to
from django_resized import ResizedImageField
import django_filters


class Image(models.Model):

    image = models.ImageField(upload_to=upload_to, height_field='height', width_field='width')
    resized_image = ResizedImageField(verbose_name="Photo", size=[150, 150], quality=90, upload_to=upload_to)
    original_name = models.CharField(verbose_name="Name", max_length=255, default='default')
    size = models.CharField(verbose_name="Size", max_length=30, default='')
    width = models.PositiveIntegerField(verbose_name="Resolution", default=0)
    height = models.PositiveIntegerField(default=0)

    @classmethod
    def human_size(cls, number_bytes):
        suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
        if number_bytes == 0:
            return '0 B'
        i = 0
        while number_bytes >= 1024 and i < len(suffixes) - 1:
            number_bytes /= 1024.
            i += 1
        f = ('%.2f' % number_bytes).rstrip('0').rstrip('.')
        return '%s %s' % (f, suffixes[i])


class ImageFilter(django_filters.FilterSet):

    class Meta:
        model = Image
        fields = ['original_name']