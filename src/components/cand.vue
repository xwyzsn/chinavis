<template>
  <div>
<div id="cand"></div>
<!--  <div>{{pol}}</div>-->
  </div>
</template>

<script>
import DataSet from '@antv/data-set';
import DataView from "@antv/data-set"
import {Chart, registerInteraction} from '@antv/g2';
import bus from "assets/bus";

export default {
  name: "cand",

  props:{
    year:String,
    area:String,
    pollution:String,
    polu:Object
    // is_drill:Boolean
  },
  data(){
    return {
      Year:this.year,
      Area:this.area,
      Polution:this.pollution,
      chart:null,
      Data:null,
      total_data:null,
      months :['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
      send_area:"中华人民共和国",
      render:false


    }
  },
  computed:{
    pol :{
      get:function (){
         return this.$store.getters["polution/getPolution"]},
      set:function (newVal){
        this.render=!this.render

      }
    }

  },
  watch:{
      polu(newVal,oldVal){
        if (JSON.stringify(newVal) !== '{}') {
          const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];

          var data = newVal
          function getMonthWeek(date) {
            const year = date.getFullYear();
            const month = date.getMonth();
            const monthFirst = new Date(year, month, 0);
            const intervalDays = Math.round((date.getTime() - monthFirst.getTime()) / 86400000);
            const index = Math.floor((intervalDays + monthFirst.getDay()) / 7);
            return index;
          }

          var data_set=[]
          this.total_data = this.deepCopyObj(data)
          var area = this.area
          // if(!this.is_drill){
          //   area = "中华人民共和国";
          // }
          data_set = data[area]

          var _data = data_set.filter(d=>{

            return (d.date>=this.year+"-01-01" && d.date<=this.year+"-12-31")})

          _data.forEach(function (obj) {
            const date = new Date(obj['date']);
            const month = date.getMonth();
            obj.month = MONTHS[month];
            obj.day = date.getDay();
            obj.week = getMonthWeek(date).toString();
          });
          const dv = new DataSet().createView();
          dv.source(_data)
            .transform({
              type: 'sort-by',
              fields: ['day'],
              order: 'DESC'
            });

          const chart = new Chart({
            container: 'cand',
            autoFit: true,
            height: 400,
            padding: [40, 20,20, 10]
          });
          this.chart = chart
          this.Data = dv.rows
          chart.data(_data);
          chart.scale({
            PM2: {
              type: 'linear',
              min: 0,
              max: 200,
              sync: true
            },
            PM10:{
              type:'linear',
              min:0,
              max:400,
              sync:true
            },
            SO2:{
              type:'linear',
              min:0,
              max:100,
              sync:true
            },
            CO:{
              type:'linear',
              min:0,
              max:8,
              sync:true
            },
            O3:{
              type:"linear",
              min:0,
              max:250,
              sync:true
            },
            NO2:{
              type:"linear",
              min:0,
              max:200
            },
            date: {
              type: 'time'
            },
            day: {
              type: 'cat'
            },
            week:{
              type:"cat",
              values: ['6','5', '4', '3', '2', '1', '0']
            }
          });
          //
          chart.axis(false);
          chart.legend(this.pollution, {
            offset: 0
          });
          chart.tooltip({
            title: 'date',
            showMarkers: false
          });
          chart.facet('list', {
            fields: ['month'],
            cols: 3,
            padding: [0, 15, 30, 15],
            columnTitle: {
              offsetY: -10,
              style: {
                fontSize: 12,
                textAlign: 'center',
                fill: '#666'
              }
            },
            eachView: view => {
              view.polygon().position('day*week')
                .color(this.pollution, '#E3F6FF-#85C6FF-#0086FA-#0A61D7-#F51D27-#FA541C-#FFBE15-#FFF2D1')
                .style({
                  lineWidth: 1,
                  stroke: '#fff'
                });
            }
          });
          //
          chart.on('annotation-text:click',(e)=> {
            const mon = e.target.attrs.text;
            bus.$emit('sendMonth',mon,this.send_area)

          });

          chart.interaction('element-active');
          chart.on('element:click',(e)=>{

            bus.$emit('click_date',this.deepCopyObj(e.data.data))

          })
          chart.render();
        }

      }
  },
  mounted() {

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
    getMonthWeek(date) {
      const year = date.getFullYear();
      const month = date.getMonth();
      const monthFirst = new Date(year, month, 0);
      const intervalDays = Math.round((date.getTime() - monthFirst.getTime()) / 86400000);
      const index = Math.floor((intervalDays + monthFirst.getDay()) / 7);
      return index;
    },
    changeData(){

      this.chart.data(this.Data)
      this.chart.render()
    },
    changeYear(drill,area){
      const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];

      var _data_set = this.deepCopyObj(this.total_data)

      // console.log("orignal area",area)
      if(!drill){
        area = "中华人民共和国";
      }
     this.send_area=area;
      // console.log(this.is_drill,area)
      var data_set = _data_set[area]

      var _data = data_set.filter(d=>{

        return (d.date>=this.year+"-01-01" && d.date<=this.year+"-12-31")})
      function getMonthWeek(date) {
        const year = date.getFullYear();
        const month = date.getMonth();
        const monthFirst = new Date(year, month, 0);
        const intervalDays = Math.round((date.getTime() - monthFirst.getTime()) / 86400000);
        const index = Math.floor((intervalDays + monthFirst.getDay()) / 7);
        return index;
      };
      _data.forEach(function (obj) {
        const date = new Date(obj['date']);
        const month = date.getMonth();
        obj.month = MONTHS[month];
        obj.day = date.getDay();
        obj.week = getMonthWeek(date).toString();
      });
      const dv = new DataSet().createView();
      dv.source(_data)
        .transform({
          type: 'sort-by',
          fields: ['day'],
          order: 'DESC'
        });
      this.chart.data(_data)
      this.chart.render()
    }
  }


}
</script>

<style scoped>

</style>
