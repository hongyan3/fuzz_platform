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
    fuzzer.random_fuzz(seed=14792, filename='./test.log')
    # uds = UDS(can_interface=ts)
    # print(uds.
    #       uds_discovery(min_id=0x000, max_id=0x7FF, blacklist_args=None, auto_blacklist_duration=0.1, delay=0.1,
    #                     verify=True))

if __name__ == '__main__':
    start()
