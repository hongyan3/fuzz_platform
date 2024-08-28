import sys
import time

from model.constants import ARBITRATION_ID_MIN, ARBITRATION_ID_MAX_EXTENDED, ARBITRATION_ID_MAX
from model.utils.iso14229_1 import Iso14229_1, NegativeResponseCodes, Constants, Services
from model.utils.iso15765_2 import IsoTp

UDS_SERVICE_NAMES = {
    0x10: "诊断会话控制（DIAGNOSTIC_SESSION_CONTROL）",
    0x11: "ECU复位（ECU_RESET）",
    0x14: "清除诊断信息（CLEAR_DIAGNOSTIC_INFORMATION）",
    0x19: "读取故障码信息（READ_DTC_INFORMATION）",
    0x20: "恢复默认设置（RETURN_TO_NORMAL）",
    0x22: "按标识符读取数据（READ_DATA_BY_IDENTIFIER）",
    0x23: "按地址读取内存（READ_MEMORY_BY_ADDRESS）",
    0x24: "按标识符读取标度数据（READ_SCALING_DATA_BY_IDENTIFIER）",
    0x27: "安全访问（SECURITY_ACCESS）",
    0x28: "通信控制（COMMUNICATION_CONTROL）",
    0x29: "认证（AUTHENTICATION）",
    0x2A: "按周期性标识符读取数据（READ_DATA_BY_PERIODIC_IDENTIFIER）",
    0x2C: "动态定义数据标识符（DYNAMICALLY_DEFINE_DATA_IDENTIFIER）",
    0x2D: "按内存地址定义PID（DEFINE_PID_BY_MEMORY_ADDRESS）",
    0x2E: "按标识符写入数据（WRITE_DATA_BY_IDENTIFIER）",
    0x2F: "按标识符进行输入输出控制（INPUT_OUTPUT_CONTROL_BY_IDENTIFIER）",
    0x31: "例程控制（ROUTINE_CONTROL）",
    0x34: "请求下载（REQUEST_DOWNLOAD）",
    0x35: "请求上传（REQUEST_UPLOAD）",
    0x36: "传输数据（TRANSFER_DATA）",
    0x37: "请求退出传输（REQUEST_TRANSFER_EXIT）",
    0x38: "请求文件传输（REQUEST_FILE_TRANSFER）",
    0x3D: "按地址写入内存（WRITE_MEMORY_BY_ADDRESS）",
    0x3E: "测试仪存在（TESTER_PRESENT）",
    0x7F: "负向响应（NEGATIVE_RESPONSE）",
    0x83: "访问定时参数（ACCESS_TIMING_PARAMETER）",
    0x84: "安全数据传输（SECURED_DATA_TRANSMISSION）",
    0x85: "控制故障码设置（CONTROL_DTC_SETTING）",
    0x86: "事件响应（RESPONSE_ON_EVENT）",
    0x87: "链接控制（LINK_CONTROL）"
}

