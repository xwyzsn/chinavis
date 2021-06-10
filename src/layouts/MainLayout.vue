
<template>
  <q-layout view="hHh lpR fFf">

    <q-header elevated class="text-white" style="text-align: center;background:none" height-hint="98">
      <q-toolbar style="background: none">
        <q-toolbar-title>
          大气污染可视化
        </q-toolbar-title>
      </q-toolbar>

<!--      <q-tabs align="left">-->
<!--        <q-route-tab to="/page1" label="Page One" />-->
<!--        <q-route-tab to="/page2" label="Page Two" />-->
<!--        <q-route-tab to="/page3" label="Page Three" />-->
<!--      </q-tabs>-->
    </q-header>

    <q-page-container>
      <div >
        <div class="row justify-center q-pt-lg">
          <div class="col-2 q-pa-sm">
            <q-card style="height: 500px">
              <q-card-section>
                <div class="q-pa-sm" style="max-width: 300px">
                  <q-select v-model="select_year" :options="years" label="years" />
                  <q-select v-model="select_month" :options="months" label="months" />
                  <q-select v-model="select_day" :options="days" label="days" />
                </div>
              </q-card-section>
              <q-card-section style="text-align: center">

                数据为{{select_year}}年,{{select_month}}月,{{select_day}}日
                <q-separator class="q-mt-sm"></q-separator>
                <q-btn class="q-mt-sm" color="white" text-color="black" label="切换数据" @click="switchDate" />
              </q-card-section>
              <q-card-section style="text-align: center">
                <q-select v-model="polution_type" :options="polutions" label="polution" />
                <q-btn class="q-mt-sm q-mb-md" color="white" text-color="black" label="切换污染物" @click="switchType" />
                <br/>
                展示的污染物为 : {{this.polution_type}}
              </q-card-section>

            </q-card>
          </div>
          <div class="col-8 q-pa-sm">
            <q-card style="width:100%;height:500px" >
              <q-card-section>
                <div style=" width:100%;height:450px;position: relative" id="map"/>
              </q-card-section>
            </q-card>

          </div>
          <div class="col-2 q-pa-sm">
            <q-card style="height: 500px">
              <q-card-section>
                <div id="River-map"></div>
              </q-card-section>
            </q-card>

          </div>
        </div>

        <div class="row justify-center ">

          <div class="col-6" >
            <q-card style="height: 175px">

                <div id="river" style="height: 100%;width: 100%"></div>

            </q-card>
          </div>

        </div>

      </div>
    </q-page-container>

  </q-layout>
</template>




<script >
import {Scene,PointLayer,HeatmapLayer,Popup} from "@antv/l7";
import {GaodeMap,Mapbox} from "@antv/l7-maps"
import { DrillDownLayer } from '@antv/l7-district';
import {DataView,DataSet} from "@antv/data-set"

import { Dark } from 'quasar'
import * as d3 from "d3";
import * as echarts from "echarts";
import {Chart} from "@antv/g2";

