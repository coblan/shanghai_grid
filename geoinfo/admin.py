# encoding:utf-8

from __future__ import unicode_literals
from django.contrib import admin
from helpers.director.model_func.dictfy import to_dict
from helpers.director.shortcut import ModelTable,TablePage,page_dc,FieldsPage,ModelFields,model_dc,RowSort,RowFilter,RowSearch,has_permit
# Register your models here.
from .models import BlockPolygon
from django.contrib.gis.geos import Polygon
import json

class BlockPolygonTablePage(TablePage):
    class BlockPolygonTable(ModelTable):
        model=BlockPolygon
        exclude=[]
        
        def dict_row(self, inst):
           
            dc={
                'display':bool (inst.display),
                'bounding':bool ( inst.bounding)
            }
            return dc
        
    
    tableCls = BlockPolygonTable

class BlockPolygonFormPage(FieldsPage):
    class BlockPolygonForm(ModelFields):
        class Meta:
            model=BlockPolygon
            exclude=[]
        
        def __init__(self, dc={}, pk=None, crt_user=None, nolimit=False,*args,**kw):
            if 'display' in dc.keys():
                dc['display'] = self._adapt_polygon_dict(dc['display'])
            if 'bounding' in dc.keys():
                dc['bounding'] = self._adapt_polygon_dict(dc['bounding'])
            super(self.__class__,self).__init__(dc,pk,crt_user,nolimit)
        
        def _adapt_polygon_dict(self,polygon_str):
            if polygon_str:
                polygon_arr = json.loads(polygon_str)
                if polygon_arr[-1] != polygon_arr[0]:
                    polygon_arr.append(polygon_arr[0])
                return Polygon(polygon_arr)
            else:
                return None
                    
            # display= dc.get('display',None)
            # if display:
                # display= json.loads(display)
                # if display[-1] !=display[0]:
                    # display.append(display[0])
                # dc['display']= Polygon(display)            
            # return dc
        
        def get_row(self):
            display = self._adapt_polygon_obj(self.instance.display)
            bounding = self._adapt_polygon_obj(self.instance.bounding)
            dc={
                'display':display,
                'bounding':bounding
            }
            return to_dict(self.instance,filt_attr=dc)
        
        def _adapt_polygon_obj(self,polygon_obj):
            if polygon_obj:
                polygon_arr = list(polygon_obj.coords[0])
                polygon_arr.pop()
                return json.dumps(polygon_arr)
            else:
                return ''
        
        def dict_head(self, head):
            if head['name'] in ['display','bounding']:
                head['type']='polygon-input'
            
        

        
    fieldsCls = BlockPolygonForm
    template='geoinfo/blockpolygon_form.html'

model_dc[BlockPolygon]={'fields':BlockPolygonFormPage.BlockPolygonForm}

page_dc.update({
    'geoinfo.blockpolygon':BlockPolygonTablePage,
    'geoinfo.blockpolygon.edit':BlockPolygonFormPage,
})