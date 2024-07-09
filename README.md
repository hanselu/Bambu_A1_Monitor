使用前先手动建立config.json，按以下格式填入连接信息

```json
{
  "username": "bblp",
  "lan_code": "打印机局域网连接码",
  "sn": "打印机sn",
  "ip": "打印机IP",
  "port": 8883
}
```

pywin32_monitor目录下的是利用win32 api抓取BambuStudio信息，需要在后台挂着BambuStudio。
自从换了MQTT以后，不再需要使用这种方法了，代码仅做归档。