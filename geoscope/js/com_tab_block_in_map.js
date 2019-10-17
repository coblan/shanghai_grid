Vue.component('com-tab-block-in-map',{
    props:['tab_head','par_row'],
    data(){
       window. controller = new PolygonGroupController()
        return {
            controller:controller
        }

    },
    mixins:[field_fun],
    mounted:function(){
        init_map()
        controller.set_drawer(drawer)
        controller.set_group(this.par_row.pk)
        controller.get_items()
        map.on('click',()=>{
            controller.map_click_callback()
        })
    },
    methods:{
        item_link:function(name){
            if(name!=this.crt_tab){
                return ex.appendSearch({_tab:name})
            }else{
                return 'javascript:;'
            }
        },
        toggle_fullscreen:function(){
            if(this.is_fullscreen){
                exit_fullscreen()
            }else{
                fullscreen()
            }
            this.is_fullscreen = !this.is_fullscreen

        },

    },
    template:`<div class="flex flex-grow" style="position: absolute;top:0;left: 0;right: 0;bottom: 0;">
        <div class="flex-grow" style="position: relative;">
            <div id="container"></div>

            <div style="position: absolute;right: 2em;top:2em;">
                <button @click="toggle_fullscreen()" type="button" class="btn btn-primary">全屏切换</button>
            </div>
        </div>

        <polygon-multi-btn-panel class="map-btn-panel" :crt_row="controller.crt_row" :items="controller.items" @new_row="controller.new_row()"></polygon-multi-btn-panel>
    </div>`
})

function init_map(){
    window.editorTool,window. map = new AMap.Map("container", {
        resizeEnable: true,
        center: [121.159647,31.157344],//地图中心点
        zoom: 13 //地图显示的缩放级别
    });
    window.mouseTool = new AMap.MouseTool(map);
//        map.setMapStyle('amap://styles/light');
    window.drawer={
        callback:function(polygon){
            console.log(polygon);//获取路径/范围
        },
        show:function(){
            there_com.show_map=true
            setTimeout(function(){
                map.setFitView();
            },100)

        },
        create_polygon:function(callback){

            this.callback = callback ||  this.callback
            mouseTool.polygon();
        },
        insert_polygon:function(arr){
            this._polygon= new AMap.Polygon({
                map: map,
                path: arr,
                strokeOpacity: 1,
                fillOpacity: 0.2,
                strokeWeight:1,
                strokeColor: "#000000",
                fillColor: "#999",
            })
            return this._polygon
        },
        edit_polygon:function(polygon){
            if(this._polygonEditor){
                this._polygonEditor.close()
            }
            this._polygonEditor= new AMap.PolyEditor(map, polygon);
            this._polygonEditor.open()
        },
        close_polygon:function(){
            if(this._polygonEditor){
                this._polygonEditor.close()
            }
        },
        submit:function(){
            // 需要设置 drawer.onsubmit
            var polygon_path = this._polygon.getPath()
            this.onsubmit(polygon_path)

        }
    }

    AMap.event.addListener( mouseTool,'draw',function(e){ //添加事件
//        console.log(e.obj.getPath());//获取路径/范围
        drawer.callback(e.obj.getPath())
        mouseTool.close( true)
    });
}
