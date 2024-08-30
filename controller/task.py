import itertools
import time
from ctypes import c_int32

from PyQt6.QtCore import QThread, pyqtSignal
from libTSCANAPI import tscan_scan_devices

from model.device import TosunDevice
from model.fuzzer.can_fuzz import apply_fuzzed_data


class TaskCanFuzzRandomParams:
    def __init__(
            self,
            arb_id: int = None,
            data: [int] = None,
            bit_map: [bool] = None,
            index: int = 0,
            delay: float = 0.01
    ):
        self.arb_id = arb_id
        self.data = data
        self.bit_map = bit_map
        self.index = index
        self.delay = delay


class TaskCanFuzzRandom(QThread):
    signal_finished = pyqtSignal(bool)
    signal_process = pyqtSignal(int)

    def __init__(self, params: TaskCanFuzzRandomParams = None):
        super().__init__()
        self.params = params
        self.running = False

    def run(self) -> None:
        try:
            # ACount = c_int32(0)
            # tscan_scan_devices(ACount)
            # if ACount.value == 0:
            #     raise IOError('no device to connect.')
            # self.running = True
            # number_of_bruteforce = sum(self.params.bit_map)
            # end_index = 256 ** number_of_bruteforce
            # bruteforce_values = range(0xFF + 1)
            # fuzz_data = itertools.product(bruteforce_values, repeat=number_of_bruteforce)
            # output_file = None
            # output_data = []
            # with TosunDevice() as bus:
            #     print("Starting at index {0} of {1}".format(self.params.index, end_index))
            #     message_count = 0
            #     for current_fuzzed_data in fuzz_data:
            #         if not self.running:
            #             break
            #         if message_count < self.params.index:
            #             message_count += 1
            #             continue
            #         # Apply fuzzed data
            #         output_data = apply_fuzzed_data(self.params.data, current_fuzzed_data, self.params.bit_map)
            #         # Send message
            #         bus.send(arb_id=self.params.arb_id, data=output_data)
            #         message_count += 1
            #         print('arb_id: {}, data: {}'.format(self.params.arb_id, output_data))
            #         process = int(message_count / end_index * 100)
            #         self.signal_process.emit(process)
            #         time.sleep(self.params.delay)
            #     print("Brute force finished")
            self.running = True
            for i in range(20):
                if not self.running:
                    break
                print(i)
                time.sleep(self.params.delay)
            self.signal_finished.emit(True)
        except Exception as e:
            print('运行失败, error: {}'.format(e))
        finally:
            self.signal_finished.emit(True)
