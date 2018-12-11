# encoding:utf-8

from __future__ import unicode_literals
#from sango.inspector import InspectorCaseConnecter
from django.utils.timezone import datetime
from helpers.director.kv import get_value, set_value
import json
from django.conf import settings
import requests
from django.utils.timezone import datetime


proxies = getattr(settings,'DATA_PROXY',{})

def get_global():
    return globals()

def get_case_number(code):
    
    url = settings.SANGO_BRIDGE+'/rq'
    
    data={
        'fun':'keeper_case_count',
        'day': datetime.today().strftime('%Y-%m-%d'),
        'code': code,
    }
    rt = requests.post(url,data=json.dumps(data), proxies = proxies)
    case_list = json.loads( rt.text )
    normed_list = []
    for row in  case_list:
        dc = {}
        for k, v in row.items():
            dc[k.lower()] = v
        normed_list.append(dc)
      
    set_value('inspector_case_%s' % code, json.dumps(normed_list))
    #value = get_value('inspector_case_%s' % code,'[]')
    
    return len(normed_list)
    # today = datetime.now().date()
    # today_str = unicode(today)
    # case_query = InspectorCaseConnecter(today_str,today_str,code)
    # return case_query.get_number()

