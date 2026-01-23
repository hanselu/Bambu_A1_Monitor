import json
import locale
import os
import sys
import time
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QLabel, QLineEdit, QSpinBox, QVBoxLayout, QHBoxLayout, QDialogButtonBox, QComboBox

import mqtt_const
from ui.ui_mqtt_mainwindow import Ui_MainWindow
from mqtt_worker import MqttWorker

# 获取脚本所在目录的绝对路径
BASE_DIR = Path(__file__).resolve().parent

DEVICE_TYPES = {
    "00M": ["X1", "X1C"],
    "03W": ["X1E"],
    "039": ["A1"],
    "030": ["A1MINI"],
    "01S": ["P1P"],
    "01P": ["P1S"],
    "22E": ["P2S"],
    "093": ["H2S"],
    "094": ["H2D"],
}


class ConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("配置参数")
        self.setModal(True)
        # 设置窗口图标
        self.setWindowIcon(QIcon(str(BASE_DIR / 'logo.png')))

        # 加载当前配置
        try:
            with open(BASE_DIR / 'config.json', 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            self.config = {
                "username": "bblp",
                "lan_code": "",
                "sn": "",
                "ip": "",
                "port": 8883
            }

        # 确保device_type存在
        if 'device_type' not in self.config:
            sn = self.config.get('sn', '')
            device_types = self.get_device_type(sn)
            if device_types:
                self.config['device_type'] = device_types[0] if len(device_types) == 1 else "未知"
            else:
                self.config['device_type'] = "未知"

        # 创建控件
        layout = QVBoxLayout()
        
        # 设置统一的标签宽度和输入框宽度
        label_width = 45
        input_width = 120
        sn_input_width = 120

        # Username
        username_layout = QHBoxLayout()
        username_layout.setSpacing(2)
        username_label = QLabel("用户名:")
        username_label.setFixedWidth(label_width)
        username_layout.addWidget(username_label)
        self.username_edit = QLineEdit(self.config.get('username', ''))
        self.username_edit.setFixedWidth(input_width)
        username_layout.addWidget(self.username_edit)
        username_layout.addStretch()
        layout.addLayout(username_layout)

        # Lan Code
        lan_code_layout = QHBoxLayout()
        lan_code_layout.setSpacing(2)
        lan_code_label = QLabel("访问码:")
        lan_code_label.setFixedWidth(label_width)
        lan_code_layout.addWidget(lan_code_label)
        self.lan_code_edit = QLineEdit(self.config.get('lan_code', ''))
        self.lan_code_edit.setFixedWidth(input_width)
        lan_code_layout.addWidget(self.lan_code_edit)
        lan_code_layout.addStretch()
        layout.addLayout(lan_code_layout)

        # SN
        sn_layout = QHBoxLayout()
        sn_layout.setSpacing(2)
        sn_label = QLabel("序列号:")
        sn_label.setFixedWidth(label_width)
        sn_layout.addWidget(sn_label)
        self.sn_edit = QLineEdit(self.config.get('sn', ''))
        self.sn_edit.setFixedWidth(sn_input_width)
        self.sn_edit.textChanged.connect(self.update_device_type)
        sn_layout.addWidget(self.sn_edit)
        sn_layout.addStretch()
        layout.addLayout(sn_layout)

        # Device Type
        device_type_layout = QHBoxLayout()
        device_type_layout.setSpacing(2)
        device_type_label_fixed = QLabel("机型:")
        device_type_label_fixed.setFixedWidth(label_width)
        device_type_layout.addWidget(device_type_label_fixed)
        self.device_type_label = QLabel()
        self.device_type_label.setFixedWidth(input_width)
        self.device_type_combo = QComboBox()
        self.device_type_combo.setFixedWidth(input_width)
        device_type_layout.addWidget(self.device_type_label)
        device_type_layout.addWidget(self.device_type_combo)
        device_type_layout.addStretch()
        layout.addLayout(device_type_layout)

        # IP
        ip_layout = QHBoxLayout()
        ip_layout.setSpacing(2)
        ip_label = QLabel("IP:")
        ip_label.setFixedWidth(label_width)
        ip_layout.addWidget(ip_label)
        self.ip_edit = QLineEdit(self.config.get('ip', ''))
        self.ip_edit.setFixedWidth(input_width)
        ip_layout.addWidget(self.ip_edit)
        ip_layout.addStretch()
        layout.addLayout(ip_layout)

        # Port
        port_layout = QHBoxLayout()
        port_layout.setSpacing(2)
        port_label = QLabel("端口:")
        port_label.setFixedWidth(label_width)
        port_layout.addWidget(port_label)
        self.port_edit = QSpinBox()
        self.port_edit.setRange(1, 65535)
        self.port_edit.setValue(self.config.get('port', 8883))
        self.port_edit.setFixedWidth(input_width)
        port_layout.addWidget(self.port_edit)
        port_layout.addStretch()
        layout.addLayout(port_layout)

        # 按钮
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)
        
        # 设置对话框最小宽度
        self.setMinimumWidth(200)

        # 初始化机型显示
        self.update_device_type()

    def get_device_type(self, sn):
        if not sn:
            return []
        for prefix, devices in DEVICE_TYPES.items():
            if sn.startswith(prefix):
                return devices
        return []

    def update_device_type(self):
        sn = self.sn_edit.text()
        device_types = self.get_device_type(sn)
        if len(device_types) == 1:
            self.device_type_label.setText(device_types[0])
            self.device_type_label.show()
            self.device_type_combo.hide()
        elif len(device_types) > 1:
            self.device_type_combo.clear()
            self.device_type_combo.addItems(device_types)
            self.device_type_combo.setCurrentIndex(0)
            self.device_type_label.hide()
            self.device_type_combo.show()
        else:
            # 未知，显示所有机型
            all_devices = [d for devices in DEVICE_TYPES.values() for d in devices]
            self.device_type_combo.clear()
            self.device_type_combo.addItems(all_devices)
            self.device_type_combo.setCurrentIndex(0)
            self.device_type_label.hide()
            self.device_type_combo.show()

    def get_config(self):
        device_types = self.get_device_type(self.sn_edit.text())
        if len(device_types) == 1:
            device_type = device_types[0]
        elif len(device_types) > 1:
            device_type = self.device_type_combo.currentText()
        else:
            device_type = self.device_type_combo.currentText() if self.device_type_combo.isVisible() else "未知"
        return {
            "username": self.username_edit.text(),
            "lan_code": self.lan_code_edit.text(),
            "sn": self.sn_edit.text(),
            "device_type": device_type,
            "ip": self.ip_edit.text(),
            "port": self.port_edit.value()
        }