export default {

  data () {
    const months=Array.from({length:12},(items,index)=>index+1)
    const days = Array.from({length:31},(item,index)=>index+1)

    return {
      air_data :[],
      select_year:2013,
      years:[2013,2014,2015,2016,2017,2018],
      select_month:1,
      month:[],
      select_day:1,
      months,
      days,
      polution_type:"PM2",
      base_url:'http://localhost:8003/201301tmp/CN-Reanalysis-daily-',
      scene:null,
      dv:null,
      drill:null,
      polutions:["PM2","PM10","SO2","NO2","CO","O3"],

    }
  },
  methods:{
    switchDate(){

      var y = this.select_year,m = this.select_month,d = this.select_day;
      if(m<10){
        m="0"+m
      }
      if(d<10){
        d="0"+d
      }
      var name = y+m+d+"00.csv";

      fetch(
        this.base_url+name
      )
        .then(res => res.text())
        .then(data => {
          const dv = new DataSet.DataView().source(data, {
            type: 'csv',
          });
          this.air_data = data
          this.dv = dv.rows;
          this.scene.getLayerByName("heatmap").setData(this.air_data)
          // this.drill.updateData(this.dv)
        })
    },
    switchType(){
      const l = this.scene.getLayerByName("heatmap")
      this.scene.removeLayer(l)
      // console.log(this.dv)
      // console.log(this.air_data)
      const layer = new HeatmapLayer({
        name:'heatmap',
        zIndex:1,
      })
        .source(this.air_data, {
          parser: {
            type: 'csv',
            x: 'lon',
            y: 'lat'
          },
          transforms: [
            {
              type: 'hexagon',
              size: 2500,
              field: this.polution_type,
              method: 'sum'
            }
          ]
        })
        .size('sum', sum => {
          return sum * 2000;
        })
        .shape('hexagonColumn')
        .style({
          coverage: 1,
          angle: 0,
          opacity: 1.0
        })
        .color('sum', [
          '#094D4A',
          '#146968',
          '#1D7F7E',
          '#289899',
          '#34B6B7',
          '#4AC5AF',
          '#5FD3A6',
          '#7BE39E',
          '#A1EDB8',
          '#C3F9CC',
          '#DEFAC0',
          '#ECFFB1'
        ]);
      // layer.active(true);
      layer.on("mousemove", (ev) => {
        const popup = new Popup()
          .setLnglat(ev.lngLat)
          .setHTML(`<span class="text-black">经度: ${ev.lngLat.lng}<br/>维度: ${ev.lngLat.lat}<br/>${this.polution_type}:
                 +${this.dv.rows[ev.featureId][this.polution_type]}</span>`);

        this.scene.addPopup(popup);
      }); // 鼠标在图层上移动时触发 // 鼠标在图层上移动时触发
      this.scene.addLayer(layer);

    },

  },
  mounted() {
    Dark.set(true)
    const scene = new Scene({
      id: 'map',
      map: new GaodeMap({
        pitch: 0,
        style: 'dark',
        zoom:4,

      }),
      logoVisible: false,
    });

    scene.on('loaded',()=>{
      this.scene=scene

      fetch(
        this.base_url+'2013010100.csv'
      )
        .then(res => res.text())
        .then(data => {
          const dv = new DataSet.DataView().source(data, {
            type: 'csv',
          });

          const  DrillLayer = new DrillDownLayer(scene,{
            data: dv.rows,
            viewStart: 'Country',
            viewEnd: 'Province',
            zIndex:0,
            visible:false,
            name:'drill',
            label: {
              enable: true,
              textAllowOverlap: false,
              //#7F7B7B
              color: "black",
              strokeWidth :0
            },
          })

          const layer = new HeatmapLayer({
            name:'heatmap',
            zIndex:1,
          })
            .source(data, {
              parser: {
                type: 'csv',
                x: 'lon',
                y: 'lat'
              },
              transforms: [
                {
                  type: 'hexagon',
                  size: 2500,
                  field: this.polution_type,
                  method: 'sum'
                }
              ]
            })
            .size('sum', sum => {
              return sum * 2000;
            })
            .shape('hexagonColumn')
            .style({
              coverage: 1,
              angle: 0,
              opacity: 1.0
            })
            .color('sum', [
              '#094D4A',
              '#146968',
              '#1D7F7E',
              '#289899',
              '#34B6B7',
              '#4AC5AF',
              '#5FD3A6',
              '#7BE39E',
              '#A1EDB8',
              '#C3F9CC',
              '#DEFAC0',
              '#ECFFB1'
            ]);
          // layer.active(true);
          this.air_data = data
          this.dv = dv
          layer.on("mousemove", (ev) => {
            const popup = new Popup()
              .setLnglat(ev.lngLat)
              .setHTML(`<span class="text-black">经度: ${ev.lngLat.lng}<br/>维度: ${ev.lngLat.lat}<br/>${this.polution_type}:
                 +${dv.rows[ev.featureId][this.polution_type]}</span>`);

            scene.addPopup(popup);
          }); // 鼠标在图层上移动时触发 // 鼠标在图层上移动时触发

          this.drill=DrillLayer
          scene.addLayer(layer);

          // scene.addLayer(DrillLayer);
        });
    })


    // fetch(
    //   'http://localhost:8003/201301tmp/CN-Reanalysis-daily-2013010100.csv'
    // )
    //   .then(res => res.text())
    //   .then(data => {
    //         const dv = new DataSet.DataView().source(data, {
    //           type: 'csv',
    //         });
    //
    //     const DrillLayer = new DrillDownLayer(scene,{
    //       data: dv.rows,
    //       viewStart: 'Country',
    //       viewEnd: 'Province',
    //       zIndex:0,
    //       visible:false,
    //
    //       label: {
    //         enable: true,
    //         textAllowOverlap: false,
    //         //#7F7B7B
    //         color: "black",
    //         strokeWidth :0
    //       },
    //     })
    //
    //
    //     const layer = new HeatmapLayer({
    //       name:'heatmapLayer',
    //       zIndex:1,
    //     })
    //       .source(data, {
    //         parser: {
    //           type: 'csv',
    //           x: 'lon',
    //           y: 'lat'
    //         },
    //         transforms: [
    //           {
    //             type: 'hexagon',
    //             size: 2500,
    //             field: "PM2.5(微克每立方米)",
    //             method: 'sum'
    //           }
    //         ]
    //       })
    //       .size('sum', sum => {
    //         return sum * 10000;
    //       })
    //       .shape('hexagonColumn')
    //       .style({
    //         coverage: 1,
    //         angle: 0,
    //         opacity: 1.0
    //       })
    //       .color('sum', [
    //         '#094D4A',
    //         '#146968',
    //         '#1D7F7E',
    //         '#289899',
    //         '#34B6B7',
    //         '#4AC5AF',
    //         '#5FD3A6',
    //         '#7BE39E',
    //         '#A1EDB8',
    //         '#C3F9CC',
    //         '#DEFAC0',
    //         '#ECFFB1'
    //       ]);
    //     // layer.active(true);
    //     layer.on("mousemove", (ev) => {
    //       console.log(dv.getColumnNames())
    //       const popup = new Popup()
    //         .setLnglat(ev.lngLat)
    //         .setHTML(`<span>test${ev.lngLat.lng}</span>`);
    //
    //         scene.addPopup(popup);
    //     }); // 鼠标在图层上移动时触发 // 鼠标在图层上移动时触发
    //
    //
    //     scene.addLayer(layer);
    //     scene.addLayer(DrillLayer);
    //   });
    //   // fetch(
    //   //   'http://localhost:8003/201301tmp/CN-Reanalysis-daily-2013010100.csv'
    //   // )
    //   //   .then(res =>res.text())
    //   //   .then(data => {
    //   //     const dv = new DataSet.DataView().source(data, {
    //   //       type: 'csv',
    //   //     });
    //   //     this.air_data = dv.rows
    //   //     console.log(dv.getColumnNames())
    //   //   const layer  = new HeatmapLayer({zIndex:2 })
    //   //     .source(data,{
    //   //       parser:{
    //   //         type:"csv",
    //   //         x:"lat",
    //   //         y:"lon"
    //   //       },
    //   //       transforms:[
    //   //         {
    //   //           type:'hexagon',
    //   //           size:2500,
    //   //           field:" U(m/s)",
    //   //           operation:'sum'
    //   //         }
    //   //       ]
    //   //     }).size('sum',sum=>{return sum*200;})
    //   //     .shape('hexagon')
    //   //     .style({
    //   //       coverage: 0.8,
    //   //       angle: 0,
    //   //       opacity: 1.0
    //   //     })
    //   //     .color('sum', [
    //   //       '#094D4A',
    //   //       '#146968',
    //   //       '#1D7F7E',
    //   //       '#289899',
    //   //       '#34B6B7',
    //   //       '#4AC5AF',
    //   //       '#5FD3A6',
    //   //       '#7BE39E',
    //   //       '#A1EDB8',
    //   //       '#C3F9CC',
    //   //       '#DEFAC0',
    //   //       '#ECFFB1'
    //   //     ]);
    //   //     layer.show()
    //   //     scene.addLayer(layer);
    //   //   });
    // var PM2 = []
    // var PM10 = []
    // var SO2 = []
    // var NO2 = []
    // var CO = []
    // var O3 = []
    // var date = []
    // var file;

    //这个是画条形图的
    // fetch("http://localhost:8003/j_test.json").then(res=>res.json()).then(Data => {
    //   var d = Data["18.34,109.25"];
    //   // const {DataView} = DataSet;
    //
    //   var DATA = new Array();
    //   for(var i in d ){
    //     DATA.push({city:i.split('.')[0],type:"NO2",value:+d[i]["NO2"]});
    //     DATA.push({city:i.split('.')[0],type:"CO",value:+d[i].CO})
    //     DATA.push({city:i.split('.')[0],type:"O3",value:+d[i].O3})
    //     DATA.push({city:i.split('.')[0],type:"PM2",value:+d[i].PM2})
    //     DATA.push({city:i.split('.')[0],type:"PM10",value:+d[i].PM10})
    //     DATA.push({city:i.split('.')[0],type:"SO2",value:+d[i].SO2})
    //
    //   }
    //   // console.log(DATA.length)
    //   var data = DATA
    //
    //   const chart = new Chart({
    //     container: 'river',
    //     autoFit: true,
    //     height: 200,
    //   });
    //   chart.data(data);
    //   chart.scale('value', {
    //
    //     alias: '占比（%）',
    //   });
    //   chart.axis('city', {
    //     tickLine: null,
    //     line: null,
    //   });
    //   chart.axis('value', {
    //     label: null,
    //     title: {
    //       style: {
    //         fontSize: 14,
    //         fontWeight: 300,
    //       },
    //     },
    //     grid: null,
    //   });
    //   chart.legend({
    //     position: 'top',
    //   });
    //   chart.coordinate('rect').transpose();
    //   chart.tooltip({
    //     shared: true,
    //     showMarkers: false,
    //   });
    //   chart.interaction('active-region');
    //   chart
    //     .interval()
    //     .adjust('stack')
    //     .position('city*value')
    //     .color('type', (type) => {
    //       if (type === 'NO2') {
    //         return '#1890ff';
    //       }
    //       if (type === 'CO') {
    //         return '#ced4d9';
    //       }
    //       if (type === 'O3') {
    //         return '#f0f2f3';
    //       }
    //       if (type === 'PM2.5') {
    //         return '#f5222d';
    //       }
    //       if(type === 'PM10'){
    //         return '#f0a2ff'
    //       }
    //       if(type === 'SO2'){
    //         return '#f78f23'
    //       }
    //     })
    //     .size(26)
    //     // .label('value*type', (val, t) => {
    //     //   const color = t === '首都人口' ? 'white' : '#47494b';
    //     //   if (val < 0.05) {
    //     //     return null;
    //     //   }
    //     //   return {
    //     //     position: 'middle',
    //     //     offset: 0,
    //     //     style: {
    //     //       fontSize: 12,
    //     //       fill: color,
    //     //       lineWidth: 0,
    //     //       stroke: null,
    //     //       shadowBlur: 2,
    //     //       shadowColor: 'rgba(0, 0, 0, .45)',
    //     //     },
    //     //   };
    //     // });
    //   chart.render();
    //
    // });

    //河流图
    fetch("http://localhost:8003/j_test.json").then(res=>res.json()).then(D =>{
      var d = D["18.34,109.25"];
      var l = new Array()
      for(var i in d){
        l.push({date:i.split('.')[0],type:"NO2",value:+d[i]["NO2"]});
        l.push({date:i.split('.')[0],type:"CO",value:+d[i].CO})
        l.push({date:i.split('.')[0],type:"O3",value:+d[i].O3})
        l.push({date:i.split('.')[0],type:"PM2",value:+d[i].PM2})
        l.push({date:i.split('.')[0],type:"PM10",value:+d[i].PM10})
        l.push({date:i.split('.')[0],type:"SO2",value:+d[i].SO2})
      }
      const chart = new Chart({
        container:'river',
        autoFit:true,

      })
      console.log(l)
      chart.data(l)
      chart.scale('date',{tickInterval:20})
      chart.legend({position:"right"})
      chart.axis('value',{
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
      chart.area().position('date*value').adjust(['stack','symmetric']).color('type').shape('smooth').style({fillOpacity:0.85});
      chart.interaction('brush');
      chart.render();


    })
  }
}
</script>
