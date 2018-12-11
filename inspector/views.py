# encoding:utf-8
from __future__ import unicode_literals
from django.shortcuts import render,HttpResponse
#from .sango.inspector import InspectorCaseConnecter
from django.utils.timezone import datetime
from helpers.director.kv import get_value
import json
from helpers.director.engine import BaseEngine
# Create your views here.
def inspector_case(request,code):
    # today = datetime.now().date()
    # today_str = unicode(today)    
    # case = InspectorCaseConnecter(today_str, today_str, code)
    value = get_value('inspector_case_%s' % code,'[]')
    ls = json.loads(value) or [['没有数据'],]
    case_list = ls
    baseengine = BaseEngine()
    baseengine.request = request
    ctx = {
        'case_list':case_list, 
        'js_config': baseengine.getJsConfig(),
    }


    return render(request,'inspector/case.html',context= ctx)