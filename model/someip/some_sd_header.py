class SdEntry:
    pass

class SdOption:
    pass

class SomeIpSdHeader:
    def __init__(
            self,
            flags: int = 0x0,
            reserved: int = 0x0,
            entries_length: int = 0x0,
            entries_array: list[SdEntry] = [],
            options_length: int = 0x0,
            options_array: list[SdOption] = []
        ) -> None:
        pass

