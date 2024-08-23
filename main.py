import threading
from model.device import TosunDevice
from model.fuzzer.can_fuzz import CanFuzzer


def start():
    ts = TosunDevice()
    ts.connect()
    fuzzer = CanFuzzer(can_interface=ts)
    fuzzer.random_fuzz()


if __name__ == '__main__':
    start()
