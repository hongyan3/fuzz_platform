from model.device import TosunDevice


def start():
    ts = TosunDevice()
    ts.connect()
    print(ts.receive(channel=0, timeout=1))


if __name__ == '__main__':
    start()
