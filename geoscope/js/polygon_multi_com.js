

export class PolygonGroupController{
    constructor(){
        this.items=[]
        this.crt_row={}
    }
    set_drawer(drawer){
        this.drawer=drawer
    }
    set_group(group_pk){
        this.group_pk=group_pk
    }
    get_items(){
        var self=this
        var post_data=[{fun:'block_group_items',group_pk:this.group_pk}]
        ex.post('/d/ajax/geoscope',JSON.stringify(post_data),function(resp){
            ex.each(resp.block_group_items,function(row){
                //self.insert(item)
                var poly = drawer.insert_polygon(row.bounding)
                self.add_poly_2_row(row,poly)
                self.items.push(row)
            })
            map.setFitView();
        })
    }
    on_map_click(callback){
        this.map_click_callback=callback
    }
    new_row(){
        var row={
            name:'未命名',
            desp:'描述',
            bounding:null,
            group:window.row.pk,
            _class:"geoscope.blockpolygon",
        }
        this.items.push(row)
        this.set_crt_polyon_row(row)
    }
    add_poly_2_row(row,poly){
        var self=this
        row.poly = poly

        //polygon_map[row]= poly
        poly.row=row
        poly.on('click',function(e){
            //self.set_crt_polyon_row(this.row)
            if(self.click_callback){
                self.click_callback(this.row)
            }
        })
    }
    delete_row(row){
        row.poly.setMap(null)
        ex.remove(this.items,row)

    }
    on_click(callback){
        this.click_callback=callback
    }
    set_crt_polyon_row(polygon_row){

        //if( this.crt_row != polygon_row){
            if(this.crt_row.poly ){
                this.crt_row.poly.setOptions({
                    strokeWeight:1,
                    strokeColor: "#000000",
                    fillColor: "#999",
                })
            }
            this.crt_row=polygon_row
            if(this.crt_row.poly ){
                this.crt_row.poly.setOptions({
                    fillColor:'#FFF',
                    strokeWeight:3,
                    strokeColor: "#0000ff",
                })
            }

        //}
    }
}




