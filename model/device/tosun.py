from libTSCANAPI import *
from model.interface import CanInterface, FlexRayInterface
from ctypes import *

PREFIX = '[TOSUN]'


class TosunDevice(CanInterface, FlexRayInterface):

    def __init__(self, serial_number=None, chn1_baudrate=500, chn2_baudrate=500):
        """
        同星CAN盒初始化

        :param serial_number: 产品序列号，若电脑只连接一个设备可省略该参数
        :param chn1_baudrate: 波特率， 默认为500
        """
        self.__bus = c_size_t(0)
        self.__chn1_baudrate = chn1_baudrate
        self.__chn2_baudrate = chn2_baudrate
        if serial_number is not None:
            self.__device_code = serial_number.encode()
        else:
            self.__device_code = b''
        initialize_lib_tscan(True, True, False)

    def connect(self):
        """
        连接同星设备
        :return:
        """
        code = tsapp_connect(self.__device_code, self.__bus)
        if code == 0:
            print(f'{PREFIX} Device connection successful. handle: {self.__bus.value}.')
            # 设置波特率
            tsapp_configure_baudrate_can(self.__bus, 0, self.__chn1_baudrate, 1)
            tsapp_configure_baudrate_can(self.__bus, 1, self.__chn2_baudrate, 1)
        elif code == 5:
            print(f'{PREFIX} Device is already connected.')
        else:
            msg = self.__get_error_description(code)
            print(f'{PREFIX} Device connection failed, error code: {code}, msg: {msg.value.decode()}')
            exit(-1)

    def close(self):
        tsapp_disconnect_by_handle(self.__bus)
        finalize_lib_tscan()

    def send(self, data, arb_id, is_extended=None, is_error=False, is_remote=False, is_fd=False, channel=0):
        pro_bit = ['0'] * 8
        fd_pro_bit = ['0'] * 8
        pro_bit[0] = '1'  # 0: RX 1: TX
        if is_error:
            arb_id = 0xFFFFFFFF
        if is_remote:
            pro_bit[1] = '1'  # 0：data frame 数据帧；1：remote frame 远程帧
        if is_extended:
            pro_bit[2] = '1'  # 0：std frame 标准帧；1：extended frame 扩
        if is_fd:
            fd_pro_bit[0] = '1'  # 0: CAN 1: CAN_FD
        f_properties = int(''.join(pro_bit), 2)
        fd_properties = int(''.join(fd_pro_bit), 2)
        message = TLIBCANFD(
            FIdxChn=channel,
            FDLC=8,
            FIdentifier=arb_id,
            FProperties=f_properties,
            FFDProperties=fd_properties,
            FData=data
        )
        res = tsapp_transmit_can_async(self.__bus, message)
        if res != 0:
            msg = self.__get_error_description(res)
            print(f'Message send failed, msg: {msg.value.decode()}')
            return

    def receive(self, channel=0, timeout=None):
        start_time = time.time()
        while True:
            buffer = (TLIBCANFD * 1)()
            buff_size = s32(1)
            tsfifo_receive_canfd_msgs(self.__bus, buffer, buff_size, channel, READ_TX_RX_DEF.ONLY_RX_MESSAGES)
            msg = buffer[0]
            if buff_size.value > 0 and msg.FIdentifier > 0:
                break
            if timeout is not None:
                if time.time() - start_time > timeout:
                    raise TimeoutError
        msg_id = msg.FIdentifier
        data = []
        timestamp = msg.FTimeUs
        for i in range(DLC_DATA_BYTE_CNT[msg.FDLC]):
            data.append(msg.FData[i])
        return msg_id, data, timestamp

    def send_fr_message(self):
        pass

    def receive_fr_message(self, channel, timeout=None):
        start_time = time.time()
        while True:
            buffer = (TLIBFlexray * 1)()
            buff_size = s32(1)
            tsfifo_receive_flexray_msgs(self.__bus, buffer, buff_size, channel, READ_TX_RX_DEF.TX_RX_MESSAGES)
            msg = buffer[0]
            if buff_size.value > 0 and msg.FSlotId > 0:
                break
            if timeout is not None:
                if time.time() - start_time > timeout:
                    raise TimeoutError
        msg_id = msg.FSlotId
        data = []
        timestamp = msg.FTimeUs
        for i in msg.FData:
            data.append(i)
        return msg_id, data, timestamp

    @staticmethod
    def __get_error_description(code):
        """
        根据错误码获取描述
        :param code: 错误码
        :return:
        """
        result = c_char_p()
        tscan_get_error_description(code, result)
        return result
