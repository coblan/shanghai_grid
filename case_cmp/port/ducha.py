from django.conf import settings
import requests
import json

class DuchaPort(object):
    def get_data(self):
        url = settings.SANGO_BRIDGE+'/rq'
        has_next = True
        page = 1
        while has_next:
            data={
                'fun':'get_ducha',
                'page':page, 
                'perpage':100
            }
            rt = requests.post(url,data=json.dumps(data))
            #print('here---', rt.text)
            case_list = json.loads(rt.text)
            for item in case_list:
                yield item
            
            if len(case_list) < 100:
                has_next = False
            else:
                page += 1
            print('DuchaPort fetch next batch')
        print('DuchaPort fetch complete')
