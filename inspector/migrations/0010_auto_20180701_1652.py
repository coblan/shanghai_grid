# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-01 16:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inspector', '0009_inspectorworkgroup'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inspectorworkgroup',
            name='work_time',
            field=models.CharField(blank=True, help_text='(8:00-12:00;13:30-17:30)<br>按照括号内的格式输入，以分号分割时间段', max_length=300, verbose_name='工作时间段'),
        ),
    ]
