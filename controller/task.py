import itertools
import time

from PyQt6.QtCore import QThread, pyqtSignal

from model.device import TosunDevice
from model.fuzzer.can_fuzz import apply_fuzzed_data


class TaskCanFuzzRandom(QThread):
    signal_finished = pyqtSignal(bool)
    signal_process = pyqtSignal(int)

    class Params:
        arb_id: int
        data: []
        bit_map: []
        index: int
        delay: float

    def __init__(self):
        super().__init__()
        self.running = False

    def run(self) -> None:
        try:
            self.running = True
            number_of_bruteforce = sum(self.Params.bit_map)
            end_index = 256 ** number_of_bruteforce
            if not 0 <= self.Params.index <= end_index:
                raise ValueError(
                    "Invalid start index '{0}', current range is [0-{1}]".format(self.Params.index, end_index))
            bruteforce_values = range(0xFF + 1)
            fuzz_data = itertools.product(bruteforce_values, repeat=number_of_bruteforce)
            output_file = None
            output_data = []
            with TosunDevice() as bus:
                print("Starting at index {0} of {1}".format(self.Params.index, end_index))
                message_count = 0
                for current_fuzzed_data in fuzz_data:
                    if not self.running:
                        break
                    if message_count < self.Params.index:
                        message_count += 1
                        continue
                    # Apply fuzzed data
                    output_data = apply_fuzzed_data(self.Params.data, current_fuzzed_data, self.Params.bit_map)
                    # Send message
                    bus.send(arb_id=self.Params.arb_id, data=output_data)
                    message_count += 1
                    print('arb_id: {}, data: {}'.format(self.Params.arb_id, output_data))
                    process = int(message_count / end_index * 100)
                    self.signal_process.emit(process)
                    time.sleep(self.Params.delay)
                print("Brute force finished")
        except Exception as e:
            print('运行失败, error: {}'.format(e))
        finally:
            self.signal_finished.emit(True)