class MainWindow(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # 显示配置对话框
        config_dialog = ConfigDialog()
        if config_dialog.exec() == QDialog.DialogCode.Accepted:
            self.mqtt_connect_info = config_dialog.get_config()
            self.save_config()
        else:
            sys.exit()

        self.translations: dict = {}

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

        # 读取中文翻译json
        with open(BASE_DIR / 'translations' / 'zh-Hans.json', 'r', encoding='utf-8') as f:
            self.translations = json.load(f)

    def get_device_type(self, sn):
        if not sn:
            return []
        for prefix, devices in DEVICE_TYPES.items():
            if sn.startswith(prefix):
                return devices
        return []

    def ui_init(self):
        # 窗口置顶
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
        device_type = self.mqtt_connect_info.get('device_type', '未知')
        self.setWindowTitle(f'{device_type} Monitor')
        # 设置窗口图标        
        self.setWindowIcon(QIcon(str(BASE_DIR / 'logo.png')))
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
        with open(BASE_DIR / 'config.json', 'r', encoding='utf-8') as f:
            self.mqtt_connect_info = json.load(f)

    def save_config(self):
        with open(BASE_DIR / 'config.json', 'w', encoding='utf-8') as f:
            json.dump(self.mqtt_connect_info, f, indent=4)

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
