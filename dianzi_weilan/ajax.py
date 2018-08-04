# encoding:utf-8

from __future__ import unicode_literals
from django.utils.timezone import datetime
from .models import OutBlockWarning
def get_global():
    return globals()

def get_warning_last_pk():
    warn = OutBlockWarning.objects.last()
    if warn:
        return warn.pk
    else:
        return -1