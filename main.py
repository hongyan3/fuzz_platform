import itertools
import threading
import time

from model.device import TosunDevice
from model.fuzzer.can_fuzz import CanFuzzer


def start():
    ts = TosunDevice()
    ts.connect()
    fuzzer = CanFuzzer(can_interface=ts)
    fuzzer.bruteforce_fuzz(0x123, [0, 0xFF, 0, 0xFF, 0xFF, 0, 0xFF, 0xFF],
                           [True, False, True, False, False, True, False, False])


if __name__ == '__main__':
    start()


