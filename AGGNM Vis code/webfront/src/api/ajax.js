//导入axios
import axios from 'axios'
import { PORT } from '@/api/port.js'
//使用axios下面的create([config])方法创建axios实例，其中config参数为axios最基本的配置信息。
const API = axios.create({
	baseURL: 'http://localhost:' + PORT, //请求后端数据的基本地址，自定义8888
	timeout: 200000                   //请求超时设置，单位ms
})

export default API