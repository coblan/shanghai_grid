# encoding:utf-8
from __future__ import unicode_literals
from django.contrib import admin
from helpers.director.shortcut import page_dc,TablePage,FieldsPage,ModelTable,ModelFields,\
     model_dc,RowSearch,RowFilter,director,RowSort
from geoscope.admin import BlockGroupTablePage,BlockGroupFormPage
from geoscope.models import BlockGroup,BlockPolygon
from .models import InspectorGroupAndWeilanRel,OutBlockWarning,WorkInspector
from inspector.models import InspectorGrop, InspectorWorkGroup
from geoscope.polygon import poly2dict
from django.utils import timezone
from .models import PROC_STATUS
from inspector.models import Inspector
from helpers.maintenance.update_static_timestamp import js_stamp

# Register your models here.
class Weilan(BlockGroupTablePage):
    
    def __init__(self,*args,**kw):
        super(Weilan,self).__init__(*args,**kw)
        self.table.set_belong('weilan')

class WeilanForm(BlockGroupFormPage):
    def __init__(self,*args,**kw):
        super(WeilanForm,self).__init__(*args,**kw)
        self.set_belong('weilan') 
    

# group_weilan_rel  = regist_director(name='dianzi_weilan.groupweilanrel',src_model=InspectorGroupAndWeilanRel)
class GroupWeilanRel(TablePage):
    template='dianzi_weilan/weilan.html'
    #template='jb_admin/table.html'
    def get_label(self):
        return '围栏信息'
    
    class tableCls(ModelTable):
        model=InspectorGroupAndWeilanRel
        exclude=['id']
        pop_edit_field='block'
        def get_heads(self):
            heads = ModelTable.get_heads(self)
            heads.append({'name':'hight_region',
                          'label':'围栏区域',
                          'editor':'com-table-extraclick',
                          'label':'提示',
                          'fun':'hight_region',
                          'width':60,
                          })
            return heads
        
        def dict_head(self, head):
            
            dc={
                'block':100,
                'groups':100,
            }
            if dc.get(head['name']):
                head['width'] =dc.get(head['name'])
                
            
            if head['name']=='groups':
                head['editor']='com-table-array-mapper'
                head['options']= [{'value': g.pk, 'label': g.name,}for g in InspectorGrop.objects.filter(kind = 1) ] #{g.pk:g.name for g in InspectorGrop.objects.filter(kind = 1)}
            if head['name']=='block':
                head['show_label']={
                    'fun':'use_other_field',
                    'other_field':'_block_label'
                }
                #head['editor']='com-table-label-shower'
            return head
        
        def dict_row(self, inst): 
            return {
                #'block': inst.block.name if inst.block else "",
                #'groups':';'.join([x.name for x in  inst.groups.all()]),
                'polygon': poly2dict( inst.block.bounding ) if inst.block else [],
                #'hight_region':'xx'
                #'block_img':"<a href='%s' target='_blank'><img src='%s' style='height:200px;'></a>"%(inst.block.shot,inst.block.shot) if inst.block else ""
            }

class GroupWeilanRelFormPage(FieldsPage):
    class fieldsCls(ModelFields):
        class Meta:
            model=InspectorGroupAndWeilanRel
            exclude=[]
        
        def dict_head(self, head): 
            if head['name'] == 'block':
                blocks = BlockPolygon.objects.filter(blockgroup__belong='weilan').distinct()
                head['options'] = [{'value':x.pk,'label':x.name} for x in blocks]
            if head['name'] == 'groups':
                groups = InspectorGrop.objects.all()
                head['groups'] = [{'value':x.pk,'label':x.name} for x in groups]
            return head
        
        #def dict_options(self):
            #blocks = BlockPolygon.objects.filter(blockgroup__belong='weilan').distinct()
            #groups = InspectorGrop.objects.all()
            #return {
                #'block':[{'value':x.pk,'label':x.name} for x in blocks],
                #'groups':[{'value':x.pk,'label':x.name} for x in groups],
            #}
        
            # blocks = BlockPolygon.objects.filter(blockgroup__belong='weilan').distinct()
            # return {
                # 'blocks':[{'value':x.pk,'label':x.name} for x in blocks]
            # }
        
        def dict_row(self, inst):
            return {
                'polygon': poly2dict( inst.block.bounding ) if inst.block else []
            }

