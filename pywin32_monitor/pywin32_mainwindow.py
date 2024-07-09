import sys

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QTimer
from ui.ui_pywin32_mainwindow import Ui_MainWindow
from bambu_studio import get_machine_info


class MainWindow(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("A1监视器")
        self.show()

        self.timer = QTimer()
        self.timer.start(1000)
        self.timer.timeout.connect(self.update_info)

    def hide_info_ui(self):
        self.label_requirement.setVisible(False)
        self.label_layer.setVisible(False)
        self.label_time.setVisible(False)
        self.label_hotend.setVisible(False)
        self.label_hotbed.setVisible(False)
        self.label_box.setVisible(False)
        self.progressBar.setVisible(False)

    def show_info_ui(self):
        self.label_requirement.setVisible(True)
        self.label_layer.setVisible(True)
        self.label_time.setVisible(True)
        self.label_hotend.setVisible(True)
        self.label_hotbed.setVisible(True)
        self.label_box.setVisible(True)
        self.progressBar.setVisible(True)

    def update_info(self):
        info = get_machine_info()
        if info is None:
            self.label_task.setText('找不到Bambu Studio')
            self.hide_info_ui()
            return
        
        self.show_info_ui()
        task = info.get("task", "")
        percent = int(info.get("percent", 100))
        mass = info.get("mass", "")
        layer = info.get("layer", "")
        total_time = info.get("total_time", "")
        remaining_time = info.get("remaining_time", "")
        hotend = info.get("hotend", "")
        hotbed = info.get("hotbed", "")
        box = info.get("box", None)

        self.label_task.setText(task)
        self.progressBar.setValue(percent)
        self.label_requirement.setText(f"需要: {mass} {total_time}")
        self.label_layer.setText(f"层数: {layer}")
        self.label_time.setText(f"剩余: {remaining_time}")
        self.label_hotend.setText(f"喷口: {hotend}")
        self.label_hotbed.setText(f"热床: {hotbed}")
        if box:
            self.label_box.setVisible(True)
            self.label_box.setText(f"箱体: {box}")
        else:
            self.label_box.setVisible(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
