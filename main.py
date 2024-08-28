import itertools
import os
import threading
import time

from model.device import TosunDevice
from model.fuzzer.can_fuzz import CanFuzzer
from model.uds import UDS


def start():
    ts = TosunDevice()
    ts.connect()
    fuzzer = CanFuzzer(can_interface=ts)
    # fuzzer.random_fuzz(seed=14792, filename='./test.log', start_index=2400, delay=1)
    # fuzzer.replay_from_file(file_name='test.log', delay=2)
    print(fuzzer.get_arb_ids_set(60))


if __name__ == '__main__':
    start()
