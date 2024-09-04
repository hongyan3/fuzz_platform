import sys
from ctypes import c_int32

from PyQt6.QtCore import QTimer, QObject, pyqtSignal
from PyQt6.QtGui import QTextCursor
from PyQt6.QtWidgets import QMainWindow, QTextBrowser, QMessageBox
from libTSCANAPI import tscan_scan_devices

from controller import TaskCanFuzzBruteforce
from controller.task import TaskCanFuzzBruteforceParams, TaskCanFuzzRandom, TaskCanFuzzRandomParams
from ui import UI_MainWindow


class RedirectStream(QObject):
    text_written = pyqtSignal(str)

    def __init__(self, widget):
        super().__init__()
        self.widget = widget
        self.buffer = ""
        # 定时器批量更新缓存的文本
        self.flush_timer = QTimer()
        self.flush_timer.timeout.connect(self.flush_buffer)
        self.flush_timer.start(200)  # 每100ms刷新一次

    def write(self, text):
        self.buffer += text
        self.text_written.emit(text)  # 可以选择性地触发信号，用于调试

    def flush(self):
        pass

    def flush_buffer(self):
        if self.buffer:
            self.widget.moveCursor(QTextCursor.MoveOperation.End)
            self.widget.insertPlainText(self.buffer)
            self.widget.ensureCursorVisible()
            self.buffer = ""  # 清空缓存


class MainWindow(QMainWindow, UI_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 线程任务初始化
        self.task_can_fuzz_bruteforce = TaskCanFuzzBruteforce(None)
        self.task_can_fuzz_bruteforce.signal_finished.connect(self.on_can_fuzz_task_finished)
        self.task_can_fuzz_random = TaskCanFuzzRandom(None)
        self.task_can_fuzz_random.signal_finished.connect(self.on_can_fuzz_task_finished)
        # 插槽初始化
        self.can_fuzz_start.clicked.connect(self.on_button_clicked)
        self.clear_console.clicked.connect(self.on_clear_console_clicked)
        self.task_can_fuzz_bruteforce.signal_process.connect(self.on_brute_process_update)
        # 组件初始化
        self.device_select.addItem('同星')
        self.fixed_arb_id.setText('123')
        self.initial_data.setText('0,0,0,0,0,0,0,0')
        self.fuzz_bit_map.setText('1,1,1,1,1,1,1,1')
        self.brute_start_index.setText('0')

        self.random_min_id.setText('0')
        self.random_max_id.setText('7FF')
        self.random_start_index.setText('0')
        self.brute_process.setVisible(False)
        # 重定向控制台输出到TextBrowser
        self.stream = RedirectStream(self.console_browser)
        sys.stdout = self.stream
        sys.stderr = self.stream

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
            dev_cnt = c_int32(0)
            tscan_scan_devices(dev_cnt)
            if dev_cnt.value == 0:
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
                self.task_can_fuzz_bruteforce.params = params
                self.task_can_fuzz_bruteforce.start()
            elif mode == 1:
                try:
                    static_arb_id = None if self.static_arb_id.text() == '' else int(self.static_arb_id.text())
                    static_data = None if self.static_data.text() == '' else [int(i) for i in self.initial_data.text().split(',')]
                    min_arb_id = None if self.random_min_id.text() == '' else int(self.random_min_id.text(), 16)
                    max_arb_id = None if self.random_max_id.text() == '' else int(self.random_max_id.text(), 16)
                    min_data_len = None if self.data_min_length.text() == '' else int(self.data_min_length.text())
                    max_data_len = None if self.data_max_length.text() == '' else int(self.data_max_length.text())
                    seed = None if self.seed.text() == '' else int(self.seed.text())
                    index = None if self.random_start_index.text() == '' else int(self.random_start_index.text())
                    delay = None if self.random_delay.text() == '' else int(self.random_delay.text()) / 1000
                except Exception as e:
                    print('参数有误，请检查 error: {}'.format(e))
                    set_finished()
                    return
                params = TaskCanFuzzRandomParams(
                    static_arb_id=static_arb_id,
                    static_data=static_data,
                    min_arb_id=min_arb_id,
                    max_arb_id=max_arb_id,
                    min_data_len=min_data_len,
                    max_data_len=max_data_len,
                    seed=seed,
                    index=index,
                    delay=delay
                )
                self.task_can_fuzz_random.params = params
                self.task_can_fuzz_random.start()
        else:
            self.task_can_fuzz_bruteforce.running = False
            self.task_can_fuzz_bruteforce.requestInterruption()
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
