# Generated by Django 4.2.3 on 2024-06-08 00:40

import django.contrib.gis.db.models.fields
import django.contrib.gis.geos.point
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodtruck', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='foodtruck',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='foodtruck',
            name='longitude',
        ),
        migrations.RemoveField(
            model_name='foodtruck',
            name='x',
        ),
        migrations.RemoveField(
            model_name='foodtruck',
            name='y',
        ),
        migrations.AddField(
            model_name='foodtruck',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(default=django.contrib.gis.geos.point.Point(-122.4194, 37.7749), geography=True, srid=4326),
        ),
    ]