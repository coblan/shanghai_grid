require('./scss/com_field_select_work_inspector.scss')

var field_select_work_inspector =  {
    props:['row','head'],
    data:function(){
        return {
            crt_group:null
        }
    },
    template:`   <div>
        <ul v-if='head.readonly'><li v-for='value in row[head.name]' v-text='get_label(value)'></li></ul>
        <div v-else>
            <div style="width: 300px;padding: 1em 0;">
                <span>从监督员分组：</span>
                <select class="form-control" style="width:200px;display: inline-block;" v-model="crt_group">
                    <option  :value="null">---</option>
                    <option  v-for="group in head.groups" :value="group" v-text="group.label"></option>
                </select>
                <button @click="add_group()">添加</button>
            </div>

            <div class="select-work-inspector"  style="position: relative;width: 600px">
                <el-transfer
                v-model="row[head.name]"
                :titles="['可选人员', '已选人员']"
                :data="options"></el-transfer>
            </div>

            <!--<multi-chosen  v-model='row[head.name]' :id="'id_'+head.name"-->
                <!--:options='head.options'-->
                <!--ref="select">-->
            <!--</multi-chosen>-->
        </div>
    </div>`,
    computed:{
        label:function(){
            return this.row['_'+this.head.name+'_label']
        },
        options:function(){
            var op_list =  ex.map(this.head.options,function(option){
                return {key:option.value,label:option.label}
            })
            op_list = ex.sortOrder(op_list,'label')
            return op_list
        }
    },
    methods:{
        add_group:function(){
            if(this.crt_group){
                var self =this
                ex.each(self.crt_group.inspectors,function(inspector_pk){
                    if(!ex.isin(inspector_pk,self.row.inspector)){
                        self.row.inspector.push(inspector_pk)
                    }

                    //alert(inspector_pk)
                })
                //var tow_col_sel = this.$refs.two_col_sel
                //ex.each(tow_col_sel.can_select,function(item){
                //    if(ex.isin(item.value,self.crt_group.inspectors)){
                //        tow_col_sel.left_sel.push(item.value)
                //    }
                //})
                //tow_col_sel.batch_add()
            }
        }
    }
}

Vue.component('com-field-select-work-inspector',field_select_work_inspector)