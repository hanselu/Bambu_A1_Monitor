### 启动时，填入打印机相关参数
- 用户名：固定为 `bblp`
- 访问码：在打印机设置里找
- 序列号：在打印机设置或者BambuStudio可找到
- IP：打印机的IP，在打印机设置里可找到
- 端口：固定为 `8883`

修改后的参数会自动保存至 `config.json`

### 归档
pywin32_monitor目录下的是利用win32 api抓取BambuStudio信息，需要在后台挂着BambuStudio。
自从换了MQTT以后，不再需要使用这种方法了，代码仅做归档。