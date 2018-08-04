import * as polygon_com from './polygon_com.js'
import {polygon_multi_btn_panel,PolygonGroupController} from  './polygon_multi_com.js'
import {map_com} from './map_com.js'
//import  {dispatch_panel} from './dispatch_panel_com.js'
require('./scss/map_btn_panel.scss')

import * as dispatch from './fullscreen.js'
import {shot} from './shot.js'

Vue.component('polygon-input',polygon_com.ploygon_editor)
Vue.component('polygon-multi-btn-panel',polygon_multi_btn_panel)

//Vue.component('com-dispatch-panel',dispatch_panel)

window.PolygonGroupController=PolygonGroupController