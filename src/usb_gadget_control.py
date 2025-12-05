import os
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- HID Configuration Data ---
KEY_CODES = {
    'a': 4, 'b': 5, 'c': 6, 'd': 7, 'e': 8, 'f': 9, 'g': 10, 'h': 11, 'i': 12, 'j': 13, 'k': 14, 'l': 15, 'm': 16,
    'n': 17, 'o': 18, 'p': 19, 'q': 20, 'r': 21, 's': 22, 't': 23, 'u': 24, 'v': 25, 'w': 26, 'x': 27, 'y': 28, 'z': 29,
    '1': 30, '2': 31, '3': 32, '4': 33, '5': 34, '6': 35, '7': 36, '8': 37, '9': 38, '0': 39, 'enter': 40,
    ' ': 44, '-': 45, '=': 46, '[': 47, ']': 48, '\\': 49, ';': 51, "'": 52, '`': 53, ',': 54, '.': 55, '/': 56,
}
MODIFIER_CODES = {
    'LCTRL': 1, 'LSHIFT': 2, 'LALT': 4, 'LGUI': 8, 'RCTRL': 16, 'RSHIFT': 32, 'RALT': 64, 'RGUI': 128
}
MODIFIER_CODES['GUI'] = MODIFIER_CODES['LGUI']
SHIFT_MAP = {
    '!': '1', '@': '2', '#': '3', '$': '4', '%': '5', '^': '6', '&': '7', '*': '8', '(': '9', ')': '0', '_': '-', '+': '=',
    '{': '[', '}': ']', '|': '\\', ':': ';', '"': "'", '~': '`', '<': ',', '>': '.', '?': '/'
}

class USBGadget:
    """ Controls the USB gadget functionality on a Raspberry Pi (Simulated). """

    def __init__(self, gadget_name='ai_usb_tool', hid_device_name='hidg0'):
        self.gadget_name = gadget_name
        self.hid_device_name = hid_device_name
        self.base_path = f"/sys/kernel/config/usb_gadget/{self.gadget_name}"

    def _run_command(self, command):
        logging.info(f"SIMULATING EXECUTION: {command}")

    def _write_file(self, path, content):
        logging.info(f"SIMULATING WRITE: '{content}' to {path}")

    def initialize_hid(self):
        logging.info("Initializing HID gadget (simulation)...")
        self._run_command(f"mkdir -p {self.base_path}")
        self._write_file(f"{self.base_path}/idVendor", "0x1d6b")
        self._write_file(f"{self.base_path}/idProduct", "0x0137")
        self._run_command(f"mkdir -p {self.base_path}/strings/0x409")
        # ... other simulated commands

    def unregister_gadget(self):
        logging.info("Unregistering USB gadget (simulation)...")
        self._write_file(f"{self.base_path}/UDC", "")
        # ... other simulated cleanup commands

    def _write_hid_report(self, report):
        logging.info(f"SIMULATING: Writing report {report.hex()} to /dev/{self.hid_device_name}")

    def press_keys(self, keys):
        modifier_byte = 0
        key_codes = [0] * 6
        key_idx = 0
        for key in keys:
            key_upper = key.upper()
            if key_upper in MODIFIER_CODES:
                modifier_byte |= MODIFIER_CODES[key_upper]
            elif key.lower() in KEY_CODES and key_idx < 6:
                key_codes[key_idx] = KEY_CODES[key.lower()]
                key_idx += 1

        report = bytes([modifier_byte, 0] + key_codes)
        self._write_hid_report(report)
        self._write_hid_report(bytes([0] * 8)) # Release keys

    def type_string(self, text):
        logging.info(f"Typing string: {text}")
        for char in text:
            modifier = 0
            key = char
            if 'A' <= char <= 'Z':
                modifier = MODIFIER_CODES['LSHIFT']
                key = char.lower()
            elif char in SHIFT_MAP:
                modifier = MODIFIER_CODES['LSHIFT']
                key = SHIFT_MAP[char]
            elif char == '\n':
                key = 'enter'

            keys_to_press = []
            if modifier: keys_to_press.append('LSHIFT')
            if key: keys_to_press.append(key)

            if keys_to_press: self.press_keys(keys_to_press)
            else: logging.warning(f"Unsupported character: {char}")
            time.sleep(0.05)

if __name__ == '__main__':
    gadget = USBGadget()
    try:
        gadget.initialize_hid()
        time.sleep(2)
        print("--- Testing key combination (GUI+R) ---")
        gadget.press_keys(['GUI', 'r'])
        time.sleep(1)
        print("--- Testing typing a string ---")
        gadget.type_string("powershell\n")
        time.sleep(1)
    finally:
        gadget.unregister_gadget()
