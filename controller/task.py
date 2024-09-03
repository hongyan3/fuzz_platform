import itertools
import random
import time
from ctypes import c_int32

from PyQt6.QtCore import QThread, pyqtSignal
from libTSCANAPI import tscan_scan_devices

from model.device import TosunDevice
from model.fuzzer.can_fuzz import apply_fuzzed_data


class TaskCanFuzzBruteforceParams:
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


class TaskCanFuzzRandomParams:
    def __init__(
            self,
            static_arb_id: int = None,
            static_data: [int] = None,
            min_arb_id: int = None,
            max_arb_id: int = None,
            min_data_len: int = None,
            max_data_len: int = None,
            seed: int = None,
            index: int = 0,
            delay: float = 0.01
    ):
        self.static_arb_id = static_arb_id
        self.static_data = static_data
        self.min_arb_id = min_arb_id
        self.max_arb_id = max_arb_id
        self.min_data_len = min_data_len
        self.max_data_len = max_data_len
        self.seed = seed
        self.index = index
        self.delay = delay


class TaskCanFuzzBruteforce(QThread):
    signal_finished = pyqtSignal(bool)
    signal_process = pyqtSignal(int)

    def __init__(self, params: TaskCanFuzzBruteforceParams = None):
        super().__init__()
        self.params = params

    def run(self) -> None:
        try:
            dev_cnt = c_int32(0)
            tscan_scan_devices(dev_cnt)
            if dev_cnt.value == 0:
                raise IOError('no device to connect.')
            number_of_bruteforce = sum(self.params.bit_map)
            end_index = 256 ** number_of_bruteforce
            bruteforce_values = range(0xFF + 1)
            fuzz_data = itertools.product(bruteforce_values, repeat=number_of_bruteforce)
            output_file = None
            output_data = []
            with TosunDevice() as bus:
                print("Starting at index {0} of {1}".format(self.params.index, end_index))
                message_count = 0
                for current_fuzzed_data in fuzz_data:
                    if self.isInterruptionRequested():
                        break
                    if message_count < self.params.index:
                        message_count += 1
                        continue
                    # Apply fuzzed data
                    output_data = apply_fuzzed_data(self.params.data, current_fuzzed_data, self.params.bit_map)
                    # Send message
                    bus.send(arb_id=self.params.arb_id, data=output_data)
                    message_count += 1
                    print('arb_id: {}, data: {}'.format(self.params.arb_id, output_data))
                    process = int(message_count / end_index * 100)
                    self.signal_process.emit(process)
                    time.sleep(self.params.delay)
                print("Brute force finished")
        except Exception as e:
            print('运行失败, error: {}'.format(e))
        finally:
            self.signal_finished.emit(True)


class TaskCanFuzzRandom(QThread):
    signal_finished = pyqtSignal(bool)

    def __init__(self, params: TaskCanFuzzRandomParams = None):
        super().__init__()
        self.params = params
        self.running = False

    def run(self) -> None:
        def set_seed(seed=None):
            if seed is None:
                seed = random.randint(0, 2 ** 16)
            print("Seed: {0} (0x{0:x})".format(seed))
            random.seed(seed)

        def get_random_arb_id(min_id, max_id):
            arb_id = random.randint(min_id, max_id)
            return arb_id

        def get_random_data(min_length, max_length):
            data_length = random.randint(min_length, max_length)
            data = []
            for _ in range(data_length):
                data_byte = random.randint(0x00, 0xFF)
                data.append(data_byte)
            return data

        try:
            dev_cnt = c_int32(0)
            tscan_scan_devices(dev_cnt)
            if dev_cnt.value == 0:
                raise IOError('no device to connect.')
            set_seed(self.params.seed)

            arb_id = None
            data = None
            output_file = None
            with TosunDevice() as bus:
                current_index = 0
                messages_sent = 0
                if self.params.index is not None:
                    print("Starting at index {0}\n".format(self.params.index))
                while True:
                    if self.isInterruptionRequested():
                        break
                    if self.params.static_arb_id is None:
                        arb_id = get_random_arb_id(self.params.min_arb_id, self.params.max_arb_id)
                    else:
                        arb_id = self.params.static_arb_id
                    if self.params.static_data is None:
                        data = get_random_data(self.params.min_data_len, self.params.max_data_len)
                    else:
                        data = self.params.static_data
                    if current_index < self.params.index:
                        current_index += 1
                        continue
                    print("Messages sent: {0}, index: {1}".format(messages_sent, current_index))
                    bus.send(data=data, arb_id=arb_id)
                    messages_sent += 1
                    time.sleep(self.params.delay)
                    current_index += 1
        except Exception as e:
            print('运行失败, error: {}'.format(e))
        finally:
            self.signal_finished.emit(True)
