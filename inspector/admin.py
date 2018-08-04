# encoding:utf-8
from __future__ import unicode_literals

from django.contrib import admin
from helpers.director.shortcut import ModelTable,TablePage,page_dc,FieldsPage,ModelFields,model_dc,RowSort,RowFilter,RowSearch,has_permit,director
from .models import Inspector,InspectorGrop, InspectorWorkGroup
from helpers.maintenance.update_static_timestamp import js_stamp
from . import admin_static
# Register your models here.

class InspectorPage(TablePage):
    template='jb_admin/table.html'
    #template='jb_admin/table_with_height.html'
    #template='inspector/inspector.html'
    def get_label(self, prefer=None):
        return '监督员名单'
    
    class InspectorTable(ModelTable):
        model=Inspector
        exclude=['id']
        pop_edit_field='name'
        
        def dict_head(self, head):
            dc={
                'name':80,
                'head':160,
                'gen':80,
                'code':100,
                'PDA':80,
                'last_loc':100,
                'track_time':160
            }
            if dc.get(head['name']):
                head['width'] =dc.get(head['name'])            
            
            if head['name']=='head':
                head['editor']='com-table-picture'
            return head
        
        class search(RowSearch):
            names=['name','code']
            
        class filters(RowFilter):
            names=['gen']
        
        class sort(RowSort):
            names=['name']
            chinese_words=['name']
        
        #def dict_head(self, head):
            #if head['name'] =='name':
                #head['editor'] = 'com-table-pop-fields'
                #head['fields_heads']=InspectorForm(crt_user=self.crt_user).get_heads()
                #head['get_row'] = {
                    ##'fun':'use_table_row'
                    #"fun":'get_table_row'
                    ##'fun':'get_with_relat_field',
                    ##'kws':{
                        ##"model_name":model_to_name(TbBanner),
                        ##'relat_field':'pk'
                    ##}
                #}
                #head['after_save']={
                    ##'fun':'do_nothing'
                    #'fun':'update_or_insert'
                #}
                #head['ops']=InspectorForm(crt_user=self.crt_user).get_operations()
            #return head
                
                #head['model_name']=model_to_name(TbBanner)
                
                #head['relat_field']='pk'
                #head['use_table_row']=True
                
        # def dict_row(self, inst):
            # return {
                # 'scope': ','.join([unicode(x) for x in inst.scope.all()])
            # }
        
    tableCls=InspectorTable
    


class InspectorForm(ModelFields):
    readonly=['last_loc','track_time']
    class Meta:
        model=Inspector
        exclude=[]
    
    def dict_head(self,head):
        if head['name'] == 'head':
            head['editor']='com-field-picture'
        return head
    
    #def get_heads(self):
        #heads = super(self.__class__,self).get_heads()
        #for head in heads:
            #if head.get('name') == 'head':
                #head['editor'] = 'picture'
                ##head['type']='picture'
                ##head['config']={
                ##'crop':True,
                ##'aspectRatio': 1,
                ##'size':{'width':250,'height':250}
            ##}
        #return heads        
        

class InspectorGroupPage(TablePage):
    template='jb_admin/table.html'
    def get_label(self):
        return '监督员分组'
    
    class tableCls(ModelTable):
        model=InspectorGrop
        exclude=['id']
        pop_edit_field='name'
        
        def dict_head(self, head):
            dc={
                'name':150,
                'inspector': 600,
            }
            if dc.get(head['name']):
                head['width'] =dc.get(head['name'])              
            
            if head['name']=='inspector':
                head['editor']='com-table-array-mapper'
                head['options']= [{'value': opt.pk, 'label': opt.name,} for opt in Inspector.objects.all()] #{opt.pk:opt.name for opt in Inspector.objects.all()}
            return head
        
        class search(RowSearch):
            names=['name']
        class sort(RowSort):
            names=['name']
            
        class filters(RowFilter):
            names = ['kind']
        #def dict_row(self, inst):
            #return {
                #'inspector':','.join([unicode(x) for x in inst.inspector.all()])
            #}
        
        #def dict_head(self, head):
            #if head['name'] =='name':
                #head['editor'] = 'com-table-pop-fields'
                #head['fields_heads']=InspectorGroupForm(crt_user=self.crt_user).get_heads()
                #head['get_row'] = {
                    ##'fun':'use_table_row'
                    #"fun":'get_table_row'
                    ##'fun':'get_with_relat_field',
                    ##'kws':{
                        ##"model_name":model_to_name(TbBanner),
                        ##'relat_field':'pk'
                    ##}
                #}
                #head['after_save']={
                    ##'fun':'do_nothing'
                    #'fun':'update_or_insert'
                #}
                #head['ops']=InspectorGroupForm(crt_user=self.crt_user).get_operations()
            #return head        
    


class InspectorGroupForm(ModelFields):
    class Meta:
        model=InspectorGrop
        exclude=[]
        
class InspectorMapPage(TablePage):
    template='inspector/inspector_map.html'
    class InspectorTable(ModelTable):
        model=Inspector
        exclude=[]
        
        # def dict_row(self, inst):
            # return {
                # 'scope': ','.join([unicode(x) for x in inst.scope.all()])
            # }
        
        def inn_filter(self, query):
            query = super(self.__class__,self).inn_filter(query)
            return query.exclude(last_loc='NaN').exclude(last_loc='')
        
        
    tableCls=InspectorTable

class InspectorWorkGroupPage(InspectorGroupPage):
    extra_js=['/static/js/inspector.pack.js?t=%s'%js_stamp.inspector_pack_js]
    class tableCls(InspectorGroupPage.tableCls):
        model = InspectorWorkGroup

class InspectorWorkGroupForm(ModelFields):
    class Meta:
        model = InspectorWorkGroup
        exclude = []
    def dict_head(self, head):
        if head['name']=='work_time':
            head['fv_rule']='work_time;'
        return head
        


director.update({
    'inspector':InspectorPage.tableCls,
    'inspector.edit':InspectorForm,
    'inspectorgroup':InspectorGroupPage.tableCls,
    'inspectorgroup.edit':InspectorGroupForm, 
    
    'inspectorWorkGroup': InspectorWorkGroupPage.tableCls,
    'inspectorWorkGroup.edit': InspectorWorkGroupForm,
})

model_dc[Inspector]={'fields':InspectorForm}
model_dc[InspectorGrop]={'fields':InspectorGroupForm}

page_dc.update({
    'inspector.inspector':InspectorPage,
    #'inspector.inspector.edit':InspectorFormPage,
    'inspector.inspectorgroup':InspectorGroupPage,
    #'inspector.inspectorgroup.edit':InspectorGroupFormPage,
    
    'inspector.inspector_map':InspectorMapPage,
    
    'inspectorWorkGroup': InspectorWorkGroupPage,
})