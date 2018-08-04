# encoding:utf-8

from __future__ import unicode_literals

#from django.db import models
from django.contrib.gis.db import models
from inspector.models import Inspector
#from helpers.base.jsonfield import JsonField

# Create your models here.

class DuchaCase(models.Model):
    taskid=models.CharField('任务号',max_length=20,blank=True)
    subtime=models.CharField('发现时间',max_length=20,blank=True)
    bigclass=models.CharField('大类',max_length=30,blank=True)
    litclass=models.CharField('小类',max_length=30,blank=True)
    addr=models.CharField('地址',max_length=500,blank=True)
    pic=models.TextField('图片',blank=True)
    audio=models.TextField('音频',blank=True)
    KEY=models.CharField('KEY',max_length=30,blank=True)
    loc = models.PointField(verbose_name='经纬度',blank=True,null=True)
    
    def __unicode__(self):
        return self.taskid
    

class JianduCase(models.Model):
    taskid=models.CharField('任务号',max_length=20,blank=True)
    subtime=models.CharField('发现时间',max_length=20,blank=True)
    bigclass=models.CharField('大类',max_length=60,blank=True)
    litclass=models.CharField('小类',max_length=60,blank=True)
    addr=models.CharField('地址',max_length=500,blank=True)
    loc = models.PointField(verbose_name='经纬度',blank=True,null=True)
    org_code =models.TextField('原始抓取数据',blank=True)
    
    infotypeid = models.IntegerField(help_text= '0:部件，1：事件')
    status = models.IntegerField(help_text= '5:待受理;9:结案;10:已作废')
    #keepersn = models.CharField(max_length=12, blank=True, null=True)
    keepersn = models.ForeignKey(to= Inspector, db_constraint= False, to_field= 'code', blank=True, null=True, db_column = 'keepersn')
    description = models.CharField(max_length=2000, blank=True, null=True)
    deptcode = models.CharField(max_length=10, verbose_name = '主责部门', help_text = '赵巷：20601')
    executedeptcode = models.CharField(max_length=20, blank=True, verbose_name = '三级主责部门', help_text = '赵巷：20601')
    
    
    
    