# encoding:utf-8
from __future__ import unicode_literals
from django.core.management.base import BaseCommand
from django.conf import settings
#from case_cmp.spider.ducha import DuchaCaseSpider
from .. .port.ducha import DuchaPort
from case_cmp.models import DuchaCase
import json
from .alg.geo2 import  cord2loc
from django.contrib.gis.geos import Polygon,Point

import logging
log = logging.getLogger('case')

if getattr(settings,'DEV_STATUS',None)=='dev':
    import wingdbstub

class Command(BaseCommand):
    """
    检查监督员的位置，判断其是否出界
    """
    def add_arguments(self, parser):
        parser.add_argument('mintime', nargs='?',)
        
    def handle(self, *args, **options):
        
        #mintime = options.get('mintime')
        #if not mintime:
            #last_case = DuchaCase.objects.order_by('-subtime').first()
            #if last_case:
                #mintime=last_case.subtime
            #else:
                #mintime='all'  
        log.info('-' * 30)
        log.info('开始抓取【督查】按键')
        DuchaCase.objects.all().delete()
        #spd = DuchaCaseSpider()
        mover = DuchaPort()
        ls =[]
        count = 0
        for row in mover.get_data():
            count += 1
            #subtime = row[7]
            #if mintime !='all' and subtime <mintime:
                #return
            time_prefix =  '/'.join( [str( int(x) )for x in row['discovertime'].split('-')] )
            imagefilename = row['imagefilename']
            image_list = imagefilename.split(',')
            image_list = ["http://10.231.18.4/Mediainfo/18/%s/%s" % (time_prefix , x)for x in image_list]
            
            taskid = row['taskid']
            loc_x,loc_y = cord2loc(float( row.get('coordx') ),float( row.get('coordy') ))
            data_dc={
                'taskid':taskid,
                'subtime':row['discovertime'],
                'bigclass':row['bcname'],
                'litclass':row['scname'],
                'addr':row['address'],
                'loc':Point(x=loc_x,y=loc_y),
                'pic':json.dumps( image_list ),
  
            }
            ls.append(DuchaCase(**data_dc))
            
            #DuchaCase.objects.update_or_create(taskid=taskid,default=dft)
            #obj , _ = DuchaCase.objects.get_or_create(taskid=taskid)
            #obj.subtime=row[7]
            #obj.bigclass = row[4]
            #obj.litclass=row[5]
            #obj.addr=row[8]
            
            #obj.KEY=row[-2]
            #dc = row[-1]
            #loc_x,loc_y = cord2loc(float( dc.get('x') ),float( dc.get('y') ))
            #obj.loc=Point(x=loc_x,y=loc_y)
            #pic = [x['src'] for x in json.loads(dc.get('pic'))]
            #obj.pic= json.dumps(pic)
            #audio = [x['src'] for x in json.loads(dc.get('audio'))]
            #obj.audio= json.dumps(audio)
        DuchaCase.objects.bulk_create(ls)
        log.info('抓取完成，共抓取了%s' % count)
            
            
            
 
            
            
            

