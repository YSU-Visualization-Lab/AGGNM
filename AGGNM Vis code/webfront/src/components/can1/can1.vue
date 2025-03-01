<template>
  <div style="height: 100%; width: 100%">
    <div style="background-color:#A8A8A8; font-size: 10px; text-align:center"><b>Pockets distance scatter plot</b></div>
    <table style="width: 100%; height: 15px; border-bottom: 2px solid #ccc; border-collapse: collapse;">
      <tr style="width: 100%;">
        <td style="width: 30%; font-size: 12px; font-weight: bold; border-right: 2px solid #ccc;">
          <span style="text-align: left;">pockets distance</span>
        </td>
        <td style="width: 10%; font-size: 12px; font-weight: bold; border-left: 2px solid #ccc;">
          <input
            v-model="pocketsDis"
            type="number"
            @change="changePocketsDis"
          />
        </td>
      </tr>
    </table>
    <div id="can1" style="height: 81%; width: 100%"></div>
  </div>
</template>

<script>
import icon1 from '@/assets/image/bz.png'
export default {
  data() {
    return {
      icon1URL: 'image://'+icon1,
      // echarts图表
      echartsInstance: null,
      pocketsDis: 10, // 变构口袋与非变构口袋之间的距离
      selAlloPockets: [], // 选中的变构口袋编号
      alloPocpos: [], // 变构口袋坐标
      selnoAPockets: [], // 选中的非变构口袋编号
      noAoPocpos: [], // 非变构口袋坐标
      noAlloPocketDisList: [], // 非变构口袋的口袋距离排序
    }
  },
  mounted() {
    this.initChart(); // 初始化图表
    this.changePocketsDis() // 更新数据+图表
  },
  unmounted() {
    
  },
  methods: {
    // 重置口袋间距离
    changePocketsDis(){
      let pocAtoms = this.$store.state.pocketAtoms[this.$store.state.pdbName] // 口袋原子数组
      let pocFeatures = this.$store.state.pdbPoc // 口袋特征数组
      let pocketsLen = this.$store.state.zxpos[this.$store.state.pdbName].length // 口袋数量
      let alloPocketIDList = [] // 记录变构口袋编号
      let posTSNE = this.$store.state.posTSNE[this.$store.state.pdbName]
      for(let i=0;i<pocketsLen;i++){ // 先找出所有的变构口袋
        if(pocFeatures[i]['pred'] === 1){
          alloPocketIDList.push(i)
        }
      }
      let noAlloPocketIDList = [] // 距离内的口袋编号
      let noAlloPocketDisList = [] // 距离记录
      for(let j=0;j<pocketsLen;j++){
        if(pocFeatures[j]['pred'] === 1){ // 跳过变构口袋
          continue
        }
        let fg = false
        let noPocketsDis = -1
        for(let i=0;i<alloPocketIDList.length;i++){
          let alloID = alloPocketIDList[i]
          let pocketsDis = this.calcPocketsDis(pocAtoms["pocket"+(alloID+1).toString()],pocAtoms["pocket"+(j+1).toString()])
          if(j != alloID && pocketsDis <= this.pocketsDis){
            if(noPocketsDis === -1){
              noPocketsDis = pocketsDis
            }else{
              noPocketsDis = Math.min(noPocketsDis,pocketsDis)
            }
            fg = true
            // break
          }
        }
        if(fg === true){
          noAlloPocketIDList.push(j)
          noAlloPocketDisList.push({
            pocID: j,
            pocDis: noPocketsDis
          })
        }
      }
      noAlloPocketDisList.sort((a,b)=>{
        if(a.noPocketsDis < b.noPocketsDis){ // 按照距离从小到大排序
          return -1
        }else if(a.noPocketsDis > b.noPocketsDis){
          return 1
        }else{
          return 0
        }
      })
      this.noAlloPocketDisList = []
      for(let i=0;i<noAlloPocketIDList.length;i++){
        let pocID = noAlloPocketIDList[i] // 口袋编号
        let pocDis = -1; // 与最近变构口袋之间的距离
        let pocRank = -1; // 口袋距离排名
        let nearestPoc = -1; // 最近的变构口袋
        for(let j=0,rk=0;j<noAlloPocketDisList.length;j++){
          if(j>0 && noAlloPocketDisList[j]['pocDis'] > noAlloPocketDisList[j-1]['pocDis']){
            rk++;
          }
          if(pocID === noAlloPocketDisList[j]['pocID']){
            pocDis = noAlloPocketDisList[j]['pocDis']
            pocRank = rk
            nearestPoc = this.GetNearestPocket(pocID,alloPocketIDList) // 返回最近的口袋编号
            break
          }
        }
        this.noAlloPocketDisList.push({
          pocID: pocID,
          pocDis: pocDis,
          pocRank: pocRank,
          nearestPoc: nearestPoc,
        })
      }
      this.selAlloPockets = alloPocketIDList
      this.selnoAPockets = noAlloPocketIDList
      this.$store.commit('changecan1SelAllo',alloPocketIDList)
      this.$store.commit('changecan1SelnoAllo',noAlloPocketIDList)
      // 制作图表数据
      this.alloPocpos = []
      for(let i=0;i<alloPocketIDList.length;i++){
        let alloID = alloPocketIDList[i]
        this.alloPocpos.push([
          posTSNE[alloID]['pocCenterTSNE'][0],
          posTSNE[alloID]['pocCenterTSNE'][1],
        ])
      }
      this.noAoPocpos = []
      for(let i=0;i<noAlloPocketIDList.length;i++){
        let noAoID = noAlloPocketIDList[i]
        this.noAoPocpos.push([
          posTSNE[noAoID]['pocCenterTSNE'][0],
          posTSNE[noAoID]['pocCenterTSNE'][1],
        ])
      }
      // 更新图表
      this.updateChart()
    },
    // 计算口袋之间的距离
    calcPocketsDis(arr1,arr2){
      let miDis = Math.sqrt((arr1[0].x-arr2[0].x)**2 +
      (arr1[0].y-arr2[0].y)**2 + 
      (arr1[0].z-arr2[0].z)**2)
      for(let i=0;i<arr1.length;i++){
        for(let j=0;j<arr2.length;j++){
          let tpDis = Math.sqrt((arr1[i].x-arr2[j].x)**2 +
          (arr1[i].y-arr2[j].y)**2 + 
          (arr1[i].z-arr2[j].z)**2)
          if(tpDis < miDis){
            miDis = tpDis
          }
        }
      }
      return miDis;
    },
    // 计算pocID与变构口袋列表中的最近的变构口袋ID是哪个
    GetNearestPocket(pocID,alloPocketArr){
      let pocAtoms = this.$store.state.pocketAtoms[this.$store.state.pdbName]
      let id = -1
      let miDis = -1
      let poc1 = pocAtoms["pocket"+(pocID+1).toString()]
      for(let i=0;i<alloPocketArr.length;i++){
        let poc2 = pocAtoms["pocket"+(alloPocketArr[i]+1).toString()]
        let pDis = this.calcPocketsDis(poc1,poc2)
        if(miDis === -1){
          miDis = pDis
          id = alloPocketArr[i]
        }else{
          if(pDis < miDis){
            miDis = pDis
            id = alloPocketArr[i]
          }
        }
        return id
      }
    },
    // echarts初始化
    initChart() {
      let chartDom = document.getElementById("can1");
      this.echartsInstance = echarts.init(chartDom,{
        renderer: 'svg',
      });
      let option = {
        brush: {
          toolbox: ['rect', 'polygon', 'clear'],
          xAxisIndex: 0
        },
        grid: {
					left: '9%',
					right: '8%',
					bottom: '13%',
          top: '15%'
				},
        toolbox: {
          show: true,
          top:0,
          feature: {
            dataZoom: {
            }
          },
        },
        color: this.$store.state.color_list,
        xAxis: {
          name: 'X',
          nameGap: 10,
        },
        yAxis: {
          name: 'Y',
          nameGap: 5,
        }
      };
      this.echartsInstance.setOption(option);
      this.linstenChart() // 监听图表事件
    },
    // 更新图表界面
    updateChart() {
      if(this.selAlloPockets.length === 0){
        alert("没有预测出变构变构口袋")
      }
      let option = {
        tooltip: {
          show: true,
          formatter: (params) => { // 这里要设置为箭头函数，不然this会指向出错
            let dataIndex = -1
            let x = -1,y = -1
            let seriesIndex = params.seriesIndex
            if(seriesIndex === 0){
              dataIndex = this.selAlloPockets[params.dataIndex]
              x = this.alloPocpos[params.dataIndex][0]
              y = this.alloPocpos[params.dataIndex][1]
            }else{
              dataIndex = this.selnoAPockets[params.dataIndex]
              x = this.noAoPocpos[params.dataIndex][0]
              y = this.noAoPocpos[params.dataIndex][1]
            }
            let ss = '<p style=\'text-align:left;\'>pocketId: ' + (dataIndex+1) + '<br />' +
            'position: [' + x.toFixed(3) + ',' + y.toFixed(3) + ']<br />'
            if(seriesIndex === 1){ // 非变构口袋要输出距离等信息
              ss += 'nearestPoc: ' + (this.noAlloPocketDisList[params.dataIndex]['nearestPoc']+1) + '<br />'
              ss += 'DisRank: ' + (this.noAlloPocketDisList[params.dataIndex]['pocRank']+1) + '<br />'
              ss += 'pocDis: ' + this.noAlloPocketDisList[params.dataIndex]['pocDis'].toFixed(3) + '<br />'
            }
            ss += 'isAllo: ' + (seriesIndex === 0 ? 'yes' : 'no') + '<br /></p>'
            return ss
          },
          position: ['50%', '50%'],
        },
        series: [
          {
            name:'allo',
            symbolSize: (val,params) => {
              let dataIndex = -1
              if(params.seriesIndex === 0){
                dataIndex = this.selAlloPockets[params.dataIndex]
              }else{
                dataIndex = this.selnoAPockets[params.dataIndex]
              }
              if(this.$store.state.pocChoice === dataIndex) // 被选中，形状变大
              {
                return 15
              }
              return 10
            },
            symbol: (val,params) => { // 形状决定是否是变构口袋
              let dataIndex = -1
              if(params.seriesIndex === 0){
                dataIndex = this.selAlloPockets[params.dataIndex]
              }else{
                dataIndex = this.selnoAPockets[params.dataIndex]
              }
              if(this.$store.state.pocChoice === dataIndex) // 被选中，变为创可贴形状
              {
                return this.icon1URL
              }
              return 'circle' // 不是变构,返回圆形
            },
            data: this.alloPocpos,
            type: 'scatter',
            itemStyle: {
              color: (e) => { // 颜色决定聚类类别
                return this.$store.state.alloColor
              }
            },
            label: {
              show: true,
              position: 'top',
              distance: 2,
              formatter:(params)=>{
                let dataIndex = -1
                if(params.seriesIndex === 0){
                  dataIndex = this.selAlloPockets[params.dataIndex]
                  let dataArr = this.$store.state.can1ShowTextAllo
                  let fg = -1
                  for(let i=0;i<dataArr.length;i++){
                    if(dataArr[i] === dataIndex){
                      fg = 1
                      break
                    }
                  }
                  if(fg === 1){
                    return (dataIndex + 1).toString()
                  }
                }else{
                  dataIndex = this.selnoAPockets[params.dataIndex]
                  let dataArr = this.$store.state.can1ShowTextnoAllo
                  let fg = -1
                  for(let i=0;i<dataArr.length;i++){
                    if(dataArr[i] === dataIndex){
                      fg = 1
                      break
                    }
                  }
                  if(fg === 1){
                    return (dataIndex + 1).toString()
                  }
                }
                return ""
              },
              fontSize: 10,
              fontWeight: 'bold',
            },
          },
          {
            name:'noAllo',
            symbolSize: (val,params) => {
              let dataIndex = -1
              if(params.seriesIndex === 0){
                dataIndex = this.selAlloPockets[params.dataIndex]
              }else{
                dataIndex = this.selnoAPockets[params.dataIndex]
              }
              if(this.$store.state.pocChoice === dataIndex) // 被选中，形状变大
              {
                return 15
              }
              return 10
            },
            symbol: (val,params) => { // 形状决定是否是变构口袋
              let dataIndex = -1
              if(params.seriesIndex === 0){
                dataIndex = this.selAlloPockets[params.dataIndex]
              }else{
                dataIndex = this.selnoAPockets[params.dataIndex]
              }
              if(this.$store.state.pocChoice === dataIndex) // 被选中，变为创可贴形状
              {
                return this.icon1URL
              }
              return 'circle' // 不是变构,返回圆形
            },
            data: this.noAoPocpos,
            type: 'scatter',
            itemStyle: {
              color: (e) => { 
                return this.$store.state.noAlloColor
              }
            },
            label: {
              show: true,
              position: 'top',
              distance: 2,
              formatter:(params)=>{
                let dataIndex = -1
                if(params.seriesIndex === 0){
                  dataIndex = this.selAlloPockets[params.dataIndex]
                  let dataArr = this.$store.state.can1ShowTextAllo
                  let fg = -1
                  for(let i=0;i<dataArr.length;i++){
                    if(dataArr[i] === dataIndex){
                      fg = 1
                      break
                    }
                  }
                  if(fg === 1){
                    return (dataIndex + 1).toString()
                  }
                }else{
                  dataIndex = this.selnoAPockets[params.dataIndex]
                  let dataArr = this.$store.state.can1ShowTextnoAllo
                  let fg = -1
                  for(let i=0;i<dataArr.length;i++){
                    if(dataArr[i] === dataIndex){
                      fg = 1
                      break
                    }
                  }
                  if(fg === 1){
                    return (dataIndex + 1).toString()
                  }
                }
                return ""
              },
              fontSize: 10,
              fontWeight: 'bold',
            },
          }
        ]
      };
      this.echartsInstance.setOption(option);
    },
    // 点击触发事件
    linstenChart () {
      // 单击节点，选中节点，
      this.echartsInstance.on('click', (params) => { // 这里要用箭头函数,不然this不能用
        // 合法的点
        if(
          params.componentType === 'series' &&
          (params.seriesIndex === 0 || params.seriesIndex === 1) &&
          params.seriesType === 'scatter'
        ) {
          let dataIndex = -1
          if(params.seriesIndex === 0){
            dataIndex = this.selAlloPockets[params.dataIndex]
          }else{
            dataIndex = this.selnoAPockets[params.dataIndex]
          }
          if(this.$store.state.pocChoice != dataIndex) // 切换节点，第一次点击
          {
            this.$store.commit('changePocChoice',dataIndex) // 修改当前口袋选中信息
            this.updateChart()
          }
          else // 两次点击，清空
          {
            this.$store.commit('changePocChoice',-1) // 修改当前口袋选中信息
            this.updateChart()
          }
        }
      })

      // 选中节点，显示编号
      this.echartsInstance.on('brushselected', (params) => { // 这里要用箭头函数,不然this不能用
        let selected = params['batch'][0]['selected']
        let series0 = selected[0]['dataIndex']
        let series1 = selected[1]['dataIndex']
        let seriesID0 = [] // allo口袋被选中的编号
        for(let i=0;i<series0.length;i++){
          seriesID0.push(this.selAlloPockets[ series0[i] ])
        }
        let seriesID1 = [] // noallo口袋被选中的编号
        for(let i=0;i<series1.length;i++){
          seriesID1.push(this.selnoAPockets[ series1[i] ])
        }
        this.$store.commit('changecan1ShowTextAllo',seriesID0)
        this.$store.commit('changecan1ShowTextnoAllo',seriesID1)
      })
    },
  },
}
</script>

<style>

</style>