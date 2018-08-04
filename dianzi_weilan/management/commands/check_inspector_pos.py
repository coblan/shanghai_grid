# encoding:utf-8
from django.core.management.base import BaseCommand
from inspector.models import Inspector
from .. .models import WorkInspector
from dianzi_weilan.warning import check_inspector,block_list,to_datetime
from django.conf import settings
from helpers.director.kv import get_value
from django.utils.timezone import datetime,timedelta
from dianzi_weilan.port_sangao import getKeeperTrack
import json
from dianzi_weilan.alg.checkpos import outBoxCheck, noPosCheck, removeInvalidPos
from sangao.cordToLoc import cordToloc
from django.contrib.gis.geos import Polygon,Point

import logging
log = logging.getLogger('task')

if getattr(settings,'DEV_STATUS',None)=='dev':
    import wingdbstub

class Command(BaseCommand):
    """
    检查监督员的位置，判断其是否出界
    """
    def add_arguments(self, parser):
        parser.add_argument('d', nargs='?',)
        
    def handle(self, *args, **options):
        log.info('-'*30)
        log.info('开始检查监督员坐标')
        
        day = options.get('d')
        if not day:
            day = datetime.now()
        else:
            day = datetime.strptime(day, '%Y-%m-%d')
        log.info('数据日期为：%s' % day)
        
        now = day
        checkDay = day
        today = now.date()
        startDate= today.strftime('%Y%m%d00')
        tomorro = now+timedelta(days=1)
        endDate= today.strftime('%Y%m%d23')
        log.info('today = %s' % today)
        try:
            todayWorkGroup= WorkInspector.objects.get(date=today)
            
            keepers = list( todayWorkGroup.inspector.all() )
            log.info('上班人数：%s' % len(keepers))
            
            for keeper in keepers:
                
                log.info('开始拉取%s轨迹数据' % str(keeper))
                tracks = getKeeperTrack(keeper.code, startDate, endDate)
                log.info('总共拉取了%s条' % len(tracks))
                posList = []
                for track in tracks:
                    x,y=cordToloc(track.get('coordx'),track.get('coordy'))
                    pos = Point(float(x),float(y))    
                    posList.append({'tracktime': datetime.strptime( track.get('tracktime'), '%Y-%m-%d %H:%M:%S' ),
                                    'pos': pos,})
                    
                log.info('开始去除无效轨迹点')
                posList = removeInvalidPos(keeper, posList)
                log.info('开始检查是否有工作时间内没有轨迹点的情况')
                noPosCheck(keeper,posList, checkDay)
                log.info('开始检查轨迹点是否跑到围栏外')
                outBoxCheck(keeper, posList)
        except WorkInspector.DoesNotExist:
            log.info('未设置工作组')
        #except Exception as e:
            #log.error(str(e))
        
        log.info('检查监督员完成')
                       
            
        #keeperSnList=[keeper.code for keeper in keeperList]
        
        #dc = getKeeperTrack(keeperSnList, startDate, endDate)
        #for keeper in keeperList:
            #posList = dc.get(keeper.code)
            #if posList:
                #outBoxCheck(keeper, posList)
                #noPosCheck(keeper,posList)
                
        
       
        #in_worktime=False
        #work_time = get_value('work_time','8:30-12:30;14:00-18:00')
        #log.info('设置的work_time=%s'% work_time)
        #ls =work_time.split(';')
        #for span in ls:
            #start,end = span.split('-')
            #start,end = (to_datetime(start),to_datetime(end))
            #if start <= now <=end:
                #in_worktime=True
        #log.info('当前时间 %s'%now )
        #if not in_worktime:
            #log.info('不在工作时间内' )
            #return
        #log.info('在工作时间内')
        
        #try:
            #workgroup = WorkInspector.objects.get(date=today)
            #log.info('开始遍历监督员')
            #for person  in workgroup.inspector.all():
                #if not list(block_list(person)):
                    #log.info('%s 没有block' % person)
                    #continue
                #else:
                    #check_inspector(person)

        #except WorkInspector.DoesNotExist:
            #log.info('working group of [%s] is not set'%today)
            ## 没设置上班组时，不报警
            #return 
        


    