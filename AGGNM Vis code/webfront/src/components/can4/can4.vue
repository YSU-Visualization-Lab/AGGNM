<template>
  <div style="height: 100%; width: 100%">
    <div style="background-color:#A8A8A8; font-size: 10px; text-align:center"><b>Pocket features distribution plot</b></div>
    <table style="width: 100%; height: 15px; border-bottom: 2px solid #ccc; border-collapse: collapse;">
      <tr style="width: 100%;">
        <td style="width: 25%; font-size: 12px; font-weight: bold; border-right: 2px solid #ccc;">
          <span style="text-align: left;">Feature</span>
        </td>
        <td style="width: 24%; font-size: 12px; font-weight: bold; border-right: 2px solid #ccc;">
          <select
            v-model="now_fea"
            @change="getChartData"
          >
            <option 
              v-for="item in fea_ls"
              :key="item.text"
              :label="item.text"
              :value="item.text"
            />
          </select>
        </td>
        <td style="width: 25%; font-size: 12px; font-weight: bold; border-right: 2px solid #ccc;">
          <span style="text-align: left;">splitNum</span>
        </td>
        <td style="width: 24%; font-size: 12px; font-weight: bold;">
          <input 
            v-model="splitNum"
            type="number" 
            :min="5"
            :max="100" 
            :step="1"
            @change="getChartData"
          >
        </td>
      </tr>
    </table>
    <div id="can4" style="height: 96%; width: 100%"></div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      // echarts图表
      echartsInstance: null,
      splitNum: 10,
      fea_ls: [],
      now_fea: null,
      xdata: [],
      ydata: [],
    }
  },
  mounted() {
    this.fea_ls = this.$store.state.colNameInfo
    this.now_fea = this.fea_ls[0]['text']
    this.getChartData()
  },
  unmounted() {
  },
  methods: {
    // echarts初始化
    showChart() {
      let chartDom = document.getElementById("can4");
      this.echartsInstance = echarts.init(chartDom,null,{
        renderer: 'svg',
      });
      let option = {
        tooltip: {
          trigger: 'axis',
          formatter: (params, ticket, callback) => {
              let val = params[0].value
              let index = params[0].dataIndex
              let qujian = this.xdata[index].valname
              let vshow = '<p style=\'text-align:left;\'>Feature Range:<br /><font color=\'red\'>' + qujian + '</font><br />AlloPoc Num：<br /><font color=\'red\'>' + val.toString() + '</font></p>'
              return vshow;
          },
          valueFormatter: (value) => {
            return value.toString()
          },
        },
        dataZoom: [
          {
            type: 'inside',
            show: true,
            realtime: true,
            showDetail: true
          }
        ],
        xAxis: {
          type: "category",
          data: this.xdata,
          nameGap: 5,
          name: 'Range',
        },
        grid: {
            left: '8%',
            right: '10%',
            top: '10%',
            bottom: '18%',
        },
        yAxis: {
          type: "value",
          axisLabel: {
            formatter: '{value}' // 纵坐标加上%
          },
          nameGap: 10,
          name: 'Number',
        },
        color: this.$store.state.color_list,
        series: [
          {
            name: "变构口袋数量",
            type: "bar",
            data: this.ydata,
            smooth: true,
            symbol: "none",
            stack: "a",
            areaStyle: {
              normal: {},
            },
          },
        ],
      };
      this.echartsInstance.setOption(option);
    },
    // 更新图表数据
    getChartData() {
      let splitNum = this.splitNum
      let now_fea = ""
      for(let i=0;i<this.fea_ls.length;i++){ // 映射值
        if(this.now_fea === this.fea_ls[i]['text']){
          now_fea = this.fea_ls[i]['name']
          break
        }
      }
      // 根据splitNum的值分割统计数据
      let n = this.$store.state.data_train.length
      this.xdata = []
      this.ydata = []
      let mival = 0
      let mxval = 0
      let alloid_list = []
      for(let i=0;i<n;i++)
      {
        if(this.$store.state.data_train[i]['tag'] === 1)
        {
          alloid_list.push(i)
        }
      }
      for(let i=0;i<alloid_list.length;i++)
      {
        let id = alloid_list[i]
        if(i === 0)
        {
          mival = this.$store.state.data_train[id][now_fea]
          mxval = this.$store.state.data_train[id][now_fea]
        }
        else
        {
          mival = Math.min(mival,this.$store.state.data_train[id][now_fea])
          mxval = Math.max(mxval,this.$store.state.data_train[id][now_fea])
        }
      }
      let splitR = []
      let cntArr = []
      let dval = (mxval - mival)/splitNum
      let lval = mival
      let rval = mival
      for(let i=0;i<splitNum;i++)
      {
        if(i === splitNum - 1) {
          rval = mxval + 10;
        }else{
          rval += dval
        }
        if(i === 0) splitR.push([lval-10,rval])
        else splitR.push([lval,rval])
        this.xdata.push({
          value:(lval + dval/2.0).toFixed(2),
          valname: '[' + lval.toFixed(2).toString() + " , " + rval.toFixed(2).toString() + ']',
        }) // 平均数,保留两位小数，更新x值数组
        cntArr.push(0)
        lval = rval
      }
      for(let i=0;i<alloid_list.length;i++)
      {
        let id = alloid_list[i]
        for(let j=0;j<splitNum;j++)
        {
          if(splitR[j][0] <= this.$store.state.data_train[id][now_fea] && this.$store.state.data_train[id][now_fea] < splitR[j][1])
          {
            cntArr[j] += 1
            break;
          }
        }
      }
      this.ydata = JSON.parse(JSON.stringify(cntArr)) // 更新y值数组
      this.showChart()
    },
  },
}
</script>

<style>

</style>