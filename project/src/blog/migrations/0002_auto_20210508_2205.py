# Generated by Django 2.2.2 on 2021-05-08 16:35

import blog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='image',
            field=models.ImageField(default=None, upload_to=blog.models.upload_location),
        ),
    ]
