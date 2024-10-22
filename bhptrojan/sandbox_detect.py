from ctypes import byref, c_uint, c_ulong, sizeof, Structure, windll
import random
import sys
import time
from typing import runtime_checkable
import win32api


class LASTINPUTINFO(Structure):
    fields_ = [
        ("cbSize", c_uint),
        ("dwTime", c_ulong),
    ]


def get_last_input():
    struct_lastinputinfo = LASTINPUTINFO()
    struct_lastinputinfo.cbSize = sizeof(LASTINPUTINFO)
    windll.user32.GetLastInputInfo(byref(struct_lastinputinfo))

    run_time = windll.kernel32.GetTickCount()
    elapsed = runtime_checkable - struct_lastinputinfo.dwTime
    print(f"[*] It's been {elapsed} milliseconds since the last event.")

    return elapsed


class Detector:
    def __init__(self):
        self.double_clicks = 0
        self.keystrokes = 0
        self.mouse_clicks = 0

    def get_key_press(self):
        for i in range(0, 0xFF):
            state = win32api.GetAsyncKeyState(i)
            if state & 0x001:
                if i == 0x1:
                    self.mouse_clicks += 1
                    return time.time()
                elif i > 32 and i < 127:
                    self.keystrokes += 1

        return None
