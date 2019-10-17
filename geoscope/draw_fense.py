from helpers.director.shortcut import TablePage,ModelTable,page_dc,ModelFields,director
from .models import BlockPolygon,BlockGroup
from .polygon import dict2poly,poly2dict
from helpers.maintenance.update_static_timestamp import js_stamp

class DrawBlockGroupPage(TablePage):
    #extra_js=['http://webapi.amap.com/maps?v=1.3&key=您申请的key值&plugin=AMap.PolyEditor,AMap.CircleEditor,AMap.MouseTool',
          #'http://cache.amap.com/lbs/static/addToolbar.js',
        #'/static/js/geoscope.pack.js?t=%s'%js_stamp.geoscope_pack_js]
    
    
    def get_label(self):
        return '围栏区域编辑'
    def get_template(self, prefer=None):
        return 'geoscope/blockgroup_table.html'
    
    def get_context(self):
        ctx = super().get_context()
        group_form = DrawBlockForm(crt_user=self.crt_user)
        ctx.update({
            'named_ctx':{
                'block_group':[
                    {'name':'group_form',
                      'label':'分组信息',
                      'com':'com_tab_fields',
                      'get_data':{
                                'fun':'get_row',
                                'kws':{
                                   'director_name':group_form.get_director_name(),
                                   'relat_field':'pk',              
                                }
                            },
                            'after_save':{
                                'fun':'update_or_insert'
                            },
                            'heads': group_form.get_heads(),
                            'ops': group_form.get_operations()  
                            },
                    {'name':'map_edit','label':'区域编辑',
                     'com':'com-tab-block-in-map',
                     
                     }
                ]
            }
        })
        return ctx
    
    class tableCls(ModelTable):
        model=BlockGroup
        exclude=['id']
        
        def dict_head(self, head):
            width ={
                'name':150,
                'blocks':400,
                'belong':120,
            }
            if head['name'] in width:
                head['width'] = width.get(head['name'])
            
            if head['name'] =='name':
                head['editor'] = 'com-table-switch-to-tab'
                head['ctx_name'] = 'block_group'
                head['tab_name'] = 'group_form'
            return head
        
class DrawBlockForm(ModelFields):
    class Meta:
        model = BlockGroup
        exclude = []
        
        
director.update({
    'draw_block':DrawBlockGroupPage.tableCls,
    'draw_block.edit':DrawBlockForm,
})

page_dc.update({
    'draw_block':DrawBlockGroupPage
})