class OutBlockWaringPage(TablePage):
    template='jb_admin/table.html'
    
    def get_label(self):
        return '围栏报警信息'
    
    class tableCls(ModelTable):
        model=OutBlockWarning
        exclude=['id']
        fields_sort=['inspector','code','proc_status','proc_detail','reason','manager','start_time', 'end_time']
        #pop_edit_field='inspector'
        def dict_row(self, inst):
            return {
                '_inspector_label': str(inst.inspector) if inst.inspector else "",
                'code':inst.inspector.code if inst.inspector else "",
                '_manager_label':str(inst.manager) if inst.manager else "",
                '_proc_status_label': inst.proc_status == 'processed',
                #'proc_detail':'<span class="ellipsis" style="max-width:100px">%s</span>'%inst.proc_detail
            }
        #def dict_head(self, head):
            #if head['name']=='proc_status':
                #head['type']='bool'
            #return head
        def dict_head(self, head):
            dc={
                'inspector':60,
                'proc_status':80,
                'proc_detail':160,
                'manager':100,
                'reason':160,
                'start_time':150, 
                'end_time': 150,
            }
            if dc.get(head['name']):
                head['width'] =dc.get(head['name'])              
            
            
            if head['name'] in[ 'inspector','manager','proc_status']:
                head['editor'] = 'com-table-label-shower'
            if head['name'] in ['proc_detail']:
                head['editor'] = 'com-table-linetext'
                head['readonly']={
                    'fun':'checkRowValue',
                    'field':'proc_status',
                    'target_value':'processed'
                    }
            if head['name']=='proc_status':
                head['editor'] = 'com-table-select'
                head['options'] = []
                for value,label in PROC_STATUS:
                    dc = {
                        'value':value,
                        'label':label
                    }
                    if value=='processed':
                        dc['html_label'] = '<span style="color:green">已处理</span>'
                    elif value =='unprocess':
                        dc['html_label'] = '<span style="color:red">未处理</span>'
                    head['options'].append(dc)
            return head
        
        def get_heads(self):
            heads = ModelTable.get_heads(self)
            for index,head in enumerate(heads):
                if head['name']=='inspector':
                    heads.insert(index+1, {
                        'name':'code',
                        'label':'编码',
                        'width':90
                    })
                    break
            return heads
        
        def get_operation(self):
            operations = ModelTable.get_operation(self)
            ops = filter(lambda op:op['name'] in ['save_changed_rows'] ,operations)
            ls=[{
                 'fun':'selected_set_value',
                 'editor':'com-op-btn',
                 'field':'proc_status',
                 'value':'processed',
                 'disabled':'!has_select',
                 #'hide':'!has_select',
                 'icon':'fa-circle',
                 'style':'color:green',
                 'label':'已处理'},
                {
                 'fun':'selected_set_value',
                 'editor':'com-op-btn',
                 'field':'proc_status',
                 'value':'unprocess',
                 'disabled':'!has_select',
                 #'hide':'!has_select',
                 'icon':'fa-exclamation',
                 'style':'color:red',
                 'label':'未处理'}, 
                
                ]
            ls.extend(ops)
            return ls
        
        class search(RowSearch):
            names=['inspector']
            def get_context(self):
                dc = super().get_context()
                dc.update({
                    'search_tip':'监督员姓名，编号'
                })
                return dc
            
            def get_query(self,query):
                self.valid_name=['inspector__name','inspector__code']
                return super().get_query(query)
            
                #if self.q:
                    #return query.filter(inspector__name__icontains=self.q,inspector__code__icontains=self.q)
                #else:
                    #return query
        class filters(RowFilter):
            names=['proc_status']
            range_fields = ['start_time']
            #range_fields=[{'name':'create_time','type':'date'}]
        
        class sort(RowSort):
            names=['start_time']

class OutBlockWarningFormPage(FieldsPage):
    class fieldCls(ModelFields):
        readonly=['manager','proc_time','inspector','create_time']
        class Meta:
            model=OutBlockWarning
            exclude=[]
        
        def get_row(self):
            row= ModelFields.get_row(self)
            row['create_time']= self.instance.create_time.strftime('%Y-%m-%d %H:%M:%S')
            row['proc_time']= self.instance.proc_time.strftime('%Y-%m-%d %H:%M:%S')
            return row
            
        def get_heads(self):
            heads = ModelFields.get_heads(self)
            heads.append({
                'name':'create_time',
                'label':'创建时间',
                'type':'linetext',
                'readonly':True
            })
            return heads
        
        def save_form(self):
            ModelFields.save_form(self)
            self.instance.manager=self.crt_user
            self.instance.save()

