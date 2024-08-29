import sys
import sys
import time

from PyQt6.QtCore import QThreadPool
from PyQt6.QtGui import QTextCursor
from PyQt6.QtWidgets import QMainWindow, QTextBrowser, QMessageBox

from controller import CanRandomFuzzTask
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
        self.init_ui()
        self.thread_pool = QThreadPool.globalInstance()
        self.can_random_fuzz_task = CanRandomFuzzTask()

    def init_ui(self):
        self.can_fuzz_start.clicked.connect(self.on_button_clicked)
        self.clear_console.clicked.connect(self.on_clear_console_clicked)
        self.device_select.addItem('同星')
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

    def on_button_clicked(self):
        text = self.can_fuzz_start.text()
        print(text)
        if text == '开始':
            self.can_fuzz_start.setText('停止')
            mode = self.fuzz_select.currentIndex()
            if mode == 0:
                arb_id = self.fixed_arb_id.text()
                data = self.initial_data.text()
                bit_map = self.fuzz_bit_map.text()
                index = self.brute_start_index.text()
                delay = self.brute_delay.text()
                self.thread_pool.start(self.can_random_fuzz_task)

            elif mode == 1:
                print('随机Fuzz')
        else:
            self.can_fuzz_start.setText('开始')

    def on_clear_console_clicked(self):
        self.console_browser.clear()


def demo():
    index = 0
    while True:
        print(index)
        index += 1
        time.sleep(1)
        if index == 5:
            raise ValueError('demo')
