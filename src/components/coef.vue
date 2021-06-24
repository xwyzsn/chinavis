<template>
  <div>
<div id="coef">
</div>
    <div id="sanky"></div>
  </div>
</template>

<script>
import {Chart, registerInteraction} from "@antv/g2";
import DataSet from "@antv/data-set";

export default {
  name: "coef",
  props:{
    area:String
  },
  data(){
    return {
    total_data:null,
      view:null,
      chart:null
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
    update(area){
      var data =this.deepCopyObj(this.total_data[area])
      var fianl=new Array()
      registerInteraction('element-link', {
        start: [
          {trigger: 'interval:mouseenter', action: 'element-link-by-color:link'}
        ],
        end: [
          {trigger: 'interval:mouseleave', action: 'element-link-by-color:unlink'}
        ]
      });

      fianl.push({polution:'PM2',type:'U',value:data.PM2.U})
      fianl.push({polution:'PM2',type:'V',value:data.PM2.V})
      fianl.push({polution:'PM2',type:'TEMP',value:data.PM2.TEMP})
      fianl.push({polution:'PM2',type:'RH',value:data.PM2.RH})
      fianl.push({polution:'PM2',type:'PSFC',value:data.PM2.PSFC})

      fianl.push({polution:'PM10',type:'U',value:data.PM10.U})
      fianl.push({polution:'PM10',type:'V',value:data.PM10.V})
      fianl.push({polution:'PM10',type:'TEMP',value:data.PM10.TEMP})
      fianl.push({polution:'PM10',type:'RH',value:data.PM10.RH})
      fianl.push({polution:'PM10',type:'PSFC',value:data.PM10.PSFC})

      fianl.push({polution:'SO2',type:'U',value:data.SO2.U})
      fianl.push({polution:'SO2',type:'V',value:data.SO2.V})
      fianl.push({polution:'SO2',type:'TEMP',value:data.SO2.TEMP})
      fianl.push({polution:'SO2',type:'RH',value:data.SO2.RH})
      fianl.push({polution:'SO2',type:'PSFC',value:data.SO2.PSFC})

      fianl.push({polution:'NO2',type:'U',value:data.NO2.U})
      fianl.push({polution:'NO2',type:'V',value:data.NO2.V})
      fianl.push({polution:'NO2',type:'TEMP',value:data.NO2.TEMP})
      fianl.push({polution:'NO2',type:'RH',value:data.NO2.RH})
      fianl.push({polution:'NO2',type:'PSFC',value:data.NO2.PSFC})

      fianl.push({polution:'CO',type:'U',value:data.CO.U})
      fianl.push({polution:'CO',type:'V',value:data.CO.V})
      fianl.push({polution:'CO',type:'TEMP',value:data.CO.TEMP})
      fianl.push({polution:'CO',type:'RH',value:data.CO.RH})
      fianl.push({polution:'CO',type:'PSFC',value:data.CO.PSFC})

      fianl.push({polution:'O3',type:'U',value:data.O3.U})
      fianl.push({polution:'O3',type:'V',value:data.O3.V})
      fianl.push({polution:'O3',type:'TEMP',value:data.O3.TEMP})
      fianl.push({polution:'O3',type:'RH',value:data.O3.RH})
      fianl.push({polution:'O3',type:'PSFC',value:data.O3.PSFC})
      this.view.data(fianl)
      this.chart.render()


    }
  },
  mounted() {
    fetch('http://localhost:8003/coef.json').then(res=>res.json()).then(d=>{
      this.total_data=d
      var data = d[this.area]
      var fianl=new Array()
      registerInteraction('element-link', {
        start: [
          {trigger: 'interval:mouseenter', action: 'element-link-by-color:link'}
        ],
        end: [
          {trigger: 'interval:mouseleave', action: 'element-link-by-color:unlink'}
        ]
      });

      fianl.push({polution:'PM2',type:'U',value:data.PM2.U})
      fianl.push({polution:'PM2',type:'V',value:data.PM2.V})
      fianl.push({polution:'PM2',type:'TEMP',value:data.PM2.TEMP})
      fianl.push({polution:'PM2',type:'RH',value:data.PM2.RH})
      fianl.push({polution:'PM2',type:'PSFC',value:data.PM2.PSFC})

      fianl.push({polution:'PM10',type:'U',value:data.PM10.U})
      fianl.push({polution:'PM10',type:'V',value:data.PM10.V})
      fianl.push({polution:'PM10',type:'TEMP',value:data.PM10.TEMP})
      fianl.push({polution:'PM10',type:'RH',value:data.PM10.RH})
      fianl.push({polution:'PM10',type:'PSFC',value:data.PM10.PSFC})

      fianl.push({polution:'SO2',type:'U',value:data.SO2.U})
      fianl.push({polution:'SO2',type:'V',value:data.SO2.V})
      fianl.push({polution:'SO2',type:'TEMP',value:data.SO2.TEMP})
      fianl.push({polution:'SO2',type:'RH',value:data.SO2.RH})
      fianl.push({polution:'SO2',type:'PSFC',value:data.SO2.PSFC})

      fianl.push({polution:'NO2',type:'U',value:data.NO2.U})
      fianl.push({polution:'NO2',type:'V',value:data.NO2.V})
      fianl.push({polution:'NO2',type:'TEMP',value:data.NO2.TEMP})
      fianl.push({polution:'NO2',type:'RH',value:data.NO2.RH})
      fianl.push({polution:'NO2',type:'PSFC',value:data.NO2.PSFC})

      fianl.push({polution:'CO',type:'U',value:data.CO.U})
      fianl.push({polution:'CO',type:'V',value:data.CO.V})
      fianl.push({polution:'CO',type:'TEMP',value:data.CO.TEMP})
      fianl.push({polution:'CO',type:'RH',value:data.CO.RH})
      fianl.push({polution:'CO',type:'PSFC',value:data.CO.PSFC})

      fianl.push({polution:'O3',type:'U',value:data.O3.U})
      fianl.push({polution:'O3',type:'V',value:data.O3.V})
      fianl.push({polution:'O3',type:'TEMP',value:data.O3.TEMP})
      fianl.push({polution:'O3',type:'RH',value:data.O3.RH})
      fianl.push({polution:'O3',type:'PSFC',value:data.O3.PSFC})




      registerInteraction('other',{
          start:[{trigger:'element:mouseenter',action:'element-highlight-by-color:highlight'}

          ],
        end: [{ trigger: 'element:mouseleave', action: 'element-highlight-by-color:reset' }],


      })


      const chart = new Chart({
        container: 'coef',
        autoFit: true,
        height:175

      });
      chart.axis(false)
      const view = chart.createView(
        {region:{
        start:{x:0.0,y:0.0},
        end:{x:0.4,y:1}
      }})
      view.data(fianl)
      view.scale({
        sales: {
          max: 2400,
          tickInterval: 600,
          nice: true,
        },
      });

      view.tooltip({
        showMarkers: false,
        showTitle:false
      });
      // view.legend({position:"left"})
      view
        .interval()
        .position('polution*value')
        .color('type')
        .adjust('stack');

      view.interaction('element-link');



      const DA = ['PM2','PM10','SO2','NO2','O3','CO','U','V','TEMP','RH','PSFC']
      var links=[]
      fianl.forEach((d)=>{

        let source = DA.indexOf(d.polution)
        let target = DA.indexOf(d.type)
        let value = d.value
        links.push({source:source,target:target,value:value})
      })

      const DATA ={
        nodes:[
          {name:'PM2'},
          {name:'PM10'},
          {name:'SO2'},
          {name:'NO'},
          {name:'O3'},
          {name:'CO'},
          {name:'U'},
          {name:'V'},
          {name:'TEMP'},
          {name:'RH'},
          // {name:'RH'},
          {name:'PSFC'}
        ],
        links:links

      }


      const ds = new DataSet();
      const dv = ds.createView().source(DATA, {
        type: 'graph',
        edges: (d) => d.links,
      });

      dv.transform({
        type: 'diagram.sankey',
        nodeWidth: 0.008,
        nodePadding: 0.03,
        sort: (a, b) => {
          if (a.value > b.value) {
            return 0;
          } else if (a.value < b.value) {
            return -1;
          }
          return 0;
        },
      });

      const edges = dv.edges.map((edge) => {
        return {
          source: edge.source.name,
          target: edge.target.name,
          name: edge.source.name,
          x: edge.x,
          y: edge.y,
          value: edge.value,
        };
      });

      const nodes = dv.nodes.map((node) => {
        return {
          x: node.x,
          y: node.y,
          name: node.name,
        };
      });

      const nodeView = chart.createView({
        region:{
          start:{
            x:0.5,
            y:0.0
          },
          end:{
            x:0.8,
            y:1
          }
        }
      });
      nodeView.data(nodes);
      nodeView
        .polygon()
        .position('x*y') // nodes数据的x、y由layout方法计算得出
        .color('name')
        .label('x*name', (x, name) => {
          const isLast = x[1] === 1;
          return {
            style: {
              fill: 'black',
              textAlign: isLast ? 'end' : 'start',
              opacity:1
            },
            offsetX: isLast ? -8 : 8,
            content: name,
          };
        })
        // .tooltip(false)


// edge view
      const edgeView = chart.createView({
        region:{
          start:{
            x:0.5,
            y:0.0
          },
          end:{
            x:1,
            y:1
          }
        },
        // legend:'false'
      });
      edgeView.data(edges);


      edgeView
        .edge()
        .position('x*y')
        .shape('arc')
        .color('name')
        .tooltip('target*source*value', (target, source, value) => {

          return {
            name: source + ' to ' + target,
            value,
          };
        })
        .style('source*target', (source, target) => {
          return {
            opacity: 0.5,
            lineWidth: 0,
          };
        })
        .state({
          active: {
            style: {
              opacity: 1,
              lineWidth: 0,
            },
          },
        });

      edgeView.tooltip({
        showTitle:false,
        showMarkers:false
      })
      nodeView.tooltip({
        showTitle:false,
        showMarkers:false
      })

      edgeView.tooltip({
        showTitle:true
      })
      edgeView.interaction('other')
      chart.interaction('element-active');
      chart.tooltip({
        showTitle:false
      })
      // edgeView.legend(false)
      this.view=view;
      this.chart=chart;
      // chart.legend(false)
      view.legend(true)
      chart.render();
    })
  }
}
</script>

<style scoped>

</style>
