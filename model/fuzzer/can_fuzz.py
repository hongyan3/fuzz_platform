import random
import time
from sys import stdout

from model.utils.common import *
from model.constants import *

MIN_DATA_LENGTH = 1
MAX_DATA_LENGTH = 8
DEFAULT_SEED_MAX = 2 ** 16
DELAY_BETWEEN_MESSAGES = 0.01


def directive_str(arb_id, data):
    data = list_to_hex_str(data, "")
    directive = "{0:03X}#{1}".format(arb_id, data)
    return directive


def parse_directive(directive):
    segments = directive.split("#")
    arb_id = int(segments[0], 16)
    data_str = segments[1]
    data = [int(data_str[i:i + 2], 16) for i in range(0, len(data_str), 2)]
    return arb_id, data


def write_directive_to_file_handle(file_handle, arb_id, data):
    directive = directive_str(arb_id, data)
    file_handle.write("{0}\n".format(directive))


def set_seed(seed=None):
    if seed is None:
        seed = random.randint(0, DEFAULT_SEED_MAX)
    print("Seed: {0} (0x{0:x})".format(seed))
    random.seed(seed)


def get_random_arb_id(min_id, max_id):
    arb_id = random.randint(min_id, max_id)
    return arb_id


def get_random_data(min_length, max_length):
    data_length = random.randint(min_length, max_length)
    data = []
    for _ in range(data_length):
        data_byte = random.randint(BYTE_MIN, BYTE_MAX)
        data.append(data_byte)
    return data


class CanFuzzer:
    def __init__(self, can_interface):
        self.__can_bus = can_interface

    def random_fuzz(self, static_arb_id=None, static_data=None, filename=None, min_id=ARBITRATION_ID_MIN,
                    max_id=ARBITRATION_ID_MAX, min_data_length=MIN_DATA_LENGTH, max_data_length=MAX_DATA_LENGTH,
                    start_index=0, show_status=True, seed=None):

        if static_arb_id is not None and static_data is not None:
            raise ValueError("Both static arbitration ID and static data cannot be set at the same time")
        if not 0 <= min_id < max_id <= ARBITRATION_ID_MAX:
            raise ValueError("Invalid value for min_id and/or max_id")
        if not MIN_DATA_LENGTH <= min_data_length <= max_data_length <= MAX_DATA_LENGTH:
            raise ValueError("Invalid value for min_data_length ({0}) and/or max_data_length ({1})".format(
                min_data_length, max_data_length))
        if static_data is not None and len(static_data) > MAX_DATA_LENGTH:
            raise ValueError("static_data ({0} bytes) must not be more than {1} bytes long".format(
                len(static_data), MAX_DATA_LENGTH))
        if not 0 <= start_index:
            raise ValueError("Invalid start index '{0}', must be 0 or larger".format(start_index))

        # Seed handling
        set_seed(seed)

        arb_id = None
        data = None
        file_logging_enabled = filename is not None
        output_file = None

        try:
            if file_logging_enabled:
                output_file = open(filename, "a")
            with self.__can_bus as bus:
                current_index = 0
                messages_sent = 0
                if show_status:
                    print("Starting at index {0}\n".format(start_index))
                # Fuzzing logic
                while True:
                    # Set arbitration ID
                    if static_arb_id is None:
                        # Use a random arbitration ID
                        arb_id = get_random_arb_id(min_id, max_id)
                    else:
                        # Use the static arbitration ID
                        arb_id = static_arb_id
                    # Set data
                    if static_data is None:
                        data = get_random_data(min_data_length, max_data_length)
                    else:
                        data = static_data
                    # If start index is not reached yet, continue without sending and sleeping
                    if current_index < start_index:
                        current_index += 1
                        continue
                    if show_status:
                        print("\rMessages sent: {0}, index: {1}".format(messages_sent, current_index), end="")
                        stdout.flush()
                    # Send message
                    self.__can_bus.send(data=data, arb_id=arb_id)
                    messages_sent += 1
                    # Log to file
                    if file_logging_enabled:
                        write_directive_to_file_handle(output_file, arb_id, data)
                    time.sleep(DELAY_BETWEEN_MESSAGES)
                    current_index += 1
        except IOError as e:
            print("ERROR: {0}".format(e))
        finally:
            if output_file is not None:
                output_file.close()

    def bruteforce_fuzz(self, arb_id, initial_data, data_bitmap, filename=None, start_index=0, show_progress=True,
                        show_responses=True):
        pass
