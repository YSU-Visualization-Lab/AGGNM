<template>
  <div style="height: 100%; width: 100%">
    <div style="background-color:#A8A8A8; font-size: 10px; text-align:center"><b>Pockets atomic correlation plot</b></div>
    <div id="can3" style="height: 94%; width: 100%"></div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      echartsInstance: null,
      Atomsnodes: [],
      Atomslinks: [],
      Atomscategories: [],
    }
  },
  mounted() {
    this.getAtomsRGData()
  },
  unmounted() {
  },
  methods: {
    getAtomsRGData() {
      let selpocID = this.$store.state.pocChoice
      // 0 原子目录
      this.Atomscategories = []
      if(selpocID != -1){
        this.Atomscategories.push({
          name:'selected',
          itemStyle:{
            color: this.$store.state.selectColor
          }
        })
      }
      this.Atomscategories.push({
        name:'isAllo',
        itemStyle:{
          color: this.$store.state.alloColor
        }
      })
      this.Atomscategories.push({
        name:'noAllo',
        itemStyle:{
          color: this.$store.state.noAlloColor
        }
      })
      // 1 原子口袋节点
      this.Atomsnodes = []
      let pdbAtoms = this.$store.state.pocketAtoms[this.$store.state.pdbName]
      for(let pocketName in pdbAtoms){
        // 统计一个口袋内的原子
        let pocketID = parseInt(pocketName.substring(6,pocketName.length)) // 口袋编号，下标+1
        let pocketAtoms = pdbAtoms[pocketName] // 原子数组
        let pocketAtomsArr = [] // 原子集合
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
            if(this.Atomscategories.length === 2){
              pocketCategory = 0
            }
            pocketColor = this.$store.state.alloColor
          }else{
            pocketCategory = 2
            if(this.Atomscategories.length === 2){
              pocketCategory = 1
            }
            pocketColor = this.$store.state.noAlloColor
          }
        }
        for(let i=0;i<pocketAtoms.length;i++){
          pocketAtomsArr.push({
            atomId:pocketAtoms[i].atomId,
            x:pocketAtoms[i].x,
            y:pocketAtoms[i].y,
            z:pocketAtoms[i].z,
          })
        }
        pocketRadis = pocketAtomsArr.length/2.5
        if(pocketID === this.$store.state.can2Selnode){
          this.Atomsnodes.push({
            pocID:pocketID,
            id:pocketID,
            category:pocketCategory, // 口袋种类
            symbolSize:pocketRadis, // 口袋半径
            value:pocketName, // 口袋名称
            pocketAtomsArr:pocketAtomsArr, // 口袋原子数组
            itemStyle:{
              color: this.$store.state.can2MouseOverColor
            }
          })
        }else{
          this.Atomsnodes.push({
            pocID:pocketID,
            id:pocketID,
            category:pocketCategory, // 口袋种类
            symbolSize:pocketRadis, // 口袋半径
            value:pocketName, // 口袋名称
            pocketAtomsArr:pocketAtomsArr, // 口袋原子数组
            itemStyle: {
              color: pocketColor
            }
          })
        }
      }
      // 2 原子口袋边
      this.Atomslinks = []
      for(let i=0;i<this.Atomsnodes.length;i++){
        for(let j=0;j<i;j++){
          let tpDis = this.calcAtomsDis(this.Atomsnodes[i]['pocketAtomsArr'],this.Atomsnodes[j]['pocketAtomsArr'])
          if(tpDis != -1 && tpDis <= 0){
            // 获取相同原子
            let comAtoms = this.calcComAtoms(this.Atomsnodes[i]['pocketAtomsArr'],this.Atomsnodes[j]['pocketAtomsArr'])
            let node1 = this.$store.state.can2Seledge[0]
            let node2 = this.$store.state.can2Seledge[1]
            if((this.Atomsnodes[i].id === node1 && this.Atomsnodes[j].id === node2) || 
            (this.Atomsnodes[j].id === node1 && this.Atomsnodes[i].id === node2)){
              this.Atomslinks.push({
                source:i,
                target:j,
                sourceID:this.Atomsnodes[i].id,
                targetID:this.Atomsnodes[j].id,
                dis:tpDis, // 口袋之间的距离
                comAtoms:comAtoms,
                lineStyle:{
                  width: 10
                }
              })  
            }else{
              this.Atomslinks.push({
                source:i,
                target:j,
                sourceID:this.Atomsnodes[i].id,
                targetID:this.Atomsnodes[j].id,
                dis:tpDis, // 口袋之间的距离
                comAtoms:comAtoms
              })
            }
          }
        }
      }
      this.showAtomsRG()
    },
    ArrayHas(arr,pocID){ // 判断arr中是否有pocID
      for(let i=0;i<arr.length;i++){
        if(pocID === arr[i]){
          return true;
        }
      }
      return false;
    },
    calcAtomsDis(arr1,arr2){
      // 计算两个口袋的距离
      let datoms = -1
      for(let i=0;i<arr1.length;i++){
        for(let j=0;j<arr2.length;j++){
          let tpd = (arr1[i].x - arr2[j].x)**2 + (arr1[i].y - arr2[j].y)**2 + (arr1[i].z - arr2[j].z)**2
          if(datoms === -1) datoms = tpd
          else datoms = Math.min(datoms,tpd)
        }
      }
      return datoms
    },
    calcComAtoms(arr1,arr2){
      // 计算两个口袋的相同原子
      let comArr = []
      for(let i=0;i<arr1.length;i++){
        for(let j=0;j<arr2.length;j++){
          if(arr1[i].atomId === arr2[j].atomId){
            comArr.push(arr1[i].atomId)
            break
          }
        }
      }
      return comArr
    },
    // AtomsRG画图
    showAtomsRG() {
      let chartDom = document.getElementById("can3");
      this.echartsInstance = echarts.init(chartDom,null,{
        renderer: 'svg',
      });
      let option = {
        tooltip: {
          show: true,
          formatter: (params) => { 
            if(params.dataType === "node"){
              let nodeid = params.dataIndex
              let atomNums = this.Atomsnodes[nodeid].pocketAtomsArr.length
              let ss = '<p style=\'text-align:left;\'>' + this.Atomsnodes[nodeid].value + '<br />'+
              'atomNums: ' + atomNums + '</p>'
              return ss
            }else if(params.dataType === "edge"){
              let edgeid = params.dataIndex
              let source = this.Atomslinks[edgeid].sourceID
              let target = this.Atomslinks[edgeid].targetID
              // let AtomsDis = this.AtomsRGData.Atomslinks[edgeid].dis.toFixed(3);
              let comAtoms = this.Atomslinks[edgeid].comAtoms.length
              let ss = '<p style=\'text-align:left;\'>source: ' + source + '<br />' +
              'target: ' + target + '<br />' +
              'comAtoms: ' + comAtoms + '</p>'
              return ss
            }
          }
        },
        legend: [
          {
            top: 1,
            itemGap: 20,
            data: this.Atomscategories
          }
        ],
        animationDurationUpdate: 1500,
        animationEasingUpdate: 'quinticInOut',
        series: [
          {
            type: 'graph',
            layout: 'circular',
            circular: {
              rotateLabel: true
            },
            data: this.Atomsnodes,
            links: this.Atomslinks,
            categories: this.Atomscategories,
            draggable: true,
            roam: true,
            label: {
              show: true,
              distance: 2,
              position: 'top',
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
              fontWeight: 'bold',
            },
            lineStyle: {
              curveness: 0.3
            },
            emphasis: {
              lineStyle: {
                width: 10
              },
            },
          }
        ],
        color: this.$store.state.color_list,
      }
      this.echartsInstance.setOption(option);
    },
  },
}
</script>

<style>

</style>