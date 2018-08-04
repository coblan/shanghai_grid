# encoding:utf-8

from __future__ import unicode_literals
from sango.inspector import InspectorCaseConnecter
from django.utils.timezone import datetime
from helpers.director.kv import get_value
import json

def get_global():
    return globals()

def get_case_number(code):
    
    value = get_value('inspector_case','[]')
    ls = json.loads(value)
    case_list=[]
    for row in ls:
        if row[-3]==code:
            case_list.append(row)
    return len(case_list)
    # today = datetime.now().date()
    # today_str = unicode(today)
    # case_query = InspectorCaseConnecter(today_str,today_str,code)
    # return case_query.get_number()

