// 设置响应头的中间件
module.exports = async (ctx,next) => {
  const contextType = 'charset=utf-8'
  ctx.set('Content-Type', contextType)
  // 解决跨域
  ctx.set("Access-Control-Allow-Origin","*")
  ctx.set("Access-Control-Allow-Methods", "OPTIONS, GET, PUT, POST, DELETE")
  await next()
}