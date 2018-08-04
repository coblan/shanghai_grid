require('./scss/com_tab_case_cmp.scss')

var com_tab_case_cmp={
    props:['tab_head','par_row'],
    template:`<div class="flex" style="height: 100%">
        <div style="margin: 1em 2em;width: 30em;">
            <label for="">案件编号:</label><span v-text="row.taskid"></span><br/>
            <label for="">案件大类:</label><span v-text="row.bigclass"></span><br/>
            <label for="">案件小类:</label><span v-text="row.litclass"></span><br/>
            <label for="">发生地址:</label><span v-text="row.addr"></span><br/>
            <label for="">发生时间:</label><span v-text="row.subtime"></span><br/>
            <ul style="overflow: scroll;max-height: 70vh;">
                <li v-for="pic in row.pic"><img :src="pic" alt="" style="max-width: 300px"/></li>
            </ul>
        </div>
        <div class="flex-grow" style="position: relative;">
            <com-map ref="map_com"></com-map>
        </div>
    </div>`,
    data:function(){
        return {
            heads:this.tab_head.heads,
            ops:this.tab_head.ops,
            errors:{},
            row:{},
        }
    },
    mixins:[mix_fields_data],
    mounted:function(){
        var self=this
        this.getData(function(row){
            self.makeMap(row)
        })
    },
    methods:{
        on_show:function(){
            if(! this.fetched){
                this.getData()
                this.fetched = true
            }
        },
        getData:function(callback){
            var director_name=this.tab_head.director_name
            var relat_field = 'pk'
            var dc ={fun:'get_row',director_name:director_name}
            dc[relat_field] = this.par_row[relat_field]
            var post_data=[dc]
            var self =this
            cfg.show_load()
            ex.post('/d/ajax',JSON.stringify(post_data),function(resp){
                cfg.hide_load()
                self.row = resp.get_row
                callback(self.row)
            })
        },
        makeMap:function(row){
            var map_com = this.$refs.map_com
            map_com.on_init(function(){
                var lon= row.loc[0]
                var lat =  row.loc[1]
                var marker = new AMap.Marker({
                    icon: "http://webapi.amap.com/theme/v1.3/markers/n/mark_b.png",
                    position: [lon,lat],
                    title:ex.template('{bigclass}/{litclass}',row),
                    content:'<div class="red circle"></div>'
                });
                marker.setMap(map_com.map)

                AMap.event.addListener(marker, 'click', function() {
                    var url = ex.template('http://10.231.18.25/INSGRID/caseoperate_flat/XinZeng/EditFeedbackCaseInfo.aspx?KEY={KEY}&TYPE=3&pageindex=0&FanKui=1&sourctType=%E5%8C%BA%E7%BA%A7%E7%9D%A3%E5%AF%9F&categoryId=120',row)
                    window.open(url)
                });

                ex.each(row.near_case,function(lcase){
                    var marker = new AMap.Marker({
                        icon: "http://webapi.amap.com/theme/v1.3/markers/n/mark_b.png",
                        position: lcase.loc,
                        title: ex.template('{bigclass}/{litclass}/{subtime}',lcase),
                        content:'<div class="blue circle"></div>'
                    });
                    marker.setMap(map_com.map)

                    AMap.event.addListener(marker, 'click', function() {
                        var url = ex.template('http://10.231.18.25/CityGrid/CaseOperate_flat/ParticularDisplayInfo.aspx?taskid={taskid}',lcase)
                        window.open(url)
                        this.setContent('<div class="dark circle"></div>')
                    });

                })
                map_com.map.setFitView()
            })
        }
    }
}

//Vue.component('com-tab-case-cmp',com_tab_case_cmp)

Vue.component('com-tab-case-cmp',function(resolve,reject){
    ex.load_js(cfg.js_lib.geoscope_pack_js,function(){
        resolve(com_tab_case_cmp)
    })
})

