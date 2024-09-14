from someip import SomeIpHeader

class SomeIpMessage():
    def __init__(self, header: SomeIpHeader, payload: bytes) -> None:
        self.header = header
        self.payload = payload
        # 计算header中length的值
        self.header.length = len(payload) * 2

    def encode(self) -> bytes:
        return self.header.encode() + self.payload

    def __str__(self) -> str:
        return f'{self.header}, Payload: {self.payload}'