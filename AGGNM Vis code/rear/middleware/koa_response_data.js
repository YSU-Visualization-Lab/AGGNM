// 处理业务逻辑的中间件，读取某个json文件
const path = require('path')
const fileUtils = require('../utils/file_utils')
const urlDeal = require('url')
module.exports = async (ctx, next) => {
  // 根据url
  const url = ctx.request.url
  // console.log('ctx.request = ',ctx.request)
  let filePath = url.replace('/api','')
  // filePath = '../data' + filePath + '.json'
  // filePath = path.join(__dirname, filePath)
  let pocPath = __dirname + '/../data' + filePath // 返回对应的文件
  // console.log('pocPath = ',pocPath)
  // console.log('__dirname = ',__dirname)
  console.log('url = ',url,'pocPath = ',pocPath)
  
  try {
    // const ret = await fileUtils.getFileJsonData(filePath)
    // ctx.response.body = ret
    // 读取pdb文件
    const ret = await fileUtils.getFileJsonData(pocPath)
    ctx.response.body = ret
  } catch(error) {
    const errorMsg = {
      message: '读取文件内容失败，文件资源不存在',
      status: 404
    }
    ctx.response.body = JSON.stringify(errorMsg)
  }
  
  // console.log(filePath)
  await next()
}