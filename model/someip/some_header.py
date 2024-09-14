import struct


SERVICE_ID_SD = 0xFFFF
METHOD_ID_SD = 0x8100
LENGTH_SD = 48
CLIENT_ID_SD = 0x0000
SESSION_ID_SD = 0x0000
PROTOCOL_VERSION_SD = 0x01
INTERFACE_VERSION_SD = 0x01
MESSAGE_TYPE_SD = 0x02
RETURN_CODE_SD = 0x00


class SomeIpHeader:
    def __init__(
            self,
            service_id: int = 0x0,
            method_id: int = 0x0,
            length: int = 0x0,
            client_id: int = 0x0,
            session_id: int = 0x0,
            protocol_version: int = 0x0,
            interface_version: int = 0x0,
            message_type: int = 0x0,
            return_code: int = 0x0,
            is_sd: bool = False
        ) -> None:
        if is_sd:
            self.service_id = SERVICE_ID_SD
            self.method_id = METHOD_ID_SD
            self.length = LENGTH_SD
            self.client_id = CLIENT_ID_SD
            self.session_id = SESSION_ID_SD
            self.protocol_version = PROTOCOL_VERSION_SD
            self.interface_version = INTERFACE_VERSION_SD
            self.message_type = MESSAGE_TYPE_SD
            self.return_code = RETURN_CODE_SD
        else:
            self.service_id = service_id
            self.method_id = method_id
            self.length = length
            self.client_id = client_id
            self.session_id = session_id
            self.protocol_version = protocol_version
            self.interface_version = interface_version
            self.message_type = message_type
            self.return_code = return_code

    def encode(self) -> bytes:
        return struct.pack(">HHIHHBBBB", self.service_id, self.method_id, self.length, self.client_id, self.session_id, self.protocol_version, self.interface_version, self.message_type, self.return_code)
    
    def __str__(self) -> str:
        return f"Service ID: 0x{self.service_id:04X}, Method ID: 0x{self.method_id:04X}, Length: {self.length}, Client ID: 0x{self.client_id:04X}, Session ID: 0x{self.session_id:04X}, Protocol Version: 0x{self.protocol_version:02X}, Interface Version: 0x{self.interface_version:02X}, Message Type: 0x{self.message_type:02X}, Return Code: 0x{self.return_code:02X}"