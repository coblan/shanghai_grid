# encoding:utf-8
from django.core.management.base import BaseCommand
from inspector.models import Inspector
from .. .models import WorkInspector
from dianzi_weilan.warning import check_inspector,block_list,to_datetime
from django.conf import settings
from helpers.director.kv import get_value
from django.utils.timezone import datetime,localtime

import logging
log = logging.getLogger('task')

if getattr(settings,'DEV_STATUS',None)=='dev':
    import wingdbstub

class Command(BaseCommand):
    """
    检查监督员的位置，判断其是否出界
    """
    def handle(self, *args, **options):
        log.info('-'*30)
        log.info('开始检测围栏')
        
        now = datetime.now()
        today = now.date()
        in_worktime=False
        work_time = get_value('work_time','8:30-12:30;14:00-18:00')
        log.info('设置的work_time=%s'% work_time)
        ls =work_time.split(';')
        for span in ls:
            start,end = span.split('-')
            start,end = (to_datetime(start),to_datetime(end))
            if start <= now <=end:
                in_worktime=True
        log.info('当前时间 %s'%now )
        if not in_worktime:
            log.info('不在工作时间内' )
            return
        log.info('在工作时间内')
        
        try:
            workgroup = WorkInspector.objects.get(date=today)
            log.info('开始遍历监督员')
            for person  in workgroup.inspector.all():
                if not list(block_list(person)):
                    log.info('%s 没有block' % person)
                    continue
                else:
                    check_inspector(person)

        except WorkInspector.DoesNotExist:
            log.info('working group of [%s] is not set'%today)
            # 没设置上班组时，不报警
            return 
        


