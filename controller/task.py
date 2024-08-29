import time

from PyQt6.QtCore import pyqtSignal, QRunnable


class CanRandomFuzzTask(QRunnable):
    signal = pyqtSignal(bool)

    def __init__(self):
        super().__init__()

    def run(self) -> None:
        for i in range(20):
            print(i)
            time.sleep(1)