export var polygon_multi_btn_panel={
    props:['crt_row','items'],
    data:function(){

      return {
          editing:false,
          crt_view:'btn-panel',
      }
    },
    template:`<div style="float: right;">
                 <ul class="nav nav-tabs" style="margin-bottom:1em; ">
                  <li role="presentation" :class="{'active':crt_view=='btn-panel'}" @click="crt_view='btn-panel'">
                    <a href="#">编辑面板</a>
                    </li>
                  <li role="presentation" :class="{'active':crt_view=='list'}" @click="crt_view='list'">
                    <a href="#">分区列表</a>
                  </li>

                </ul>
                <div v-show="crt_view=='list'">
                    <ul>
                        <li v-for="item in items"><a @click="set_crt_row(item)" href="#" v-text="item.name"></a></li>
                    </ul>
                </div>
                <div v-show="crt_view=='btn-panel'">
                    <button v-show="!editing" @click="new_row()">新建</button>

                     <button v-show="!editing && !is_empty(crt_row)" @click="start_edit()">编辑</button>
                    <button v-show="editing" @click="save()">保存</button>
                    <button v-show="editing" @click="fallback()">取消</button>


                    <!--<button v-show="!editing && !is_empty(crt_row)" @click="remove()">移除</button>-->
                    <button v-show="!editing && !is_empty(crt_row)" @click="del(crt_row)">删除</button>
                    <div class="hr"></div>
                    <div>
                        <div class="panel-field">
                            <label for="">名字:</label><br/>
                            <span v-if="!editing" v-text="crt_row.name"></span>
                            <input v-else type="text" v-model="crt_row.name"/>
                        </div>
                        <div class="panel-field">
                             <label for="">描述:</label><br/>
                             <span v-if="!editing" v-text="crt_row.desp"></span>
                            <textarea v-else  rows="10" v-model="crt_row.desp"></textarea>
                        </div>
                        <div class="panel-field" v-if="editing">
                            <label  for="">区域:</label><br/>
                            <button v-show="editing" @click="edit_poly()">编辑分区</button>
                        </div>

                        <div class="panel-field">
                            <label for="">截图:</label><br/>
                             <img  v-if="!editing" :src="crt_row.shot">
                              <com-file-uploader v-else v-model="crt_row.shot" :config="{multiple:false}"></com-file-uploader>
                        </div>
                    <!--<button v-show="editing" @click="close_poly()">关闭编辑</button>-->
                    </div>

                </div>

     </div>`,


    mounted:function(){
        var self=this
        controller.on_click(function(row){
            if(!self.editing){
                controller.set_crt_polyon_row(row)
            }
        })
        controller.on_map_click(function(){
            if(!self.editing){
                controller.set_crt_polyon_row({})
            }
        })
    },

    methods:{
        set_crt_row:function(row){
            controller.set_crt_polyon_row(row)
        },
        is_empty:function(obj){
          return Object.keys(obj).length ==0
        },
        new_row:function(){
            this.$emit('new_row')
            this.editing=true
        },
        start_edit:function(){
            this.editing=true
            this.fallback_cache = {
                name: this.crt_row.name,
                desp: this.crt_row.desp,
                oldpath : ex.map(this.crt_row.bounding ,function(pos){
                    return [pos.lng,pos.lat]
                })
            }
        },
        save:function(){
            var self=this
            var row={}
            ex.assign(row,this.crt_row)
            if(!row.poly){
                alert('请创建一个多边形')
                return
            }

            var path_pos= row.poly.getPath()
            row.bounding= ex.map(path_pos,function(pos){
                return [pos.lng,pos.lat]
            })
            row._director_name = 'geoscope.blockpolygon.edit'

            delete row['poly']

            var post_data=[{fun:'save_row',row:row}]
            ex.post("/d/ajax",JSON.stringify(post_data),function(resp){
                var resp_row=resp.save_row
                self.crt_row.id=resp_row.id
                self.crt_row.pk=resp_row.pk

                self.editing=false
                self.close_poly()
            })
        },
        fallback:function(){
            this.close_poly()
            this.editing=false

            if(!this.crt_row.pk){
                // 新建的情况
                if(this.crt_row.poly){

                    this.crt_row.poly.setMap(null)
                }
                controller.items.pop()
                controller.crt_row={}
            }else{
                this.crt_row.name=this.fallback_cache.name
                this.crt_row.desp=this.fallback_cache.desp

                // 因为高德的Polygon直接操作opiotns设置的array属性，
                // bounding 与 poly_bounding 的数据应该一致，所以有下面两行
                this.crt_row.bounding=this.fallback_cache.oldpath
                this.crt_row.poly.setPath(this.crt_row.bounding)
            }


        },
        _create_poly:function(){
            var self=this
            drawer.create_polygon(function(polygon){
                var poly_obj =  drawer.insert_polygon(polygon)
                controller.add_poly_2_row(self.crt_row,poly_obj)
                controller.set_crt_polyon_row(self.crt_row)
                drawer.edit_polygon(poly_obj)
            });
        },
        edit_poly:function(){
            var self=this
            if(!this.crt_row.poly ){
                self._create_poly()
            }else{
                var poly_obj = this.crt_row.poly
                drawer.edit_polygon(poly_obj)
            }

        },
        close_poly:function(){
            drawer.close_polygon()
        },
        remove:function(){
            confirm("真的将该划分区域从该组中移除吗？",function(resp){
                alert(resp)
            })
        },
        del:function(row){
            var r = confirm("真的删除该划分区域吗？")
            if(r){
                if(row.pk){
                    var self=this


                    var post_data=[{fun:'del_rows',rows:[{pk:row.pk,_director_name:'geoscope.blockpolygon.edit'}]}]
                    ex.post('/d/ajax',JSON.stringify(post_data),function(resp){
                        controller.delete_row(row)
                    })
                }else{
                    controller.delete_row(row)
                }

            }

        }
    }
}