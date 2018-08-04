from django.conf import settings
import requests
import json

proxies = getattr(settings,'DATA_PROXY',{})

class JianduPort(object):
    def __init__(self, start, end): 
        self.start = start
        self.end = end

    def get_data(self):
        url = settings.SANGO_BRIDGE+'/rq'
        has_next = True
        page = 1
        perpage = 500
        
        while has_next:
            data={
                'fun':'get_jiandu',
                'start': self.start,
                'end': self.end,
                'page':page, 
                'perpage':perpage
            }
            rt = requests.post(url,data=json.dumps(data), proxies = proxies)
            case_list = json.loads(rt.text)
            for item in case_list:
                yield item
            
            if len(case_list) < perpage:
                has_next = False
            else:
                page += 1
