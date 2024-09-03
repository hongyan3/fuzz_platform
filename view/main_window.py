import sys
from ctypes import c_int32

from PyQt6.QtGui import QTextCursor
from PyQt6.QtWidgets import QMainWindow, QTextBrowser, QMessageBox
from libTSCANAPI import tscan_scan_devices

from controller import TaskCanFuzzBruteforce
from controller.task import TaskCanFuzzBruteforceParams
from ui import UI_MainWindow


class RedirectStream:
    widget: QTextBrowser

    def __init__(self, widget):
        self.widget = widget

    def write(self, text):
        self.widget.moveCursor(QTextCursor.MoveOperation.End)
        self.widget.insertPlainText(text)
        self.widget.ensureCursorVisible()

    def flush(self):
        pass


class MainWindow(QMainWindow, UI_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 线程任务初始化
        self.task_can_fuzz_random = TaskCanFuzzBruteforce(None)
        self.task_can_fuzz_random.signal_finished.connect(self.on_can_fuzz_task_finished)
        # 插槽初始化
        self.can_fuzz_start.clicked.connect(self.on_button_clicked)
        self.clear_console.clicked.connect(self.on_clear_console_clicked)
        self.task_can_fuzz_random.signal_process.connect(self.on_brute_process_update)
        # 组件初始化
        self.device_select.addItem('同星')
        self.fixed_arb_id.setText('123')
        self.initial_data.setText('0,0,0,0,0,0,0,0')
        self.fuzz_bit_map.setText('1,1,1,1,1,1,1,1')
        self.brute_start_index.setText('0')
        self.brute_process.setVisible(False)
        # 重定向控制台输出到TextBrowser
        sys.stdout = RedirectStream(self.console_browser)
        sys.stderr = RedirectStream(self.console_browser)

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, '提示', '确定要退出吗?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            sys.stdout = sys.__stdout__
            event.accept()
            res = super().closeEvent(event)
        else:
            event.ignore()
            res = None
        return res

    def show_message(self, msg):
        QMessageBox.question(
            self, '提示', msg,
            QMessageBox.StandardButton.Yes)

    def on_button_clicked(self):
        def set_finished():
            self.can_fuzz_start.setText('开始')
            self.brute_process.setVisible(False)

        def set_start():
            self.can_fuzz_start.setText('停止')
            self.brute_process.setVisible(True)

        text = self.can_fuzz_start.text()
        if text == '开始':
            ACount = c_int32(0)
            tscan_scan_devices(ACount)
            if ACount.value == 0:
                self.show_message('未发现设备连接')
                return
            set_start()
            mode = self.fuzz_select.currentIndex()
            if mode == 0:
                try:
                    arb_id = int(self.fixed_arb_id.text())
                    data = [int(i) for i in self.initial_data.text().split(',')]
                    bit_map = [i == '1' for i in self.fuzz_bit_map.text().split(',')]
                    index = int(self.brute_start_index.text())
                    delay = int(self.brute_delay.text()) / 1000
                except Exception as e:
                    print('参数有误，请检查 error: {}'.format(e))
                    set_finished()
                    return
                params = TaskCanFuzzBruteforceParams(
                    arb_id=arb_id,
                    data=data,
                    bit_map=bit_map,
                    index=index,
                    delay=delay
                )
                self.task_can_fuzz_random.params = params
                self.task_can_fuzz_random.start()
            elif mode == 1:
                print('随机Fuzz')
        else:
            self.task_can_fuzz_random.running = False
            self.task_can_fuzz_random.requestInterruption()
            set_finished()

    def on_clear_console_clicked(self):
        self.console_browser.clear()

    def on_can_fuzz_task_finished(self, finished):
        if finished:
            self.can_fuzz_start.setText('开始')
            self.brute_process.setVisible(False)

    def on_brute_process_update(self, process):
        self.brute_process.setValue(process)
