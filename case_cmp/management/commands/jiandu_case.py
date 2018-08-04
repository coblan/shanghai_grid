# encoding:utf-8
from django.core.management.base import BaseCommand
from inspector.models import Inspector
#from dianzi_weilan.warning import check_inspector
from django.conf import settings
#from case_cmp.spider.jiandu import JianDuSpider
from .. .port.jiandu import JianduPort
from case_cmp.models import JianduCase
from django.contrib.gis.geos import Polygon,Point
from .alg.geo2 import cord2loc
from django.utils.timezone import datetime, timedelta
import time
import json

import logging
log = logging.getLogger('case')

if getattr(settings,'DEV_STATUS',None)=='dev':
    import wingdbstub

class Command(BaseCommand):
    """
    检查监督员的位置，判断其是否出界
    python manage.py jiandu_case
    python manage.py jiandu_case -s 2018-04-01 -e 2018-05-01
    """
    def add_arguments(self, parser):
        #parser.add_argument('mintime', nargs='?',)
        parser.add_argument('-s', nargs='?')
        parser.add_argument('-e', nargs='?')
        
    def handle(self, *args, **options):
        log.info('-' * 30)
        log.info('开始抓取【监督员】按键')
        
        today_str = datetime.now().strftime('%Y-%m-%d %H:%M:%D')

        print('start fetch jiandu %s' % today_str)
        
        tomorro = datetime.now() + timedelta(days = 1)
        tomorro_str = tomorro.strftime('%Y-%m-%d')
        
        start = options.get('s')
        if not start:
            lastone = JianduCase.objects.order_by('-subtime').first()
            if lastone:
                start = lastone.subtime[:10]
            else:
                start = today_str[:10]
        end= options.get('e') or tomorro_str
        #mintime = end
        #last_case = JianduCase.objects.order_by('-subtime').first()
        #if last_case:
            #mintime=last_case.subtime
        
        #start = options.get('s') or mintime[0:10]
        #spd = JianDuSpider(start,end)
        
        log.info('开始时间%s ; 结束时间%s' % (start, end))
        spd =  JianduPort(start = start, end = end)
        #count = 0
        
        #print('start get jiandu_case start=%s end=%s'%(start,end))
        ls = []
        count = 0
        created_count = 0
        for row in spd.get_data():
            count += 1
            #subtime = row[4]
            #count +=1
            #if count % 50 ==0:
                #print(count)
            #if subtime <= mintime:
                #return
            loc_x,loc_y = cord2loc(float( row.get('coordx') ),float( row.get('coordy') ))
            
            keeper = row['keepersn'] if  row['keepersn'] else None
            def_data={
               
                'subtime':row['discovertime'],
                'bigclass':row['bcname'],
                'litclass':row['scname'],
                'addr':row['address'],
                'loc':Point(x=loc_x,y=loc_y),
                'org_code': '' ,  #json.dumps(row), 现在不存储原始数据了，以后直接从三高系统里面刷新。
                'infotypeid': row['infotypeid'],
                'status': row['status'],
                'keepersn_id': keeper,
                'description': row['description'],
                'deptcode': row['deptcode'],
                'executedeptcode': row['executedeptcode'],
            }            
            log.info(row['taskid'])
            obj, created = JianduCase.objects.update_or_create(taskid = row['taskid'], defaults = def_data)
            if created:
                created_count += 1
    
        log.info('监督员按键抓取完成，总共抓取了 %s ,新建了 %s ' % (count, created_count) )
