<template>
  <div style="width: 100%;height: 100%;">
    <div style="background-color:#A8A8A8; font-size: 10px; text-align:center"><b>Pocket feature comparison plot</b></div>
    <table style="width: 100%; height: 15px; border-bottom: 2px solid #ccc; border-collapse: collapse;">
      <tr style="width: 100%; height: 20px;">
        <td style="width: 50%; font-size: 12px; font-weight: bold; border-right: 2px solid #ccc;">
          <span style="text-align: left;">Feature Select</span>
        </td>
        <td style="width: 50%; font-size: 12px; font-weight: bold; border-right: 2px solid #ccc;">
          <div class="can5-container">
            <div class="can5-item" v-for="item in fea_ls" :key="item.name" @change="getParallelData">
              <input type="checkbox" :value="item.name" v-model="selectedfea_ls">
              <label>{{ item.text }}</label>
            </div>
          </div>
        </td>
      </tr>
    </table>
    <div id="can5" style="width: 100%;height: 79%;"></div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      selectedfea_ls: [], // 选中的选项
      fea_ls: [],
      parallelData: [],
      parallelLegend: [],
      parallelAxisData: [],
    }
  },
  mounted() {
    this.fea_ls = this.$store.state.colNameInfo
    this.selectedfea_ls = []
    for(let i=0;i<10;i++){
      this.selectedfea_ls.push(this.fea_ls[i]['name'])
    }
    this.getParallelData()
  },
  unmounted() {
  },
  methods: {
    getParallelData() {
      // 0 收集数据 + 归一化处理数据
      let rawData = []
      for(let i=0;i<this.$store.state.pdbPoc.length;i++){
        let tpLS = []
        for(let j=0;j<this.selectedfea_ls.length;j++){
          tpLS.push(this.$store.state.pdbPoc[i][ this.selectedfea_ls[j] ])
        }
        rawData.push(tpLS)
      }
      rawData = this.normData(rawData) // 归一化
      // 1 数据：变构+非变构+选中的
      this.parallelData = []
      let isAlloPD = [],noAlloPD = [],selPD = []
      let isAlloIDList = [],noAlloIDList = [],selIDList = [] // 标记其在this.$store.state.pdbPoc的编号列表
      let selpocID = this.$store.state.pocChoice
      if(selpocID != -1){ // 有选中的
        let tpLS = []
        for(let j=0;j<rawData[0].length;j++){ // 选中的口袋
          tpLS.push(rawData[selpocID][j])
        }
        selPD.push(tpLS)
        selIDList.push(selpocID)
      }
      for(let i=0;i<rawData.length;i++){
        if(this.ArrayHas(this.$store.state.can1SelAllo,i)===false && this.ArrayHas(this.$store.state.can1SelnoAllo,i)===false){
          continue; // 如果不在两个数组内，跳过
        }
        if(this.$store.state.pdbPoc[i]['pred'] === 1 && selpocID != i){ // 变构口袋
          let tpLS = []
          for(let j=0;j<rawData[i].length;j++){
            tpLS.push(rawData[i][j])
          }
          isAlloPD.push(tpLS)
          isAlloIDList.push(i)
        }
        if(this.$store.state.pdbPoc[i]['pred'] === 0 && selpocID != i){ // 非变构口袋
          let tpLS = []
          for(let j=0;j<rawData[i].length;j++){
            tpLS.push(rawData[i][j])
          }
          noAlloPD.push(tpLS)
          noAlloIDList.push(i)
        }
      }
      // 2 提示框
      this.parallelLegend = []
      if(selpocID != -1){
        this.parallelLegend.push({
          name:'selected',
          itemStyle:{
            color: this.$store.state.selectColor
          }
        })
        this.parallelData.push({
          name:'selected',
          type: 'parallel',
          lineStyle: {
            normal: {
              width: 1,
              opacity: 0.5
            },
          },
          color: this.$store.state.selectColor,
          data: selPD, // 归一化
          idList: selIDList, // 对应到this.$store.state.pdbPoc的编号
        })
      }
      this.parallelData.push({
        name:'isAllo',
        type: 'parallel',
        lineStyle: {
          normal: {
            width: 1,
            opacity: 0.5
          },
        },
        color: this.$store.state.alloColor,
        data: isAlloPD,
        idList: isAlloIDList,
      })
      this.parallelData.push({
        name:'noAllo',
        type: 'parallel',
        lineStyle: {
          normal: {
            width: 1,
            opacity: 0.5
          },
        },
        color: this.$store.state.noAlloColor,
        data: noAlloPD,
        idList: noAlloIDList,
      })
      this.parallelLegend.push({
        name:'isAllo',
        itemStyle:{
          color: this.$store.state.alloColor
        }
      })
      this.parallelLegend.push({
        name:'noAllo',
        itemStyle:{
          color: this.$store.state.noAlloColor
        }
      })
      // 3 坐标列
      this.parallelAxisData = []
      for(let i=0;i<this.selectedfea_ls.length;i++){
        this.parallelAxisData.push({
          // 调整文字顺序
          name: this.NameToRank(this.selectedfea_ls[i]),
          dim: i,
          nameGap: 10,//改这里
          max: 1.0,
        })
      }
      // 展示parallel图
      this.showParallel()
    },
    normData(dt) {
      for(let j=0;j<dt[0].length;j++){
        let mx = dt[0][j]
        let mi = dt[0][j]
        for(let i=0;i<dt.length;i++){
          mx = Math.max(mx,dt[i][j])
          mi = Math.min(mi,dt[i][j])
        }
        for(let i=0;i<dt.length;i++){
          let tpVal = (dt[i][j] - mi)/(mx - mi)
          dt[i][j]= tpVal
        }
      }
      return dt
    },
    ArrayHas(arr,pocID){ // 判断arr中是否有pocID
      for(let i=0;i<arr.length;i++){
        if(pocID === arr[i]){
          return true;
        }
      }
      return false;
    },
    // Parallel画图
    showParallel(){
      if(this.echartsInstance != null){
        this.echartsInstance.clear()
        this.echartsInstance = null
      }
      let chartDom = document.getElementById("can5");
      this.echartsInstance = echarts.init(chartDom,null,{
        renderer: 'svg',
      });
      let option = {
        legend: {
          top: 1,
          data: this.parallelLegend,
          itemGap: 20
        },
        tooltip: {
          show: true,
          formatter: (params) => { // 这里要设置为箭头函数，不然this会指向出错
            let nowid = params.dataIndex
            let copid = params.componentIndex
            let realid = this.parallelData[copid].idList[nowid]
            let ss = '<p style=\'text-align:left;\'>pocketId: ' + (realid+1) + '<br />'
            for(let i=0;i<this.selectedfea_ls.length;i++){
              ss += (this.NameToText(this.selectedfea_ls[i]) + ": " +
              this.$store.state.pdbPoc[realid][this.selectedfea_ls[i]].toFixed(3) + '<br />'
              )
            }
            ss += ('isAllo: ' + (this.$store.state.pdbPoc[realid]['pred'] === 1 ? 'yes' : 'no') + '<br /></p>')
            return ss
          }
        },
        brush: {
          toolbox: ['rect', 'clear'],
          xAxisIndex: 0
        },
        parallelAxis: this.parallelAxisData,
        parallel: {
          // left: '5%',
          right: '7%',
          left: '5%',
          bottom: '5%',
          top: '18%',
        },
        series: this.parallelData,
        // color: this.$store.state.color_list,
      };
      this.echartsInstance.setOption(option);
    },
    NameToRank(val){
      for(let i=0;i<this.fea_ls.length;i++){
        if(this.fea_ls[i]['name'] === val){
          return this.fea_ls[i]['rank']
        }
      }
    },
    NameToText(val){
      for(let i=0;i<this.fea_ls.length;i++){
        if(this.fea_ls[i]['name'] === val){
          return this.fea_ls[i]['text']
        }
      }
    },
  }
}
</script>

<style scoped>
.can5-container {
  text-align:left;
  margin-left: 15px;
  height: 48px;
  overflow-y: auto;
}

.can5-item {
  height: 15px;
}
</style>