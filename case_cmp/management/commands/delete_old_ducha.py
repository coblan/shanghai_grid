# encoding:utf-8
from __future__ import unicode_literals
from django.core.management.base import BaseCommand
from django.conf import settings
from case_cmp.spider.ducha import DuchaCaseSpider
from case_cmp.models import DuchaCase
import json
from .alg.geo2 import  cord2loc
from django.contrib.gis.geos import Polygon,Point
from django.utils.timezone import datetime

if getattr(settings,'DEV_STATUS',None)=='dev':
    import wingdbstub

class Command(BaseCommand):
    """
    删除过期的督察员案件
    """
  
        
    def handle(self, *args, **options):
        today = datetime.now()
        
        DuchaCase.objects.filter(subtime__gt='')
        
        mintime = options.get('mintime')
        if not mintime:
            last_case = DuchaCase.objects.order_by('-subtime').first()
            if last_case:
                mintime=last_case.subtime
            else:
                mintime='all'        
        
        spd = DuchaCaseSpider()
        for row in spd.get_data():
            subtime = row[7]
            if mintime !='all' and subtime <mintime:
                return
            
            taskid=row[1]
            obj , _ = DuchaCase.objects.get_or_create(taskid=taskid)
            obj.subtime=row[7]
            obj.bigclass = row[4]
            obj.litclass=row[5]
            obj.addr=row[8]
            
            obj.KEY=row[-2]
            dc = row[-1]
            #obj.coord='%s,%s'%(dc.get('x'),dc.get('y'))
            loc_x,loc_y = cord2loc(float( dc.get('x') ),float( dc.get('y') ))
            obj.loc=Point(x=loc_x,y=loc_y)
            pic = [x['src'] for x in json.loads(dc.get('pic'))]
            obj.pic= json.dumps(pic)
            audio = [x['src'] for x in json.loads(dc.get('audio'))]
            obj.audio= json.dumps(audio)
            
            
            obj.save()
            
            print(obj.taskid,obj.subtime)
            
            
            

