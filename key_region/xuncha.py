# encoding:utf-8
from __future__ import unicode_literals

import requests
from django.conf import settings
from urllib.parse import urljoin

import json
from django.utils.timezone import datetime,timedelta
import math


class XunCha(object):
    xuncha_host = getattr(settings,'XUNCHA_HOST')
    def forcast(self):
        """
        @return: 给每个item添加上概率
        """
        data = self._get_data()
        data = self._cal_prob(data)
        return data
    
    def _get_data(self):
        """
        @return:[{polygon:[[1,2],[33,33]],time: "2018-02-08 07:53:21"}]
        """
        url = urljoin(self.xuncha_host,'forcast?jiezheng=14')
        rt = requests.get(url)
        return json.loads(rt.text)   
    
    def _cal_prob(self,data):
        last = data[0]
        last_time = last['time']
        last_time = datetime.strptime(last_time,'%Y-%m-%d %H:%M:%S')
        now = datetime.now()
        one_day=timedelta(days=1)
        
        today_mid=now.replace(hour=13,minute=0)
        last_day_mid=(now-one_day).replace(hour=13,minute=0)
        last_day_morning = (now-one_day).replace(hour=7,minute=0)
        
        # 总体基数
        base = 0.8
        # 判断当前检查区域，还没有被检查的概率
        if last_time > last_day_morning:
            last_pro=0.02
        elif last_time > last_day_mid:
            last_pro = 0.1
        elif last_time > today_mid:
            last_pro = 0.35
        else:
            last_pro = 0.8
        
        last['probability']='%d%%'%round(100* base * last_pro)
        left = 1-last_pro

        if data[1]['polygon'] == data[2]['polygon']:
            # 两个相同区域，去掉最后一个
            data[1]['probability'] ='%d%%'%round(100* base * left)
            data.pop() 
        else:
            data[1]['probability'] ='%d%%'%round(100* base * left*0.9)
            data[2]['probability'] ='%d%%'%round(100* base * left*0.1)            
        return data
        