# encoding:utf-8
from __future__ import unicode_literals
from django.contrib import admin
from helpers.director.shortcut import page_dc,TablePage,FieldsPage,ModelTable,ModelFields,model_dc,\
     RowSort,model_to_name,director
from .models import DuchaCase,JianduCase
from django.contrib.gis.measure import D
from helpers.director.model_func.dictfy import to_dict
import json
from helpers.maintenance.update_static_timestamp import js_stamp

# Register your models here.
class CaseCmpPage(TablePage):
    """
    ���ݿⰴ�վ�������
    https://stackoverflow.com/questions/19703975/django-sort-by-distance
    """
    template='jb_admin/table.html'
    def get_label(self):
        return '案件比对辅助'
    
    def get_context(self):
        ctx = TablePage.get_context(self) 
        ctx['extra_js'] = ['/static/js/casecmp.pack.js?t=%s'%js_stamp.casecmp_pack_js,
                           #'/static/js/geoscope.pack.js?t=%s'%js_stamp.geoscope_pack_js,
                           ]
        cmpform = CaseCmpFormPage.fieldsCls(crt_user=self.crt_user)
        ctx['tabs']=[
            {'name':'cmp',
             'label':'案件比对',
             #'com':'com_tab_fields',
             'com':'com-tab-case-cmp',
             'director_name':cmpform.get_director_name(),
             #'model_name':model_to_name(DuchaCase),
             #'get_data':{
                 #'fun':'get_row',
                 #'kws':{
                    #'model_name':model_to_name(DuchaCase),
                    #'relat_field':'pk',              
                 #}
             #},          
             #'after_save':{
                 #'fun':'update_or_insert'
             #},
             'heads': cmpform.get_heads(),
             'ops': cmpform.get_operations()                 
             },
        ]
        return ctx
    
    class tableCls(ModelTable):
        model=DuchaCase
        exclude=['pic','audio','loc','KEY','id']
        #pop_edit_field='taskid'
        
        def dict_head(self, head):
            dc={
                'taskid':120,
                'subtime':120,
                'bigclass':100,
                'litclass':100,
                'addr':240,
            }
            if dc.get(head['name']):
                head['width'] =dc.get(head['name'])
            if head['name'] == 'taskid':
                head['editor'] = 'com-table-switch-to-tab'
                head['tab_name']='cmp'
            return head
        
        def get_operation(self):
            return []
    
        class sort(RowSort):
            names=['subtime'] 
            def get_query(self, query):
                if self.sort_str:
                    return RowSort.get_query(self,query)
                else:
                    return query.order_by('-subtime')
    
    #def get_context(self):
        #ctx = TablePage.get_context(self)
        #ctx['table_fun_config'] ={
               #'detail_link': '对比', 
           #}
        #return ctx

class CaseCmpFormPage(FieldsPage):
    template='case_cmp/casecmp_form.html'
    class fieldsCls(ModelFields):
        class Meta:
            model=DuchaCase
            exclude=[]
    
        def get_row(self):
            row = ModelFields.get_row(self)
            loc = row['loc']
            row['loc'] = row['loc'].x, row['loc'].y
            row['pic']=json.loads(row['pic'])
            #row['audio']=json.loads(row['audio'])
            
            distance = 100
            ref_location = loc
            ls = []
            for case in  JianduCase.objects.filter(loc__distance_lte=(ref_location, D(m=distance))):
                ls.append(
                    to_dict(case,filt_attr=lambda case :{'loc':[case.loc.x,case.loc.y]},exclude=['org_code'])
                )
            
            row['near_case']=ls
            return row
    
model_dc[DuchaCase]={'fields':CaseCmpFormPage.fieldsCls}

director.update({
    'case_cmp.duchacase':CaseCmpPage.tableCls,
    'case_cmp.duchacase.edit':CaseCmpFormPage.fieldsCls,    
})

page_dc.update({
    'case_cmp.duchacase':CaseCmpPage,
    'case_cmp.duchacase.edit':CaseCmpFormPage,
    
})
    