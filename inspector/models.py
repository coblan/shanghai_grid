# encoding:utf-8
from __future__ import unicode_literals

from django.db import models
# from geoinfo.models import BlockPolygon

# Create your models here.

GEN=(
    ('male','男'),
    ('female','女')
)


class Inspector(models.Model):
    name=models.CharField('姓名',max_length=50,blank=False)
    code=models.CharField('编号',max_length=50,blank=True, unique=True)
    gen=models.CharField('性别',max_length=30,choices=GEN,blank=True)
    # scope=models.ManyToManyField(BlockPolygon,verbose_name='工作区域',blank=True)
    PDA=models.CharField('PDA号码',max_length=100,blank=True)
    head=models.CharField('头像',max_length=300,blank=True)
    # group=models.ForeignKey(InspectorGrop,verbose_name='从属组',blank=True,on_delete=None,null=True)
    
    last_loc=models.CharField('上次坐标',max_length=100,blank=True)
    track_time= models.DateTimeField(verbose_name='追踪时间',blank=True,null=True)
    
    def __str__(self):
        return self.name

INSPECTOR_KIND = (
    (0, '缺省'), 
    (1, '围栏'), 
    (2, '排班')
)

class InspectorGrop(models.Model):
    name=models.CharField('组名',max_length=100,unique=True,blank=False, error_messages={'unique':"相同名字的组已经存在，请换一个名字"})
    inspector=models.ManyToManyField(Inspector,verbose_name='监督员',blank=True)
    kind = models.IntegerField(verbose_name= '类型', default= 0, choices= INSPECTOR_KIND )
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '监督员分组表'

class InspectorWorkGroup(models.Model):
    name=models.CharField('组名',max_length=100,unique=True,blank=False, error_messages={'unique':"相同名字的组已经存在，请换一个名字"})
    inspector=models.ManyToManyField(Inspector,verbose_name='监督员',blank=True)
    work_time = models.CharField('工作时间段',max_length= 300, help_text = '(8:00-12:00;13:30-17:30)<br>按照括号内的格式输入，以分号分割时间段')

    def __str__(self):
        return self.name

class InspectorCase(models.Model):
    code = models.CharField('编号',max_length=100,unique=True)
    page = models.TextField('案子页面',blank=True)
    update_time = models.DateTimeField('更新时间',auto_now=True)


