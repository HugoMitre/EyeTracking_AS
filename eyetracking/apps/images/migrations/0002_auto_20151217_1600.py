# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_resized.forms
import uuid_upload_path.storage


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='resized_image',
            field=django_resized.forms.ResizedImageField(upload_to=uuid_upload_path.storage.upload_to, verbose_name=b'Image'),
        ),
    ]
