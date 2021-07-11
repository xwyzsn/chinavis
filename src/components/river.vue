<template>
  <div id="river" ></div>
</template>

<script>
import {Chart, registerInteraction} from "@antv/g2";
import bus from "assets/bus";

export default {

  props:{
    area:String,
    mon:Number,
    year:String,
    standard:Array,
    day:Number,
    is_drill:Boolean,
    polu:Object
  },
  data(){

    return{
      chart:null,
      total_data:null,
      view:null,



    }
  },
  watch:{
    polu(newVal,oldVal){
      if(JSON.stringify(newVal)!=='{}'){
        var D = newVal
        this.total_data=this.deepCopyObj(D)
        var area = this.area

        var data = D[area]
        // console.log(this.is_drill,area)
        var _data = data.filter((d)=>{
          var m = this.mon
          if(this.mon<10){
            m ="0"+m
          }
          var time = this.year+"-"+m+"-"
          return d.date>=time+"01" && d.date<=time+"31"
        })
        var final_data=new Array()
        _data.forEach((d)=>{
          var stand = this.standard
          d.PM2 = (d.PM2-stand[0])>0?((d.PM2-stand[0])/stand[0]):0
          d.PM10 = (d.PM10-stand[1])>0?((d.PM10-stand[1])/stand[1]):0
          d.SO2 = (d.SO2-stand[2])>0?((d.SO2-stand[2])/stand[2]):0
          d.NO2 = (d.NO2-stand[3])>0?((d.NO2-stand[3])/stand[3]):0
          d.CO = (d.NO2-stand[4])>0?((d.CO-stand[4])/stand[4]):0
          d.O3 = (d.O3-stand[5])>0?((d.O3-stand[5])/stand[5]):0
          final_data.push({type:"NO2",value:+(d.NO2).toFixed(4),date:d.date})
          final_data.push({type:"CO",value:+(d.CO).toFixed(4),date:d.date})
          final_data.push({type:"O3",value:+(d.O3).toFixed(4),date:d.date})
          final_data.push({type:"PM2",value:+(d.PM2).toFixed(4),date:d.date})
          final_data.push({type:"SO2",value:+(d.SO2).toFixed(4),date:d.date})
          final_data.push({type:"PM10",value:+(d.PM10).toFixed(4),date:d.date})
        })

        const chart = new Chart({
          container:'river',
          autoFit:true,
          // height:200,
          // width:500

        })
        this.chart = chart

        const view  = chart.createView({
          region:{
            start:{x:0.0,y:0.0},
            end:{x:1,y:1}
          }
        })

        this.view=view


        view.data(final_data)
        view.scale('date',{tickInterval:20})
        view.legend({position:"right"})
        view.animate(true)
        view.axis('value',{
          line:{
            style:{
              lineWidth:1,
              stroke:'#bfbfbf'
            }
          },
          tickLine:{
            length:8,
            style:{
              stroke:'#ddd',

            }
          },
          grid:null
        });
        view.area().position('date*value').adjust(['stack','symmetric']).color('type').shape('smooth').style({fillOpacity:0.85});
        // view.interaction('brush');
        view.interaction('other-filter')


        bus.$on('sendMonth',(res,area)=>{
          const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
          let index = MONTHS.indexOf(res) + 1;
          let tmp = this.deepCopyObj(this.total_data);
          if(area ===undefined){
            area = "中华人民共和国"
          }
          // if(!this.is_drill){
          //   area = "中华人民共和国"
          // }
          let data = tmp[area]

          var _data = data.filter((d)=>{
            let m = index;
            if(index<10){
              m = "0" +m;
            }
            let time = this.year + "-" + m + "-";
            return d.date>=time+"01" && d.date<=time+"31"
          })


          var final_data=new Array()
          let stand = this.standard;
          _data.forEach((d)=>{

            d.PM2 = (d.PM2-stand[0])>0?((d.PM2-stand[0])/stand[0]):0
            d.PM10 = (d.PM10-stand[1])>0?((d.PM10-stand[1])/stand[1]):0
            d.SO2 = (d.SO2-stand[2])>0?((d.SO2-stand[2])/stand[2]):0
            d.NO2 = (d.NO2-stand[3])>0?((d.NO2-stand[3])/stand[3]):0
            d.CO = (d.NO2-stand[4])>0?((d.CO-stand[4])/stand[4]):0
            d.O3 = (d.O3-stand[5])>0?((d.O3-stand[5])/stand[5]):0

            final_data.push({type:"NO2",value:+(d.NO2).toFixed(4),date:d.date})
            final_data.push({type:"CO",value:+(d.CO).toFixed(4),date:d.date})
            final_data.push({type:"O3",value:+(d.O3).toFixed(4),date:d.date})
            final_data.push({type:"PM2",value:+(d.PM2).toFixed(4),date:d.date})
            final_data.push({type:"SO2",value:+(d.SO2).toFixed(4),date:d.date})
            final_data.push({type:"PM10",value:+(d.PM10).toFixed(4),date:d.date})
          })
          view.data(final_data)
          chart.render();
        })
        chart.render();

      }

    }

  },
  name: "river",
  mounted() {
    // fetch("http://localhost:8003/t.json").then(res=>res.json()).then(D =>{
    //
    //
    //
    //
    // })
  }
  ,
  methods:{
    deepCopyObj(obj) {
      if (null == obj || "object" != typeof obj) return obj;
      if (obj instanceof Date) {
        var copy = new Date();
        copy.setTime(obj.getTime());
        return copy;
      }
      if (obj instanceof Array) {
        var copy = [];
        for (var i = 0, len = obj.length; i < len; i++) {
          copy[i] = this.deepCopyObj(obj[i]);
        }
        return copy;
      }
      if (obj instanceof Object) {
        var copy = {};
        for (var attr in obj) {
          if (obj.hasOwnProperty(attr)) copy[attr] = this.deepCopyObj(obj[attr]);
        }
        return copy;
      }
      throw new Error("Unable to copy obj this object.");
    },
    update(area){

      var tmp = this.deepCopyObj(this.total_data)
      var data = tmp[area]
      var _data = data.filter((d)=>{
        var m = this.mon
        if(this.mon<10){
          m ="0"+m
        }
        var time = this.year+"-"+m+"-"
        return d.date>=time+"01" && d.date<=time+"31"
      })
      var final_data=new Array()

      _data.forEach((d)=>{
        var stand = this.standard
        d.PM2 = (d.PM2-stand[0])>0?((d.PM2-stand[0])/stand[0]):0
        d.PM10 = (d.PM10-stand[1])>0?((d.PM10-stand[1])/stand[1]):0
        d.SO2 = (d.SO2-stand[2])>0?((d.SO2-stand[2])/stand[2]):0
        d.NO2 = (d.NO2-stand[3])>0?((d.NO2-stand[3])/stand[3]):0
        d.CO = (d.NO2-stand[4])>0?((d.CO-stand[4])/stand[4]):0
        d.O3 = (d.O3-stand[5])>0?((d.O3-stand[5])/stand[5]):0
        final_data.push({type:"NO2",value:+(d.NO2),date:d.date})
        final_data.push({type:"CO",value:+(d.CO),date:d.date})
        final_data.push({type:"O3",value:+(d.O3),date:d.date})
        final_data.push({type:"PM2",value:+(d.PM2),date:d.date})
        final_data.push({type:"SO2",value:+(d.SO2),date:d.date})
        final_data.push({type:"PM10",value:+(d.PM10),date:d.date})
      })

      this.view.data(final_data)
      this.chart.render()


    }


  }
}
</script>

<style scoped>

</style>
