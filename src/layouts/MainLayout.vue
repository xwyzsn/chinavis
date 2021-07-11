
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
          <dv-border-box8 class="col-2" style="height: 100%">
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

                <div class="row">
                  <div class="col-5">
                <q-btn class="q-mt-sm q-ml-md" color="white" text-color="black" label="切换数据" @click="switchDate" />
                  </div>
                  <div class="col-5">
                    <q-btn class="q-mt-sm q-ml-md" color="white" text-color="black" label="年度对比" @click="showYear=!showYear" />
                    <q-dialog style="max-width: 1000px;width: 1000px;max-height: 800px" v-model="showYear" >
                      <q-card style="max-width: 1000px;width: 1000px;height: 600px;max-height: 800px">

                        <yearcmp  style="height: 100%;" :area="getProvince(curRegion.adcode_pro)" />

                        <q-card-actions align="right" >
                          <q-btn flat label="OK" color="primary" v-close-popup />
                        </q-card-actions>
                      </q-card>

                    </q-dialog>
                  </div>
                </div>
              </q-card-section>
              <q-card-section style="text-align: center">
                <q-select v-model="polution_type" :options="polutions" label="polution" />
                <q-btn class="q-mt-sm q-mb-md" color="white" text-color="black" label="切换污染物" @click="switchType" />
                <br/>
                展示的污染物为 : {{this.polution_type}}
              </q-card-section>

            </q-card>
          </div>
          </dv-border-box8>
          <dv-border-box-11 class="col-8" title="污染物空间分布图"  >
          <div class="col-8 ">
<!--            <q-card   >-->
<!--            margin-top: 5%;margin-left: 2%-->
<!--              <q-card-section>-->
                <div style=" width:95%;height:430px;position: relative;margin: 6% 2.5% 2%" id="map" />
<!--              </q-card-section>-->
<!--            </q-card>-->

          </div>
          </dv-border-box-11>
          <dv-border-box8 reverse class="col-2">
          <div class="col-2 q-pa-sm">
            <q-card style="height: 500px">
              <q-card-section>
                <div style="text-align: center">
                  {{select_year}}年月份热力图
                </div>
              </q-card-section>
              <q-separator/>
              <cand :polu="$store.getters['polution/getPolution']" v-bind:is_drill="is_dirll" ref="cand" :area="getProvince(curRegion.adcode_pro)" :year="select_year" :pollution="polution_type" style="width: 100%;max-width: 500px" />

            </q-card>

          </div>
          </dv-border-box8>
        </div>

        <div class="row justify-center">
          <dv-border-box1 class="col-5">
          <div class="col-5 q-ma-sm ">
            <q-card style="height: 260px">

<!--                <q-card-section>平行坐标轴</q-card-section>-->
              <q-card-section  @click="alert=!alert" >
              <div style="text-align: center">
              相关性分析图(点击可查看平行坐标)
              </div>
              </q-card-section>
              <q-separator/>
              <q-card-section>
                <coef ref="coef" style="height: 100%;width: 100%" :area="getProvince(curRegion.adcode_pro)" />
              </q-card-section>


              <q-dialog style="max-width:1000px;width: 1000px;height: 600px" v-model="alert">
                <q-card style="max-width:1000px;width: 1000px;height: 600px">
<!--                  <paralleAxis ref="para" :area="getProvince(curRegion.adcode_pro)"></paralleAxis>-->
                  <para :area="getProvince(curRegion.adcode_pro)" style="width: 500px;height: 500px"></para>
                  <div style="text-align: center">
                    国家污染标准-优-(可框选)相对应得数值进行查看
                    <!--                 polutions:["PM2","PM10","SO2","NO2","CO","O3"],   -->
                    &nbsp; PM2: &nbsp;{{standard_1[0]}}&nbsp; PM10:&nbsp;{{standard_1[1]}}&nbsp; SO2:&nbsp;{{standard_1[2]}}&nbsp; NO2:&nbsp;{{standard_1[3]}}
                    &nbsp; CO:&nbsp;{{standard_1[4]}}&nbsp; O3:&nbsp;{{standard_1[5]}}
                  </div>
                  <q-card-actions align="right" >

                    <q-btn flat label="OK" color="primary" v-close-popup />
                  </q-card-actions>
                </q-card>
              </q-dialog>
            </q-card>

          </div>
          </dv-border-box1>

          <dv-border-box1 class="col-4"  style="height: 100%; ">
          <div class="col-4 q-ma-sm " >

            <q-card style="height: 260px">
              <q-card-section>
                <div style="text-align: center">
                  月份污染物河流图
                </div>
              </q-card-section>
              <q-separator/>
