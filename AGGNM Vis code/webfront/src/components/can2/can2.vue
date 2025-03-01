<template>
  <div style="height: 100%; width: 100%">
    <div style="background-color:#A8A8A8; font-size: 10px; text-align:center"><b>Pockets residue correlation plot</b></div>
    <div id="can2" style="height: 93%; width: 100%"></div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      echartsInstance: null,
      Resnodes: [], // 节点
      ResLinks: [], // 边
      Rescategories: [], // 目录
    }
  },
  mounted() {
    this.getResRGData()
  },
  unmounted() {
  },
  methods: {
    // ResRG获取数据
    getResRGData(){
      let selpocID = this.$store.state.pocChoice // 是否有选中的口袋,-1代表没有
      // 0 Rescategories
      this.Rescategories = []
      if(selpocID != -1){
        this.Rescategories.push({
          name: 'selected',
          itemStyle:{
            color: this.$store.state.selectColor
          }
        })
      }
      this.Rescategories.push({
        name: 'isAllo',
        itemStyle:{
          color: this.$store.state.alloColor
        }
      })
      this.Rescategories.push({
        name: 'noAllo',
        itemStyle:{
          color: this.$store.state.noAlloColor
        }
      })
      // 1 Resnodes
      this.Resnodes = []
      let pdbAtoms = this.$store.state.pocketAtoms[this.$store.state.pdbName]
      for(let pocketName in pdbAtoms){
        // 统计一个口袋内的残基
        let pocketID = parseInt(pocketName.substring(6,pocketName.length)) // 口袋编号，下标+1
        let pocketAtoms = pdbAtoms[pocketName] // 原子数组
        let pocketResSet = new Set() // 残基集合
        let pocketCategory = 0 // 默认为被选中的口袋
        let pocketRadis = 0 // 口袋半径
        let pocketColor = "000"
        // 判断pocketID是否在被选中的范围内
        if(this.ArrayHas(this.$store.state.can1SelAllo,pocketID-1)===false && this.ArrayHas(this.$store.state.can1SelnoAllo,pocketID-1)===false){
          continue; // 如果不在两个数组内，跳过
        }
        if(pocketID-1 === selpocID){
          pocketCategory = 0 //
          pocketColor = this.$store.state.selectColor
        }else{
          if(this.$store.state.pdbPoc[pocketID-1]['pred'] === 1){
            pocketCategory = 1
            if(this.Rescategories.length === 2){
              pocketCategory = 0
            }
            pocketColor = this.$store.state.alloColor
          }else{
            pocketCategory = 2
            if(this.Rescategories.length === 2){
              pocketCategory = 1
            }
            pocketColor = this.$store.state.noAlloColor
          }
        }
        for(let i=0;i<pocketAtoms.length;i++){
          let resVal = pocketAtoms[i]['resName'] + pocketAtoms[i]['resSeq'].toString()
          if(pocketResSet.has(resVal) === false){
            pocketResSet.add(resVal)
          }
        }
        pocketRadis = pocketResSet.size
        this.Resnodes.push({
          pocID:pocketID,
          id:pocketID,
          category:pocketCategory, // 口袋种类
          symbolSize:pocketRadis, // 口袋半径
          value:pocketName, // 口袋名称
          resSet:pocketResSet,
          resNum:pocketResSet.size, // 残基数量
          itemStyle: {
            color: pocketColor
          }
        })
      }
      // 2 ResLinks
      this.ResLinks = []
      for(let i=0;i<this.Resnodes.length;i++){
        for(let j=0;j<i;j++){
          // 计算set1与set2的交集
          const intersectionResult = [...new Set(Array.from(this.Resnodes[i].resSet).filter((value) => this.Resnodes[j].resSet.has(value)))];
          if(intersectionResult.length > 0){ // 有交集
            this.ResLinks.push({
              source:i,
              target:j,
              sourceID:this.Resnodes[i].id,
              targetID:this.Resnodes[j].id,
              resLS:intersectionResult
            })
          }
        }
      }
      this.showResRG() // 展示
    },
    ArrayHas(arr,pocID){ // 判断arr中是否有pocID
      for(let i=0;i<arr.length;i++){
        if(pocID === arr[i]){
          return true;
        }
      }
      return false;
    },
    // 展示力导向图
    showResRG() {
      let chartDom = document.getElementById("can2");
      this.echartsInstance = echarts.init(chartDom,null,{
        renderer: 'svg',
      });
      let option = {
        tooltip: {
          show: true,
          formatter: (params) => { // 这里要设置为箭头函数，不然this会指向出错
            if(params.dataType === "node"){
              let nodeid = params.dataIndex
              let ss = '<p style=\'text-align:left;\'>' + this.Resnodes[nodeid].value + '<br />' +
              'resNum:' + this.Resnodes[nodeid].resNum + '</p>'
              return ss
            }else if(params.dataType === "edge"){
              let edgeid = params.dataIndex
              let source = this.ResLinks[edgeid].sourceID
              let target = this.ResLinks[edgeid].targetID
              let comRes = this.ResLinks[edgeid].resLS.join(',');
              let ss = '<p style=\'text-align:left;\'>source: ' + (source) + '<br />' +
              'target: ' + target + '<br />' +
              'comRes: ' + comRes + '</p>'
              return ss
            }
          }
        },
        legend: [
          {
            top: 1,
            itemGap: 20,
            data: this.Rescategories
          }
        ],
        series: [
          {
            type: 'graph',
            layout: 'force',
            data: this.Resnodes,
            links: this.ResLinks,
            categories: this.Rescategories,
            roam: true,
            label: {
              show: true,
              position: 'top',
              distance: 2,
              formatter:(params)=>{
                let dataIndex = params['data']['pocID']
                let fg = -1
                let can1AlloArr = this.$store.state.can1ShowTextAllo
                let can1noAlloArr = this.$store.state.can1ShowTextnoAllo
                for(let i=0;i<can1AlloArr.length;i++){
                  if(dataIndex === (can1AlloArr[i]+1)){
                    fg = 1
                    break
                  }
                }
                for(let i=0;i<can1noAlloArr.length;i++){
                  if(dataIndex === (can1noAlloArr[i]+1)){
                    fg = 1
                    break
                  }
                }
                if(fg === 1){ // 如果在对应区域，返回标记
                  return dataIndex.toString()
                }
                return ""
              },
              // fontSize: 10,
              fontWeight: 'bold',
            },
            draggable: true,
            force: {
              edgeLength: [20,50],
              repulsion: 20,
              gravity: 0.2
            },
            emphasis: {
              focus: 'adjacency',
              lineStyle: {
                width: 10
              },
              itemStyle:{
                color: this.$store.state.can2MouseOverColor
              }
            },
          }
        ],
        color: this.$store.state.color_list,
      }
      this.echartsInstance.setOption(option);
      // 监听鼠标悬浮，移动鼠标会与can3联动
      this.echartsInstance.on('mouseover',(params)=>{
        if(params.dataType === 'node'){
          this.$store.commit('changecan2Seledge',[-1,-1])
          this.$store.commit('changecan2Selnode',params.data['pocID'])
        }else if(params.dataType === 'edge'){
          this.$store.commit('changecan2Selnode',-1)
          this.$store.commit('changecan2Seledge',[ params.data['sourceID'],params.data['targetID'] ])
        }
      })
      // 点击取消can3效果
      this.echartsInstance.on('click',(params)=>{
        if(params.componentSubType === "graph"){
          this.$store.commit('changecan2Selnode',-1)
          this.$store.commit('changecan2Seledge',[-1,-1])
        }
      })
    }
  },
}
</script>

<style>

</style>