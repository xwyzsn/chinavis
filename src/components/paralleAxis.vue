<template>
  <div id="para" style="height: 100%;width: 100%">


  </div>

</template>

<script>
import * as  echarts from 'echarts/core'
import {
  ParallelComponent
} from 'echarts/components';
import {
  ParallelChart
} from 'echarts/charts';
import {
  CanvasRenderer
} from 'echarts/renderers';

export default {
  name: "paralleAxis",

  props:{
    area:String,
    month:Number,
  },
  data(){
    return{
      chart:null,
      Data:null
    }
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
    changeData(){
      var option = this.chart.getOption();
      var new_data = this.deepCopyObj(this.Data[this.area])
      var data = []
      new_data.forEach((d)=>{
        data.push( [d.PM2,d.PM10,d.SO2,d.NO2,d.CO,d.O3,d.U,d.V,d.TEMP,d.RH,d.PSFC])
      })

      option.series[0].data=data

      this.chart.setOption(option)
    },

  },
  mounted() {

    fetch('http://localhost:8003/t.json').then(res=>res.json()).then(d =>{
      this.Data = this.deepCopyObj(d)

      var _data = this.deepCopyObj(d[this.area])
      echarts.use(
        [ParallelComponent, ParallelChart, CanvasRenderer]
      );
      var chartDom = document.getElementById('para');
      var myChart =echarts.init(chartDom);
      var parallelAxis=[
        {dim:0,name:'PM10'},
        {dim:1,name:'PM2'},
        {dim:2,name:'SO2'},
        {dim:3,name:'NO2'},
        {dim:4,name:'CO'},
        {dim:5,name:'O3'},
        {dim:6,name:'U'},
        {dim:7,name:'V'},
        {dim:8,name:'TEMP'},
        {dim:9,name:'RH'},
        {dim:10,name:'PSFC'},
      ]
      var data = []

      _data.forEach((d)=>{
        data.push( [d.PM2,d.PM10,d.SO2,d.NO2,d.CO,d.O3,d.U,d.V,d.TEMP,d.RH,d.PSFC])
      })
      var  series = {
        type:'parallel',
        lineStyle:{width:0.3,opacity:0.1},
        data:data,

      }
      var option={
        parallelAxis:parallelAxis,
        series:series,
        parallel:{
          parallelAxisDefault:{
            interval :500
          }
        },
      }
      this.chart=myChart
      myChart.setOption(option);

    })


  }


}
</script>

<style scoped>

</style>
