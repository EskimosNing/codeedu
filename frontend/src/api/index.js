// axios.js
import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://192.168.192.144:5000', // API基础路径
  timeout: 100000, // 请求超时时间
});

export default instance;