NRC_NAMES = {
    0x00: "正向响应（POSITIVE_RESPONSE）",
    0x10: "普通拒绝（GENERAL_REJECT）",
    0x11: "服务不被支持（SERVICE_NOT_SUPPORTED）",
    0x12: "子功能不被支持（SUB_FUNCTION_NOT_SUPPORTED）",
    0x13: "消息长度错误或格式无效（INCORRECT_MESSAGE_LENGTH_OR_INVALID_FORMAT）",
    0x14: "响应过长（RESPONSE_TOO_LONG）",
    0x21: "忙碌请重试（BUSY_REPEAT_REQUEST）",
    0x22: "条件不正确（CONDITIONS_NOT_CORRECT）",
    0x24: "请求序列错误（REQUEST_SEQUENCE_ERROR）",
    0x25: "子网组件无响应（NO_RESPONSE_FROM_SUBNET_COMPONENT）",
    0x26: "故障阻止请求执行（FAILURE_PREVENTS_EXECUTION_OF_REQUESTED_ACTION）",
    0x31: "请求超出范围（REQUEST_OUT_OF_RANGE）",
    0x33: "安全访问被拒绝（SECURITY_ACCESS_DENIED）",
    0x34: "需要认证（AUTHENTICATION_REQUIRED）",
    0x35: "无效密钥（INVALID_KEY）",
    0x36: "尝试次数过多（EXCEEDED_NUMBER_OF_ATTEMPTS）",
    0x37: "所需等待时间未到期（REQUIRED_TIME_DELAY_NOT_EXPIRED）",
    0x70: "上传下载未被接受（UPLOAD_DOWNLOAD_NOT_ACCEPTED）",
    0x71: "传输数据已暂停（TRANSFER_DATA_SUSPENDED）",
    0x72: "编程失败（GENERAL_PROGRAMMING_FAILURE）",
    0x73: "块序列计数器错误（WRONG_BLOCK_SEQUENCE_COUNTER）",
    0x78: "请求已接收待处理响应（REQUEST_CORRECTLY_RECEIVED_RESPONSE_PENDING）",
    0x7E: "活动会话中子功能不被支持（SUB_FUNCTION_NOT_SUPPORTED_IN_ACTIVE_SESSION）",
    0x7F: "活动会话中服务不被支持（SERVICE_NOT_SUPPORTED_IN_ACTIVE_SESSION）",
    0x81: "转速过高（RPM_TOO_HIGH）",
    0x82: "转速过低（RPM_TOO_LOW）",
    0x83: "发动机正在运行（ENGINE_IS_RUNNING）",
    0x84: "发动机未运行（ENGINE_IS_NOT_RUNNING）",
    0x85: "发动机运行时间太短（ENGINE_RUN_TIME_TOO_LOW）",
    0x86: "温度过高（TEMPERATURE_TOO_HIGH）",
    0x87: "温度过低（TEMPERATURE_TOO_LOW）",
    0x88: "车速过高（VEHICLE_SPEED_TOO_HIGH）",
    0x89: "车速过低（VEHICLE_SPEED_TOO_LOW）",
    0x8A: "油门踏板位置过高（THROTTLE_PEDAL_TOO_HIGH）",
    0x8B: "油门踏板位置过低（THROTTLE_PEDAL_TOO_LOW）",
    0x8C: "变速器不在空档（TRANSMISSION_RANGE_NOT_IN_NEUTRAL）",
    0x8D: "变速器不在前进挡（TRANSMISSION_RANGE_NOT_IN_GEAR）",
    0x8F: "制动开关未关闭（BRAKE_SWITCHES_NOT_CLOSED）",
    0x90: "换挡杆不在驻车位（SHIFT_LEVER_NOT_IN_PARK）",
    0x91: "液力变矩器离合器锁定（TORQUE_CONVERTER_CLUTCH_LOCKED）",
    0x92: "电压过高（VOLTAGE_TOO_HIGH）",
    0x93: "电压过低（VOLTAGE_TOO_LOW）"
}

DELAY_DISCOVERY = 0.01
DELAY_TESTER_PRESENT = 0.5
DELAY_SECSEED_RESET = 0.01
TIMEOUT_SERVICES = 0.2
TIMEOUT_SUBSERVICES = 0.02

# Max number of arbitration IDs to backtrack during verification
VERIFICATION_BACKTRACK = 5
# Extra time in seconds to wait for responses during verification
VERIFICATION_EXTRA_DELAY = 0.5

BYTE_MIN = 0x00
BYTE_MAX = 0xFF

DUMP_DID_MIN = 0x0000
DUMP_DID_MAX = 0xFFFF
DUMP_DID_TIMEOUT = 0.2

MEM_START_ADDR = 0
MEM_LEN = 0x100
MEM_SIZE = 0x10
ADDR_BYTE_SIZE = 4
MEM_LEN_BYTE_SIZE = 2


