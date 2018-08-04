# encoding:utf-8
from __future__ import unicode_literals

from django.contrib import admin
from helpers.director.shortcut import page_dc
from .alg import polygon2circle
from .xuncha import XunCha
from  geoinfo.polygon import dict2poly
from . import admin_key_region_statistic
# Register your models here.
class Forcast(object):
    template='key_region/forcast.html'
    def __init__(self,*args,**kw):
        pass
    
    def get_label(self,prefer=None):
        return '巡查区域预测'
    
    def get_context(self):
        xun_sys = XunCha()
        poly_list = xun_sys.forcast()
        out = []
        for poly_dc in poly_list:
            poly_cods =poly_dc['polygon']
            poly = dict2poly(poly_cods)
            circle = polygon2circle(poly)
            circle['probability']=poly_dc['probability']
            out.append(circle)
        return {
            'circles':out
        }



page_dc.update({
    'key_region.forcast':Forcast,
})