export var ploygon_editor={
    props:['name','row','kw'],
    template: `<div>
            <span v-if="row[name]"><i class="fa fa-map-o fa-2x" aria-hidden="true"></i></span>
            <button @click="create_new()" title="新建"><i class="fa fa-plus-square-o" aria-hidden="true"></i></button>
            <button @click="edit()" title="编辑"><i class="fa fa-pencil-square-o" aria-hidden="true"></i></button>
            <button @click="copy()">copy</button>
            <button @click="paste()">paste</button>
        </div>`,
    methods:{
        create_new:function(){
            //map.clearMap()

            drawer.show()
            drawer.create_polygon(function(polygon){
               var poly_obj =  drawer.insert_polygon(polygon)
                drawer.edit_polygon(poly_obj)
            });
            this.listn_submit()
        },
        edit:function(){
            drawer.show()
            if(this.row[this.name]){
                var polygon= JSON.parse(this.row[this.name])
                var poly_obj =  drawer.insert_polygon(polygon)
                drawer.edit_polygon(poly_obj)
            }
            this.listn_submit()
        },
        listn_submit:function(){
            var self=this
            drawer.onsubmit=function(polygon){
                var point_arr =  ex.map(polygon,function(point){
                    return [point.lng,point.lat]
                })
                self.row[self.name]=JSON.stringify(point_arr)
            }
        },
        copy:function(){
            localStorage.setItem('clip_polygon',this.row[this.name])
            alert('复制成功!')
        },
        paste:function(){
            var clip_polygon = localStorage.getItem('clip_polygon')
            if(clip_polygon){
                this.row[this.name]=clip_polygon
            }
            alert('粘贴成功!')
        }
    }
}
