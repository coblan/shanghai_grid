from helpers.maintenance.update_static_timestamp import js_stamp
from helpers.director.base_data import js_lib_list

def get_lib(request): 
    dc =  {
        'geoscope_pack_js':'/static/js/geoscope.pack.js?t=%s'%js_stamp.geoscope_pack_js,
        'gaode_css':'http://cache.amap.com/lbs/static/main1119.css',
        'gaode_js':'http://webapi.amap.com/maps?v=1.3&key=0909294a753dfe00a0aa124b6ecb93eb&plugin=AMap.PolyEditor,AMap.CircleEditor,AMap.MouseTool',
        'gaode_addtoolbar_js':'http://cache.amap.com/lbs/static/addToolbar.js'
    }
    return dc
js_lib_list.append(get_lib)