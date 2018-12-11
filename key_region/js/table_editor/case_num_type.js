Vue.component('com-table-case-num-type',{
    props:['rowData','field','index'],
    template:`<div style="text-align:center">
    <span v-text="num"></span><br><span style="color:gray;font-size:70%%;" v-text="litclass"></span>
    </div>`,
    data:function(){
        var dd = this.rowData[this.field]
        if(dd ){
            var num=dd.split('/')[0]
            var litclass = dd.split('/')[1]
        }else{
            var num=''
            var litclass = ''
        }
        return {
            num:num,
            litclass:litclass
        }
    },

})