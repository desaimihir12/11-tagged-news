# Generated by Django 2.2.2 on 2021-05-09 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20210508_2206'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='form_url',
            field=models.URLField(blank=True, max_length=250),
        ),
    ]