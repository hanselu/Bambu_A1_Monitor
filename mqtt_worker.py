import json
from PySide6.QtCore import QThread, Signal, QObject
import paho.mqtt.client as mqtt
import mqtt_commands


class MqttWorker(QObject):
    message_received = Signal(str)  # 定义一个信号

    def __init__(self, username: str, lan_code: str, sn: str, ip: str, port: int):
        super().__init__()

        self.username = username
        self.lan_code = lan_code
        self.sn = sn
        self.ip = ip
        self.port = port

        self.thread = None
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.running = False

    def start(self):
        self.running = True
        self.thread = QThread()
        self.moveToThread(self.thread)
        self.thread.started.connect(self.run)
        self.thread.start()

    def run(self):
        self.client.tls_set(ca_certs=None, cert_reqs=mqtt.ssl.CERT_NONE)
        self.client.tls_insecure_set(True)
        self.client.username_pw_set(self.username, self.lan_code)
        self.client.connect(self.ip, self.port, 60)

        while self.running:
            self.client.loop_start()  # 注意这里可能需要根据实际情况调整
        self.client.disconnect()

    def stop(self):
        self.running = False
        self.thread.quit()
        self.thread.wait()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("已连接到MQTT代理")
            client.subscribe(f"device/{self.sn}/report")
            self.push_all_messages()  # 推送全部信息
        else:
            print(f"连接失败 错误码 {rc}")

    def on_message(self, client, userdata, msg):
        self.message_received.emit(msg.payload.decode())

    def publish_message(self, msg):
        self.client.publish(f"device/{self.sn}/request", msg)

    def push_all_messages(self):
        self.publish_message(json.dumps(mqtt_commands.PUSH_ALL))
