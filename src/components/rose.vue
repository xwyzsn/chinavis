<template>
<div id="rose">

</div>
</template>

<script>
import DataSet from "@antv/data-set";
import {Chart} from "@antv/g2";
import bus from "assets/bus";

export default {
  name: "rose",
  props:{
    year:String,
    month:Number,
    day:Number,
    area:String,
    standard:Array


  },

  data(){
    return {
      total_data:[],
      chart:null

    }
  },


  mounted() {
    bus.$on('click_date',(data)=>{
      var f =[]

      var d = this.deepCopyObj(data)
      var stand = this.standard
      d.PM2 = (d.PM2-stand[0])>0?((d.PM2-stand[0])/stand[0]):0
      d.PM10 = (d.PM10-stand[1])>0?((d.PM10-stand[1])/stand[1]):0
      d.SO2 = (d.SO2-stand[2])>0?((d.SO2-stand[2])/stand[2]):0
      d.NO2 = (d.NO2-stand[3])>0?((d.NO2-stand[3])/stand[3]):0
      d.CO = (d.NO2-stand[4])>0?((d.CO-stand[4])/stand[4]):0
      d.O3 = (d.O3-stand[5])>0?((d.O3-stand[5])/stand[5]):0

      f.push({type:"NO2",value:+(d.NO2)})
      f.push({type:"CO",value:+(d.CO)})
      f.push({type:"O3",value:+(d.O3)})
      f.push({type:"PM2",value:+(d.PM2)})
      f.push({type:"SO2",value:+(d.SO2)})
      f.push({type:"PM10",value:+(d.PM10)})

      this.chart.data(f)
      this.chart.render()
    })

    fetch("http://localhost:8003/t.json").then(res=>res.json()).then(data=>{

     var _data = data[this.area]
    this.total_data=this.deepCopyObj(data)
     var final =  _data.filter((d)=>{
        var m=this.month,day=this.day;
        if(this.month<10){
          m="0"+m
        }
        if(this.day<10){
          day="0"+day
        }

        var date = this.year+"-"+m+"-"+day;

        return d.date===date
      })
      var final_data=[]
      final.forEach((d)=>{
        var stand = this.standard
        d.PM2 = (d.PM2-stand[0])>0?((d.PM2-stand[0])/stand[0]):0
        d.PM10 = (d.PM10-stand[1])>0?((d.PM10-stand[1])/stand[1]):0
        d.SO2 = (d.SO2-stand[2])>0?((d.SO2-stand[2])/stand[2]):0
        d.NO2 = (d.NO2-stand[3])>0?((d.NO2-stand[3])/stand[3]):0
        d.CO = (d.NO2-stand[4])>0?((d.CO-stand[4])/stand[4]):0
        d.O3 = (d.O3-stand[5])>0?((d.O3-stand[5])/stand[5]):0
        final_data.push({type:"NO2",value:+(d.NO2)})
        final_data.push({type:"CO",value:+(d.CO)})
        final_data.push({type:"O3",value:+(d.O3)})
        final_data.push({type:"PM2",value:+(d.PM2)})
        final_data.push({type:"SO2",value:+(d.SO2)})
        final_data.push({type:"PM10",value:+(d.PM10)})
      })

      const chart = new Chart({
        container: 'rose',
        autoFit: true,
        // height: 500,
      });
     this.chart = chart;
      chart.data(final_data);
      chart.coordinate('polar');
      chart.axis(false);
      chart.tooltip({
        showMarkers: false
      });
      chart.interaction('element-highlight');
      chart
        .interval()
        .position('type*value')
        .label('type', {
          offset: -15,
        })
        .color('type')
        .style({
          lineWidth: 1,
          stroke: '#fff',
        });
      chart.render();
    })




  },
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
      var _data = tmp[area]

      var final =  _data.filter((d)=>{
        var m=this.month,day=this.day;
        if(this.month<10){
          m="0"+m
        }
        if(this.day<10){
          day="0"+day
        }
        var date = this.year+"-"+m+"-"+day;

        return d.date===date
      })
      var final_data=[]
      final.forEach((d)=>{
        var stand = this.standard
        d.PM2 = (d.PM2-stand[0])>0?((d.PM2-stand[0])/stand[0]):0
        d.PM10 = (d.PM10-stand[1])>0?((d.PM10-stand[1])/stand[1]):0
        d.SO2 = (d.SO2-stand[2])>0?((d.SO2-stand[2])/stand[2]):0
        d.NO2 = (d.NO2-stand[3])>0?((d.NO2-stand[3])/stand[3]):0
        d.CO = (d.NO2-stand[4])>0?((d.CO-stand[4])/stand[4]):0
        d.O3 = (d.O3-stand[5])>0?((d.O3-stand[5])/stand[5]):0
        final_data.push({type:"NO2",value:+(d.NO2)})
        final_data.push({type:"CO",value:+(d.CO)})
        final_data.push({type:"O3",value:+(d.O3)})
        final_data.push({type:"PM2",value:+(d.PM2)})
        final_data.push({type:"SO2",value:+(d.SO2)})
        final_data.push({type:"PM10",value:+(d.PM10)})


      })
      this.chart.data(final_data)
      this.chart.render()


    }


  }
}
</script>

<style scoped>








</style>