class WorkinspectorPage(TablePage):
    template='jb_admin/table.html'
    extra_js=['/static/js/dianzi_weilan.pack.js?t=%s'%js_stamp.dianzi_weilan_pack_js]
    def get_label(self):
        return '上班排单'
    
    class tableCls(ModelTable):
        model = WorkInspector
        exclude=['id']
        #pop_edit_field='date'
        
        def dict_head(self, head):
            
            dc={
                'date':120,
                'inspector':400,
            }
            if dc.get(head['name']):
                head['width'] =dc.get(head['name'])  
                
            if head['name']=='inspector':
                head['editor']='com-table-array-mapper'
                head['options']= [{'value': ins.pk, 'label':ins.name } for ins in Inspector.objects.all() ] #{ins.pk:ins.name for ins in Inspector.objects.all()}
            elif head['name']=='date':
                head['editor'] = 'com-table-switch-to-tab'
                head['tab_name']='workinspector_form'                
            return head
        
        #def dict_row(self, inst):
            #return {
                #'inspector':';'.join([unicode(x) for x in inst.inspector.all()])
            #}
    def get_context(self):
        ctx = TablePage.get_context(self)
        wkinsp_form = InspectorWorkScheduleForm(crt_user=self.crt_user)
        ctx['tabs']=[
            {'name':'workinspector_form',
             'label':'WorkInspector Form',
             'com':'com_tab_fields',
             'get_data':{
                 'fun':'get_row',
                 'kws':{
                    'director_name':InspectorWorkScheduleForm.get_director_name(),
                    'relat_field':'pk',              
                 }
             },
             'after_save':{
                 'fun':'update_or_insert'
             },
             'heads': wkinsp_form.get_heads(),
             'ops': wkinsp_form.get_operations()  
             }
        ]
        return ctx
    

#class WorkinspectorFormPage(FieldsPage):
    #template='dianzi_weilan/workinspector_form.html'
   
class InspectorWorkScheduleForm(ModelFields):
    class Meta:
        model = WorkInspector
        exclude= []
    
    def dict_head(self, head):
        if head['name']=='inspector':
            ls= []
            for group in InspectorGrop.objects.filter(kind = 2):
            #for group in InspectorWorkGroup.objects.all():
                ls.append({
                    'label':group.name,
                    'inspectors':[x.pk for x in group.inspector.all()]
                })
            head['editor'] = 'com-field-select-work-inspector' 
            head['groups']= ls
        return head
    
        
director.update({
    'dianzi_weilan':Weilan.tableCls,
    'dianzi_weilan.edit':WeilanForm.BlockGroupFormPage_normal.BlockGroupForm,
    'dianzi_weilan.warning':OutBlockWaringPage.tableCls,
    'dianzi_weilan.warning.edit':OutBlockWarningFormPage.fieldCls,
    'dianzi_weilan.groupweilanrel':GroupWeilanRel.tableCls,
    'dianzi_weilan.groupweilanrel.edit':GroupWeilanRelFormPage.fieldsCls,    
    
    'dianzi_weilan.workinspector':WorkinspectorPage.tableCls,
    'dianzi_weilan.workinspector.edit':InspectorWorkScheduleForm,    
})
#model_dc[InspectorGroupAndWeilanRel]={'fields':GroupWeilanRelFormPage.fieldsCls}
#model_dc[OutBlockWarning]={'fields':OutBlockWarningFormPage.fieldCls}
#model_dc[WorkInspector]={'fields':WorkinspectorFormPage.fieldsCls}

page_dc.update({
    'dianzi_weilan.blockgroup':Weilan,
    'dianzi_weilan.blockgroup.edit':WeilanForm,
    'dianzi_weilan.groupweilanrel':GroupWeilanRel,
    'dianzi_weilan.groupweilanrel.edit':GroupWeilanRelFormPage,
    
    'dianzi_weilan.warning':OutBlockWaringPage,
    'dianzi_weilan.warning.edit':OutBlockWarningFormPage,
    
    'dianzi_weilan.workinspector':WorkinspectorPage,
    #'dianzi_weilan.workinspector.edit':WorkinspectorFormPage,
})
# page_dc.update(group_weilan_rel)