# encoding:utf-8
from __future__ import unicode_literals
from django.core.management.base import BaseCommand
import requests
import xmltodict
from inspector.models import Inspector
from django.conf import settings
#from .alg.geo import cord2loc
# 引入第二次的坐标映射算法
from .alg.geo2 import  cord2loc

class Command(BaseCommand):
    """
    获取赵巷所有监督员的位置
    """
    def handle(self, *args, **options):
        dc = self.get_pos()
        rows = self.parse_rt(dc)
        self.save_rows(rows)
    
    def get_pos(self):

        headers = {'SOAPAction':"http://www.china-gis.com/gisshare/Select",
                   'content-type': 'text/xml'}
        
        
        var_dict={
            #'inspector':'31189242',
            #'start':'2017121400',
            #'end':'2017121500',
            'dept':'20601', # 赵项代码
        }
        
        body="""<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:s="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            <SOAP-ENV:Body>
                <tns:Select xmlns:tns="http://www.china-gis.com/gisshare/">
                    <tns:sql>select a.*,b.lastx,b.lasty,b.updatetime as tracktime,case when (b.lastx=0 and b.lasty=0) then '0' else '1' end as onlinestatus,citygrid.FN_GET_CODENAME(a.rank,'028') as RANKTYPE,b.UPLOADNUM,citygrid.F_GET_KEEPERCOLOUR(a.RANK) as rankcolor from citygrid.t_keepersinfo a left join citygrid.t_keeperssameday b on a.keepersn=b.keepersn where 1=1  and a.DEPTCODE ='%(dept)s'  order by a.keepertype desc,onlinestatus desc,a.keepersn</tns:sql>
                    <tns:pageSize>0</tns:pageSize>
                    <tns:pageIndex>0</tns:pageIndex>
                </tns:Select>
            </SOAP-ENV:Body>
        </SOAP-ENV:Envelope>"""%(var_dict)


        url="http://10.231.18.6/wgh_qp/LogicWebService/Sql/SqlHelper.asmx"

        # proxies = {
            # 'http': 'socks5://0.tcp.ap.ngrok.io:13661',
        # }
        
       
        
        proxy = getattr(settings,'DATA_PROXY',None)
        if proxy:
            proxies = proxy           
            rt=requests.post(url,headers=headers,data=body,proxies=proxies)
        else:
            rt=requests.post(url,headers=headers,data=body)
        
        dc=xmltodict.parse(rt.content)
        
        return dc

    def parse_rt(self,dc):
        env = dc.get('soap:Envelope')
        bd = env.get('soap:Body')
        sel =bd.get('SelectResponse')
        sel_rt = sel.get('SelectResult')
        dc2 = xmltodict.parse(sel_rt)
        rt = dc2.get('Result')
        rows = rt.get('Rows')
        row = rows.get('Row')
        return row

    def save_rows(self,rows):
        for item in rows:
            try:
                inspector = Inspector.objects.get(code=item.get('KEEPERSN'))
                track_time= item.get('TRACKTIME')
                inspector.track_time=track_time.replace('/','-')
                
                x,y= item.get('LASTX'),item.get('LASTY')
                if x !='0' and y!='0':
                    inspector.last_loc = '%s,%s'%(cord2loc(float(x), float(y)))
                else:
                    inspector.last_loc = 'NaN'
                inspector.save()
            except Inspector.DoesNotExist:
                pass
            