<!--                <div id="river" style="height: 100%;width: 100%"></div>-->
                <river :polu="$store.getters['polution/getPolution']" :is_drill="is_dirll" ref="river" :day="select_day" :standard="select_standard==='standard_1'?standard_1:standard_2" :year="select_year" :mon="select_month" :area="getProvince(curRegion.adcode_pro)" style="width: 100%;height: 80%" />
            </q-card>
          </div>
          </dv-border-box1>

          <dv-border-box1 class="col-2" style="height: 100%">


          <div class=" col-2 q-ma-sm" >

            <q-card style="height: 260px">

              <q-card-section>
                <div style="text-align: center">
                单日污染物玫瑰图
                </div>
              </q-card-section>
              <q-separator></q-separator>

            <rose ref="rose" style="width: 100%;height: 80%" :polu="$store.getters['polution/getPolution']" :standard="select_standard==='standard_1'?standard_1:standard_2" :year="select_year" :month="select_month" :day="select_day" :area="getProvince(curRegion.adcode_pro)" />
            </q-card>

          </div>
          </dv-border-box1>
        </div>
<!--        <div class="row justify-center">-->
<!--          <div class="col-8">-->
<!--            <q-card style="height: 100px">-->
<!-- -->
<!--            </q-card>-->
<!--          </div>-->
<!--        </div>-->

      </div>
    </q-page-container>

  </q-layout>

</template>




<script >
import {Scene,HeatmapLayer,Popup} from "@antv/l7";
import {GaodeMap} from "@antv/l7-maps"
import { DrillDownLayer } from '@antv/l7-district';
import {DataSet} from "@antv/data-set"

import { Dark } from 'quasar'

import cand from "components/cand";
import river from "components/river";
import Rose from "components/rose";
import Coef from "components/coef";

import para from "components/para";
import Yearcmp from "components/yearcmp";

