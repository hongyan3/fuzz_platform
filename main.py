import itertools
import threading
import time

from model.device import TosunDevice
from model.fuzzer.can_fuzz import CanFuzzer
from model.uds import UDS


def start():
    ts = TosunDevice()
    ts.connect()
    # fuzzer = CanFuzzer(can_interface=ts)
    # fuzzer.bruteforce_fuzz(0x123, [0, 0xFF, 0, 0xFF, 0xFF, 0, 0xFF, 0xFF],
    #                        [True, False, True, False, False, True, False, False])
    uds = UDS(can_interface=ts)
    print(uds.service_discovery(arb_id_request=0x7FF, arb_id_response=0x637, timeout=1))


if __name__ == '__main__':
    start()
