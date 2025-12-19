import json
import locale
import sys
import time

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow

import mqtt_const
from ui.ui_mqtt_mainwindow import Ui_MainWindow
from mqtt_worker import MqttWorker


class MainWindow(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.translations: dict = {}
        self.mqtt_connect_info: dict = {}

        self.data_init()

        # 读取mqtt连接信息

        self.mqtt_worker = MqttWorker(
            username=self.mqtt_connect_info['username'],
            lan_code=self.mqtt_connect_info['lan_code'],
            sn=self.mqtt_connect_info['sn'],
            ip=self.mqtt_connect_info['ip'],
            port=self.mqtt_connect_info['port'],
        )
        self.mqtt_worker.message_received.connect(self.update_monitor_info)

        self.setupUi(self)
        self.btn_pull_all.clicked.connect(self.btn_pull_all_on_clicked)

        self.task_name: str = '未知任务'
        self.total_layer: int = -1
        self.curr_layer: int = -1
        self.total_time: int = -1
        self.remind_time = -1
        self.nozzle_temperature: float = -1
        self.nozzle_target_temperature: float = -1
        self.hotbed_temperature: float = -1
        self.hotbed_target_temperature: float = -1
        self.task_percent: int = -1
        self.stage_code: int = -1

        self.ui_init()
        self.clear_info()

        self.mqtt_worker.start()
        # self.mqtt_worker.push_all_messages()

    def data_init(self):
        # 设置locale为英文，以使用AM/PM
        locale.setlocale(locale.LC_TIME, 'C')

        # 读取mqtt配置
        self.load_config()

        # 读取中文翻译json
        with open('translations/zh-Hans.json', 'r', encoding='utf-8') as f:
            self.translations = json.load(f)

    def ui_init(self):
        # 窗口置顶
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
        self.setWindowTitle('A1 Monitor')
        self.show_monitor_info()

    def show_monitor_info(self):
        self.label_task.setText(f'任务: {self.task_name}')
        self.label_layer.setText(f'层数: {self.curr_layer} / {self.total_layer}')
        # 天数
        days = self.remind_time // 1440
        # 小时数
        hours = self.remind_time % 1440 // 60
        # 钟数
        minutes = self.remind_time % 1440 % 60

        # 计算完成时间
        finish_time = time.time() + self.remind_time * 60
        finish_time_struct = time.localtime(finish_time)
        finish_time_str = time.strftime('%I:%M %p', finish_time_struct)

        if days > 0:
            self.label_time.setText(f'剩余: {days}天{hours:02d}时{minutes:02d}分 → 明天{finish_time_str}')
        elif hours > 0:
            self.label_time.setText(f'剩余: {hours}时{minutes:02d}分 → {finish_time_str}')
        else:
            self.label_time.setText(f'剩余: {minutes}分 → {finish_time_str}')
        self.label_nozzle.setText(f'喷嘴: {self.nozzle_temperature:.2f} / {self.nozzle_target_temperature:.2f}')
        self.label_hotbed.setText(f'热床: {self.hotbed_temperature:.2f} / {self.hotbed_target_temperature:.2f}')
        self.progressBar.setValue(self.task_percent)
        self.show_current_stage()

    def clear_info(self):
        self.label_task.setText('任务: 无')
        self.label_layer.setText('层数: ')
        self.label_time.setText('剩余: ')
        self.label_nozzle.setText(f'喷嘴: {self.nozzle_temperature:.2f} / {self.nozzle_target_temperature:.2f}')
        self.label_hotbed.setText(f'热床: {self.hotbed_temperature:.2f} / {self.hotbed_target_temperature:.2f}')
        self.label_stage.setText('状态: 空闲')
        self.progressBar.setValue(0)

    def load_config(self):
        with open('config.json', 'r', encoding='utf-8') as f:
            self.mqtt_connect_info = json.load(f)

    def show_current_stage(self):
        current_stage = mqtt_const.CURRENT_STAGE_IDS.get(self.stage_code, f'未知状态{self.stage_code}')
        if current_stage == 'idle':
            self.clear_info()
        else:
            current_stage = self.translations['entity']['sensor']['stage']['state'].get(current_stage, current_stage)
            self.label_stage.setText(f'状态: {current_stage}')

    def update_monitor_info(self, message: str):
        try:
            data = json.loads(message)['print']

            for key, value in data.items():
                if key == 'subtask_name':
                    self.task_name = value
                    continue

                if key == 'mc_remaining_time':
                    self.remind_time = value
                    continue

                if key == 'nozzle_temper':
                    self.nozzle_temperature = value
                    continue

                if key == 'bed_temper':
                    self.hotbed_temperature = value
                    continue

                if key == 'mc_percent':
                    self.task_percent = value
                    continue

                if key == 'layer_num':
                    self.curr_layer = value
                    continue

                if key == 'total_layer_num':
                    self.total_layer = value
                    continue

                if key == 'bed_target_temper':
                    self.hotbed_target_temperature = value
                    continue

                if key == 'nozzle_target_temper':
                    self.nozzle_target_temperature = value
                    continue

                if key == 'stg_cur':
                    self.stage_code = value
                    # self.show_current_stage(value)
                    continue

                continue

                # # 调试用 跳过特定信息
                # if key in ['msg', 'sequence_id', 'wifi_signal', 'command', 'mc_print_line_number',
                #            'heatbreak_fan_speed']:
                #     continue
                #
                # print(key, value)

            self.show_monitor_info()

        except Exception as e:
            print('发生异常', e)
            print(message)

    def btn_pull_all_on_clicked(self):
        self.mqtt_worker.push_all_messages()

    def closeEvent(self, event):
        self.mqtt_worker.stop()
        super().closeEvent(event)


def main():
    app = QApplication([])
    app.setStyle('Fusion')
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
