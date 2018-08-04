from helpers.director.shortcut import TablePage, ModelTable, page_dc, director, RowFilter
from case_cmp.models import JianduCase
from django.db.models import F, Q, Case, When
from django.db.models.aggregates import Count,Sum
from django.utils.timezone import datetime,timedelta

class KeeperCaseStatic(TablePage):
    template = 'jb_admin/table.html'
    def get_label(self): 
        return '监督员统计'
    
    class tableCls(ModelTable):
        model = JianduCase
        exclude = ['loc', 'org_code', 'id']
        
        @classmethod
        def clean_search_args(cls, search_args):
            if '_start_subtime' not in  search_args.keys() and '_end_subtime' not in search_args.keys():
                today =datetime.now()
                day_30_ago = today-timedelta(days=30)                
                search_args['_start_subtime']= day_30_ago.strftime('%Y-%m-%d 00:00:00')
                search_args['_end_subtime'] =today.strftime('%Y-%m-%d 23:59:59') 
            return search_args
        
        #def __init__(self, _page=1, row_sort=[], row_filter={}, row_search='', 
                    #crt_user=None, perpage=None, **kw):
            #if '_start_subtime' not in  kw.keys() and '_end_subtime' not in kw.keys():
               
                #kw['_start_subtime']= str(day_30_ago)
                #kw['_end_subtime']= str(today)
                #kw['search_args']['_start_subtime']=str(day_30_ago)
                #kw['search_args']['_end_subtime'] = str(today)
            
            #super().__init__(_page, row_sort, row_filter, row_search, 
                    #crt_user, perpage, **kw)
        
        def get_heads(self): 
            return [
            {'name': 'keepersn__name','label': '监督员',}, 
            {'name': 'keepersn','label': '监督员编号',}, 
            {'name': 'nums_case','label': '立案数',}, 
            {'name': 'nums_simple','label': '简易案件',}, 
            {'name': 'nums_normal','label': '一般案件',}, 
            {'name': 'nums_bujian','label': '部件',}, 
            {'name': 'nums_shijian','label': '事件',}
            ]
        
        #def get_query(self): 
            #ls = []
            #for row in JianduCase.objects.all().values('keepersn').annotate(nums_case = Count('id')):
                #ls.append(row)
            #return ls
        def statistics(self, query): 
            """
            
            """
            return query.values('keepersn', 'keepersn__name').exclude(Q(status = 5) | Q(status = 10)|\
                                                                      Q(keepersn__isnull=True))\
                   .annotate(nums_case = Count('id'))\
                   .annotate(nums_simple = Count(Case(When(Q(deptcode = F('executedeptcode')) & Q( deptcode = '20601'), then= 1)) ))\
                   .annotate(nums_normal = F('nums_case') - F('nums_simple'))\
                   .annotate(nums_bujian = Count(Case(When(infotypeid = 0, then= 1))))\
                   .annotate(nums_shijian = Count(Case(When(infotypeid = 1, then= 1))))\
              
        
        class filters(RowFilter):
            range_fields = ['subtime']
            
            def dict_head(self, head):
                if head['name']=='subtime':
                    head['editor']='com-date-datetimefield-range-filter'
                return head
    
director.update({
    'keeper.caseStatic': KeeperCaseStatic.tableCls,
})
page_dc.update({
    'keeper.caseStatic': KeeperCaseStatic,
})