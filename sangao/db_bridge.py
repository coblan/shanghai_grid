import requests
import json
from django.conf import settings

proxies = getattr(settings,'DATA_PROXY',{})

def exec_sql(sql,small_key=True):
    url = settings.SANGO_BRIDGE+'/rq'
    data= {'fun':'exec_sql','sql':sql}
    rt = requests.post(url,data=json.dumps(data),proxies = proxies)
    rows= json.loads( rt.text )
    if small_key:
        temp_rows=[]
        for row in rows:
            temp_dc ={}
            for k,v in row.items():
                temp_dc[k.lower()]=v
            temp_rows.append(temp_dc)
        rows=temp_rows
    return rows
    