def get_negative_response_code_name(nrc):
    nrc_name = NRC_NAMES.get(nrc, "Unknown NRC value")
    return nrc_name


def print_negative_response_code(nrc):
    nrc_name = get_negative_response_code_name(nrc)
    print(f"Negative Response Code (NRC): {hex(nrc)} - {nrc_name}")


def auto_blacklist(bus, duration, classifier_function, print_results):
    if print_results:
        print("Scanning for arbitration IDs to blacklist")
    blacklist = set()
    start_time = time.time()
    end_time = start_time + duration
    while time.time() < end_time:
        if print_results:
            time_left = end_time - time.time()
            num_matches = len(blacklist)
            print("\r{0:> 5.1f} seconds left, {1} found".format(time_left, num_matches), end="")
            sys.stdout.flush()
        # Receive message
        msg = bus.recv(timeout=0.1)
        if msg is None:
            continue
        # Classify
        if classifier_function(msg):
            # Add to blacklist
            blacklist.add(msg.arbitration_id)
    if print_results:
        num_matches = len(blacklist)
        print("\r  0.0 seconds left, {0} found".format(num_matches), end="")
        if len(blacklist) > 0:
            print("\n  Detected IDs: {0}".format(" ".join(sorted(list(map(hex, blacklist))))))
        else:
            print()
    return blacklist


