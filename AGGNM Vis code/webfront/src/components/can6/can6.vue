<template>
  <div style="height: 100%; width: 100%">
    <div style="background-color:#A8A8A8; font-size: 10px; text-align:center"><b>Pocket sequence distance plot</b></div>
    <table style="width: 100%;height: 15px; border-bottom: 2px solid #ccc; border-collapse: collapse;">
      <tr>
        <td style="border-right: 2px solid #ccc;">
          <span style="font-size: 12px; font-weight: bold; text-align:center;">First pocket: </span>
        </td>
        <td style="border-right: 2px solid #ccc;">
          <select
            v-model="poc1"
            @change="changePoc1"
          >
            <option 
              v-for="item in pdbpoc_list"
              :key="item.id"
              :label="item.id"
              :value="item.id"
            />
          </select>
        </td>
        <td style="border-right: 2px solid #ccc;">
          <span style="font-size: 12px; font-weight: bold; text-align:center;">Second pocket: </span>
        </td>
        <td style="border-right: 2px solid #ccc;">
          <select
            v-model="poc2"
            @change="changePoc2"
          >
            <option 
              v-for="item in pdbpoc_list"
              :key="item.id"
              :label="item.id"
              :value="item.id"
            />
          </select>
        </td>
      </tr>
    </table>
    <div id="can6" style="height: 93%; width: 100%"></div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      echartsInstance: null,
      poc1: 1,
      poc2: 2,
      pdbpoc_list: [], // 口袋列表
      pocDisLS: [], // 口袋距离
      poccategories: [], // 口袋距离目录
      markLineData: [], // 最小值，平均值，最大值
      // 热力图相关
      xData:[], // 横轴数据
      yData:[], // 纵轴数据
      heatMapData:[], // 热力图数据，[posy,posx,value]
      heatMapDataShow: [], // 热力图数据是否打标记
    }
  },
  mounted() {
    this.poc1 = 1
    this.poc2 = 2
    this.pdbpoc_list = []
    let pdbposTSNE = this.$store.state.posTSNE[this.$store.state.pdbName]
    for(let i=0;i<pdbposTSNE.length;i++){
      this.pdbpoc_list.push({
        id: i+1,
      })
    }
    this.calcHeatMapData()
  },
  unmounted() {
  },
  methods: {
    changePoc1(){
      this.calcHeatMapData()
    },
    changePoc2(){
      this.calcHeatMapData()
    },
    // 计算差值数据
    calcData(){
      let pdbposTSNE = this.$store.state.posTSNE[this.$store.state.pdbName]
      let poc1ZXLS = pdbposTSNE[this.poc1 - 1]['pocZXnorm']
      let poc2ZXLS = pdbposTSNE[this.poc2 - 1]['pocZXnorm']
      this.pocDisLS = []
      this.poccategories = []
      let mxDis = -1,miDis = -1,aveDis = 0
      for(let i=0;i<poc1ZXLS.length;i++){
        let pocdis = Math.sqrt((poc1ZXLS[i][0] - poc2ZXLS[i][0])**2 +
        (poc1ZXLS[i][1] - poc2ZXLS[i][1])**2 +
        (poc1ZXLS[i][2] - poc2ZXLS[i][2])**2)
        this.pocDisLS.push(pocdis.toFixed(3))
        this.poccategories.push({
          name: "cen" + (i+1).toString()
        })
        aveDis += pocdis
        if(mxDis === -1) mxDis = pocdis
        else mxDis = Math.max(mxDis,pocdis)
        if(miDis === -1) miDis = pocdis
        else miDis = Math.min(miDis,pocdis)
      }
      aveDis = (aveDis/poc1ZXLS.length).toFixed(3)
      miDis = miDis.toFixed(3)
      mxDis = mxDis.toFixed(3)
      this.markLineData = []
      this.markLineData.push({
        label:{
          formatter:'{b}',
          position: 'insideStartTop',
        },
        name: 'minVal',
        yAxis:miDis
      })
      this.markLineData.push({
        label:{
          formatter:'{b}',
          position: 'insideMiddleTop',
        },
        name: 'average',
        yAxis:aveDis
      })
      this.markLineData.push({
        label:{
          formatter:'{b}',
          position: 'insideEndTop',
        },
        name: 'mxDis',
        yAxis:mxDis
      })
      this.showChart()
    },
    // 更新图表
    showChart(){
      let chartDom = document.getElementById("can6");
      this.echartsInstance = echarts.init(chartDom,null,{
        renderer: 'svg',
      });
      let option = {
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: this.poccategories.map((e)=>{
            return e.name
          })
        },
        yAxis: {
          type: 'value',
        },
        tooltip: {
          trigger: 'axis',
        },
        grid: {
          left: '10%',
          right: '6%',
          top: '10%',
          bottom: '14%',
        },
        dataZoom: [
          {
            type: 'inside',
            show: true,
            realtime: true,
            showDetail: true
          }
        ],
        series: [
          {
            data: this.pocDisLS,
            type: 'line',
            areaStyle: {},
            markLine: {
              data: this.markLineData,// 计算三条线，平均值，最小值，最大值
              label: {
                distance: [20, 8]
              }
            }
          }
        ],
        color: this.$store.state.color_list,
      };
      this.echartsInstance.setOption(option);
    },
    // 计算热力图的数据
    calcHeatMapData(){
      let pdbposTSNE = this.$store.state.posTSNE[this.$store.state.pdbName]
      let poc1ZXLS = pdbposTSNE[this.poc1 - 1]['pocZXnorm']
      let poc2ZXLS = pdbposTSNE[this.poc2 - 1]['pocZXnorm']
      // 1 ydata
      this.yData = []
      for(let i=0;i<poc1ZXLS.length;i++){
        this.yData.push(i+1)
      }
      // 2 xdata
      this.xData = []
      for(let i=0;i<poc2ZXLS.length;i++){
        this.xData.push(i+1)
      }
      // 3 heatMapData
      this.heatMapData = []
      this.heatMapDataShow = []
      for(let i=0;i<poc1ZXLS.length;i++){
        for(let j=0;j<poc2ZXLS.length;j++){
          let pocdis = Math.sqrt((poc1ZXLS[i][0] - poc2ZXLS[j][0])**2 +
          (poc1ZXLS[i][1] - poc2ZXLS[j][1])**2 +
          (poc1ZXLS[i][2] - poc2ZXLS[j][2])**2)
          this.heatMapData.push([
            i,
            j,
            pocdis
          ])
          this.heatMapDataShow.push(-1)
        }
      }
      this.showHeatMap()
    },
    // 展示热力图
    showHeatMap(){
      let chartDom = document.getElementById("can6");
      this.echartsInstance = echarts.init(chartDom,null,{
        renderer: 'svg',
      });
      let option = {
        tooltip: {
          position: 'top',
          formatter: (params) => { // 这里要设置为箭头函数，不然this会指向出错
            let poc1Cen = this.yData[ params.data[0] ]
            let poc2Cen = this.xData[ params.data[1] ]
            let cenDis = params.data[2]
            let ss = '<p style=\'text-align:left;\'>' +
            'poc' + this.poc1 + '-' + poc1Cen + ',poc' + this.poc2 + '-' + poc2Cen + '<br />' +
            'Dis: ' + cenDis.toFixed(3) + '<br />'
            return ss
          }
        },
        grid: {
          // height: '75%',
          top: '10%',
          right: '16%',
          left: '8%',
          bottom: '15%',
        },
        xAxis: {
          name: 'pocket'+this.poc2,
          nameLocation: 'end',
          nameGap: 10,
          type: 'category',
          data: this.xData,
          splitArea: {
            show: true
          }
        },
        yAxis: {
          name: 'pocket'+this.poc1,
          nameLocation: 'end',
          nameGap: 10,
          type: 'category',
          data: this.yData,
          splitArea: {
            show: true
          }
        },
        visualMap: {
          min: 0,
          max: 2,
          calculable: true,
          itemHeight: 180,
          orient: 'vertical',
          right: '0%',
          bottom: '18%',
          textStyle:{
            fontSize: 10,
          },
          formatter: function (value) {
            return value.toFixed(3); // 范围标签显示内容。
          },
          padding: 3,
          range: this.ShowRange(),
        },
        gradientColor: this.$store.state.heatMap_col,
        series: [
          {
            type: 'heatmap',
            coordinateSystem: 'cartesian2d',
            data: this.heatMapData,
            label: {
              show: true,
              formatter:(params)=>{
                let dataIndex = params.dataIndex // ID
                if(this.heatMapDataShow[dataIndex] === -1){
                  return ""
                }else{
                  return (this.heatMapDataShow[dataIndex]+1).toString()
                }
              }
            },
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowColor: 'rgba(0, 0, 0, 0.5)',
              }
            },
          }
        ],
      };
      this.echartsInstance.setOption(option);
      this.linstenChart()
    },
    // 计算展示范围
    ShowRange(){
      return [0,0.25]// 修改这里的值用于对应
    },
    linstenChart () {
      // 监听范围变化
      this.echartsInstance.on('datarangeselected', (params) => { // 这里要用箭头函数,不然this不能用
        let dataRange = params.selected // 记录被选中的范围
        let selData = [] // 被选中的坐标
        let orderLS = this.$store.state.orderLS // 0~7的全排列
        for(let i=0;i<this.heatMapData.length;i++){
          if(dataRange[0] <= this.heatMapData[i][2] && this.heatMapData[i][2] <= dataRange[1]){
            selData.push([
              this.heatMapData[i][0],
              this.heatMapData[i][1]
            ])
          }
        }
        let fg = false // 判断是否检测成功
        let ansXL = []
        for(let i=0;i<orderLS.length;i++){
          let cnt = 0
          for(let j=0;j<orderLS[i].length;j++){
            for(let k=0;k<selData.length;k++){
              if(j === selData[k][0] && orderLS[i][j] === selData[k][1]){
                cnt++;
                break
              }
            }
          }
          if(cnt === orderLS[i].length){
            fg = true
            for(let j=0;j<orderLS[i].length;j++){
              ansXL.push(orderLS[i][j])
            }
            break
          }
        }
        if(fg === true){ // 检测成功
          for(let i=0;i<this.heatMapDataShow.length;i++){
            this.heatMapDataShow[i] = -1
            for(let j=0;j<ansXL.length;j++){
              if(j === this.heatMapData[i][0] && ansXL[j] === this.heatMapData[i][1]){
                this.heatMapDataShow[i] = ansXL[j]
                break
              }
            }
          }
        }else{
          for(let i=0;i<this.heatMapDataShow.length;i++){
            this.heatMapDataShow[i] = -1 // 该为不显示
          }
        }
      })
    },
},
}
</script>

<style>

</style>