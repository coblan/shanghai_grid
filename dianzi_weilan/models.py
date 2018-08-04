# encoding:utf-8
from __future__ import unicode_literals

from django.db import models
from inspector.models import InspectorGrop,Inspector
from django.contrib.auth.models import User
from geoscope.models import BlockPolygon
# Create your models here.
class InspectorGroupAndWeilanRel(models.Model):
    block = models.OneToOneField(BlockPolygon,verbose_name='围栏名称',null=True,blank=True)
    groups = models.ManyToManyField(InspectorGrop ,verbose_name='应用对象',null=True,blank=True)
    
    def __unicode__(self):
        return unicode( self.block ) or '未命名围栏'

PROC_STATUS=(
    ('processed','已处理'),
    ('unprocess','未处理')
)
    
class OutBlockWarning(models.Model):
    inspector = models.ForeignKey(Inspector,verbose_name = '监察员')
    create_time = models.DateTimeField(verbose_name='告警时间',auto_now_add=True)
    #block = models.ForeignKey(BlockPolygon,verbose_name = '告警区域')
    manager=models.ForeignKey(User,verbose_name='处理人员',blank=True,null=True)
    proc_time = models.DateTimeField(verbose_name='处理时间', auto_now=True)
    proc_status = models.CharField('处理状态',max_length=30,choices=PROC_STATUS,default='unprocess')
    proc_detail = models.TextField('处理结果',blank=True)
    reason = models.CharField('警告原因',max_length=700,blank=True)
    start_time = models.DateTimeField(verbose_name='开始时间',blank=True,null=True)
    end_time = models.DateTimeField(verbose_name='结束时间',blank=True,null=True)
    
    def __unicode__(self):
        return "围栏告警 %s"% self.inspector 
    

class WorkInspector(models.Model):
    """
    当天的工作员工组
    """
    date = models.DateField(verbose_name='对应日期',blank=False,null=True)
    inspector = models.ManyToManyField(Inspector,verbose_name='对应监督员',blank=True)
    
    def __unicode__(self):
        return '上班排单'
    
    
