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


while True:
    get_last_input()
    time.sleep(1)
