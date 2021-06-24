<template>
  <div style="height: 100%;width: 80%;margin-left: 10%" id="year-cmp" />

</template>

<script>
import {Chart} from "@antv/g2";

export default {
  name: "yearcmp",
  props:{
    area:String
  },
  mounted() {
    fetch('http://localhost:8003/t.json').then(res=>res.json()).then(d=>{
      var data = d[this.area]
      var _data=[]
      data.forEach((d)=>{
        _data.push({type:'PM2',value:+d.PM2,date:d.date})
        _data.push({type:'PM10',value:+d.PM10,date:d.date})
        _data.push({type:'SO2',value:+d.SO2,date:d.date})
        _data.push({type:'CO',value:+d.CO,date:d.date})
        _data.push({type:'O3',value:+d.O3,date:d.date})
        _data.push({type:'NO2',value:+d.NO2,date:d.date})

      })

      const chart = new Chart({
        container: 'year-cmp',
        autoFit: true,
        // height: 500,
        // padding: [30, 20, 70, 30]
      });
      chart.data(_data);
      // chart.scale({
      //   PM2: {
      //     min: 0,
      //     max: 200,
      //   },
      //   PM10:{
      //     min:0,
      //     max:400,
      //   },
      //   SO2:{
      //     min:0,
      //     max:100,
      //   },
      //   CO:{
      //     min:0,
      //     max:8,
      //   },
      //   O3:{
      //     min:0,
      //     max:400,
      //   },
      //   NO2:{
      //     min:0,
      //     max:200
      //   },
      //
      // });

      chart.legend('type',{position:"right"});

      chart.line().position('date*value').color('type','#1890ff-#2fc25b-#F6BD16-#F08BB4-#008685');


      chart.render();


    })



  }
}
</script>

<style scoped>

</style>