class UDS:
    def __init__(self, can_interface):
        self.bus = can_interface

    def uds_discovery(self, min_id=ARBITRATION_ID_MIN, max_id=ARBITRATION_ID_MAX, blacklist_args=None,
                      auto_blacklist_duration=None, delay=1, verify=True, print_results=True):
        # Set defaults
        if blacklist_args is None:
            blacklist_args = []
        if min_id is None:
            min_id = ARBITRATION_ID_MIN
        if max_id is None:
            if min_id <= ARBITRATION_ID_MAX:
                max_id = ARBITRATION_ID_MAX
            else:
                # If min_id is extended, use an extended default max_id as well
                max_id = ARBITRATION_ID_MAX_EXTENDED
        if auto_blacklist_duration is None:
            auto_blacklist_duration = 0
        if blacklist_args is None:
            blacklist_args = []

        # Sanity checks
        if max_id < min_id:
            raise ValueError("max_id must not be smaller than min_id -"
                             " got min:0x{0:x}, max:0x{1:x}".format(min_id, max_id))
        if auto_blacklist_duration < 0:
            raise ValueError("auto_blacklist_duration must not be smaller "
                             "than 0, got {0}".format(auto_blacklist_duration))

        diagnostic_session_control = Services.DiagnosticSessionControl
        service_id = diagnostic_session_control.service_id
        sub_function = diagnostic_session_control.DiagnosticSessionType.DEFAULT_SESSION
        session_control_data = [service_id, sub_function]

        valid_session_control_responses = [0x50, 0x7F]

        def is_valid_response(message):
            return (len(message.data) >= 2 and
                    message.data[1] in valid_session_control_responses)

        found_arbitration_ids = []

        with IsoTp(None, None, self.bus) as tp:
            blacklist = set(blacklist_args)
            # Perform automatic blacklist scan
            if auto_blacklist_duration > 0:
                auto_bl_arb_ids = auto_blacklist(tp.bus,
                                                 auto_blacklist_duration,
                                                 is_valid_response,
                                                 print_results)
                blacklist |= auto_bl_arb_ids

            # Prepare session control frame
            sess_ctrl_frm = tp.get_frames_from_message(session_control_data)
            send_arb_id = min_id - 1
            while send_arb_id < max_id:
                send_arb_id += 1
                if print_results:
                    print("\rSending Diagnostic Session Control to 0x{0:04x}"
                          .format(send_arb_id), end="")
                    sys.stdout.flush()
                # Send Diagnostic Session Control
                tp.transmit(sess_ctrl_frm, send_arb_id, None)
                end_time = time.time() + delay
                # Listen for response
                while time.time() < end_time:
                    msg = tp.bus.recv(0)
                    if msg is None:
                        # No response received
                        continue
                    if msg.arbitration_id in blacklist:
                        # Ignore blacklisted arbitration IDs
                        continue
                    if is_valid_response(msg):
                        # Valid response
                        if verify:
                            # Verification - backtrack the latest IDs and
                            # verify that the same response is received
                            verified = False
                            # Set filter to only receive messages for the
                            # arbitration ID being verified
                            tp.set_filter_single_arbitration_id(msg.arbitration_id)
                            if print_results:
                                print("\n  Verifying potential response from "
                                      "0x{0:04x}".format(send_arb_id))
                            verify_id_range = range(send_arb_id,
                                                    send_arb_id - VERIFICATION_BACKTRACK,
                                                    -1)
                            for verify_arb_id in verify_id_range:
                                if print_results:
                                    print("    Resending 0x{0:0x}... "
                                          .format(verify_arb_id), end=" ")
                                tp.transmit(sess_ctrl_frm,
                                            verify_arb_id,
                                            None)
                                verification_end_time = (time.time()
                                                         + delay
                                                         + VERIFICATION_EXTRA_DELAY)
                                while time.time() < verification_end_time:
                                    verification_msg = tp.bus.recv(0)
                                    if verification_msg is None:
                                        continue
                                    if is_valid_response(verification_msg):
                                        # Verified
                                        verified = True
                                        send_arb_id = verify_arb_id
                                        break
                                if print_results:
                                    # Print result
                                    if verified:
                                        print("Success")
                                    else:
                                        print("No response")
                                if verified:
                                    # Verification succeeded - stop checking
                                    break
                            # Remove filter after verification
                            tp.clear_filters()
                            if not verified:
                                # Verification failed - move on
                                if print_results:
                                    print("  False match - skipping")
                                continue
                        if print_results:
                            if not verify:
                                # Blank line needed
                                print()
                            print("Found diagnostics server "
                                  "listening at 0x{0:04x}, "
                                  "response at 0x{1:04x}"
                                  .format(send_arb_id, msg.arbitration_id))
                        # Add found arbitration ID pair
                        found_arb_id_pair = (send_arb_id,
                                             msg.arbitration_id)
                        found_arbitration_ids.append(found_arb_id_pair)
            if print_results:
                print()
        return found_arbitration_ids

    def service_discovery(self, arb_id_request, arb_id_response, timeout,
                          min_id=BYTE_MIN, max_id=BYTE_MAX, print_results=True):
        found_services = []

        with IsoTp(arb_id_request=arb_id_request,
                   arb_id_response=arb_id_response,
                   bus=self.bus
                   ) as tp:
            # Setup filter for incoming messages
            tp.set_filter_single_arbitration_id(arb_id_response)
            # Send requests
            try:
                for service_id in range(min_id, max_id + 1):
                    tp.send_request([service_id])
                    if print_results:
                        print("\rProbing service 0x{0:02x} ({0}/{1}): found {2}"
                              .format(service_id, max_id, len(found_services)),
                              end="")
                    sys.stdout.flush()
                    # Get response
                    msg = tp.bus.recv(timeout=timeout)
                    if msg is None:
                        # No response received
                        continue
                    # Parse response
                    if len(msg.data) > 3:
                        # Since service ID is included in the response, mapping is correct even if response is delayed
                        response_id = msg.data[1]
                        response_service_id = msg.data[2]
                        status = msg.data[3]
                        if response_id != Constants.NR_SI:
                            request_id = Iso14229_1.get_service_request_id(response_id)
                            found_services.append(request_id)
                        elif status != NegativeResponseCodes.SERVICE_NOT_SUPPORTED:
                            # Any other response than "service not supported" counts
                            found_services.append(response_service_id)
                if print_results:
                    print("\nDone!\n")
            except KeyboardInterrupt:
                if print_results:
                    print("\nInterrupted by user!\n")
        return found_services