export default {
  components:{
    Yearcmp,
    // ParalleAxis,
    Coef,
    Rose,
    cand,
    river,
    para
  },

  data () {
    const months=Array.from({length:12},(items,index)=>index+1)
    const days = Array.from({length:31},(item,index)=>index+1)
    const adcodeMap = [
      {adcode: "110000", name: "北京市"},
      {adcode: "120000", name: "天津市"},
      {adcode: "130000", name: "河北省"},
      {adcode: "140000", name: "山西省"},
      {adcode: "150000", name: "内蒙古自治区"},
      {adcode: "210000", name: "辽宁省"},
      {adcode: "220000", name: "吉林省"},
      {adcode: "230000", name: "黑龙江省"},
      {adcode: "310000", name: "上海市"},
      {adcode: "320000", name: "江苏省"},
      {adcode: "330000", name: "浙江省"},
      {adcode: "340000", name: "安徽省"},
      {adcode: "350000", name: "福建省"},
      {adcode: "360000", name: "江西省"},
      {adcode: "370000", name: "山东省"},
      {adcode: "410000", name: "河南省"},
      {adcode: "420000", name: "湖北省"},
      {adcode: "430000", name: "湖南省"},
      {adcode: "440000", name: "广东省"},
      {adcode: "450000", name: "广西壮族自治区"},
      {adcode: "460000", name: "海南省"},
      {adcode: "500000", name: "重庆市"},
      {adcode: "510000", name: "四川省"},
      {adcode: "520000", name: "贵州省"},
      {adcode: "530000", name: "云南省"},
      {adcode: "540000", name: "西藏自治区"},
      {adcode: "610000", name: "陕西省"},
      {adcode: "620000", name: "甘肃省"},
      {adcode: "630000", name: "青海省"},
      {adcode: "640000", name: "宁夏回族自治区"},
      {adcode: "650000", name: "新疆维吾尔自治区"},
      {adcode: "710000", name: "台湾省"},
      {adcode: "810000", name: "香港特别行政区"},
      {adcode: "820000", name: "澳门特别行政区"},
    ]


    return {
      showYear:false,
      adcodeMap,
      alert:false,
      air_data :[],
      select_year:'2013',
      years:['2013','2014','2015','2016','2017','2018'],
      select_month:1,
      month:[],
      select_day:1,
      months,
      days,
      polution_type:"PM2",
      base_url:'https://xwyzsn.site/chinavis/CN-Reanalysis',
      scene:null,
      dv:null,
      drill:null,
      polutions:["PM2","PM10","SO2","NO2","CO","O3"],
      curRegion:{adcode_pro:0,NAME_CHN:"中华人民共和国"},
      select_chart:'river',
      charts:['river','other'],
      select_mode:'dark',
      modes:['dark','light'],
      standard_1:[35,50,50,80,4,100],
      standard_2:[75,70,150,80,4,160],
      select_standard:'standard_1',
      distrinct:[],
      is_dirll:false

    }
  },
  methods:{

    getProvince(adcode){
      var tmp = this.adcodeMap.filter((d)=>{
        return +d.adcode===+adcode
      })
      if(+adcode===0 || this.is_dirll===false) {
        // console.log("adcode",adcode,"drill",this.is_dirll)
        return "中华人民共和国"
      }
      return tmp[0].name
    },

    switchDate(){

      var m = this.select_month,d = this.select_day;
      if(m<10){
        m="0"+m
      }
      if(d<10){
        d="0"+d
      }

      fetch(
        this.base_url+this.select_year+m+"/"+this.select_year+m+"/CN-Reanalysis-daily-"+this.select_year+m+d+"00.csv"
      )
        .then(res => res.text())
        .then(data => {
          const dv = new DataSet.DataView().source(data, {
            type: 'csv',
          });
          this.air_data = data
          this.dv = dv;
          this.scene.getLayerByName("heatmap").setData(this.air_data)
          // this.drill.updateData(this.dv)
        })
      var area = this.getProvince(this.curRegion.adcode_pro)
      this.$refs.cand.changeYear(this.is_dirll)
      this.$refs.river.update(area)
      this.$refs.rose.update(area)

    },
    switchType(){
      const l = this.scene.getLayerByName("heatmap")
      this.scene.removeLayer(l)
      var index = this.polutions.indexOf(this.polution_type)
      var  stand = this.select_standard==='standard_1'?this.standard_1[index]:this.standard_2[index]

      var select = this.polution_type
      var area = this.getProvince(this.curRegion.adcode_pro)
      var dirll_state = this.is_dirll
      //adcode_pro


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
              type:'filter',
              callback(row){
                  if(dirll_state){
                    return row[select]>=stand&&row['province']===area;
                  }
                  else {
                    return row[select] >= stand;
                  }
              }
            },

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
          '#34B6B7',
          '#4AC5AF',
          '#5FD3A6',
          '#7BE39E',
          '#A1EDB8',
          '#C3F9CC',
          '#DEFAC0',
          '#F2EAEA'
        ]);

      layer.on('undblclick',(e)=>{
        this.curRegion={adcode_pro:0,NAME_CHN:"中华人民共和国"}
        this.is_dirll=!this.is_dirll;
        // this.switchType()
        var select = this.polution_type
        this.scene.getLayerByName("heatmap").setData(this.dv.rows,{
          parser:{
            type:'json',
            x: 'lon',
            y: 'lat'
          },
          transforms: [
            {
              type:'filter',
              callback(row){
                return  row[select]>=stand
              }
            },
            {
              type: 'hexagon',
              size: 2500,
              field: select,
              method: 'sum'
            }
          ]

        })

      })
      var area = this.getProvince(this.curRegion.adcode_pro)
      this.scene.addLayer(layer);
      this.$refs.cand.changeData()
      this.$refs.rose.update(area)


    },

  },

  created() {
    this.$store.dispatch('polution/getPolutionRemote')
    },
  mounted() {

    var data = require('../assets/t.json')
    this.$store.commit('polution/setPolution',data)


    fetch("https://xwyzsn.site/chinavis/distrinct_map.json").then(res =>res.json()).then(d =>{
      this.distrinct=d;
    })

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
    this.polutions=["PM2","PM10","SO2","NO2","CO","O3"];
    var index = this.polutions.indexOf(this.polution_type)
    var  stand = this.select_standard==='standard_1'?this.standard_1[index]:this.standard_2[index]
    // console.log(stand)
    var select = this.polution_type
    var dirll_state = this.is_dirll
    scene.on('loaded',()=>{
      this.scene=scene

      fetch(
        this.base_url+'201301/201301/CN-Reanalysis-daily-2013010100.csv'
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
            fill:{
              color:'#424242'
            },
            province:{
              provinceStroke:'#232323'
            },
            country:{
              countryStroke:'#232323'
            },
            popup: {
              enable: true,
              Html: props => {
                this.curRegion = props
                return `<span class="text-black" ">${props.NAME_CHN}</span>`;
              }
            },
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
                type:'filter',
                callback(row){
                  if(dirll_state){
                  return  row[select]>=stand &&row['province']===this.getProvince(this.curRegion.adcode_pro)}
                  else{
                    return row[select]>=stand
                  }
                }
              },
                {
                  type: 'hexagon',
                  size: 2500,
                  field: this.polution_type,
                  method: 'sum'
                }
              ]
            })
            .size('sum', sum => {
              if(sum<=0.15){
                return 0
              }
              else{
                return sum * 2000;
              }


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


          DrillLayer.provinceLayer.on('click',(e)=>{
            this.is_dirll=!this.is_dirll
            // console.log('click',this.is_dirll)
            var new_data=[]
            var area = this.getProvince(this.curRegion.adcode_pro)
            var index_list = this.distrinct[area]
            // console.log(index_list)
            index_list.forEach((v,i)=>{
              new_data.push(this.dv.rows[+v])
            })

            scene.getLayerByName("heatmap").setData(new_data,{
              parser:{
                type:'json',
                x: 'lon',
                y: 'lat'
              }
            })

            this.$refs.cand.changeYear(this.is_dirll,area)
            this.$refs.river.update(area)
            this.$refs.rose.update(area)
           this.$refs.coef.update(area)
            // this.$refs.para.changeData()
          })


          layer.on('undblclick',(e)=>{
            this.is_dirll=!this.is_dirll;
            // console.log(this.is_dirll)
            this.$refs.cand.changeYear(this.is_dirll)
            this.curRegion={adcode_pro:0,NAME_CHN:"中华人民共和国"}
            var select = this.polution_type
            scene.getLayerByName("heatmap").setData(this.dv.rows,{
              parser:{
                type:'json',
                x: 'lon',
                y: 'lat'
              },
              transforms: [
                {
                  type:'filter',
                  callback(row){
                    return  row[select]>=stand
                  }
                },
                {
                  type: 'hexagon',
                  size: 2500,
                  field: select,
                  method: 'sum'
                }
              ]

            })
            var area = this.getProvince(this.curRegion.adcode_pro)
            this.$refs.river.update(area)
            this.$refs.rose.update(area)
            this.$refs.coef.update(area)

          })
          scene.addLayer(layer);

        });
    })


  }
}
</script>

<style lang="sass" scoped>
.flex-break
  flex: 1 0 100% !important
  height: 0 !important
</style>
