# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-12-11 07:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inspector', '0003_auto_20171211_1550'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inspectorgrop',
            old_name='insp',
            new_name='inspector',
        ),
    ]
