import sys
import socket
import threading

HEX_FILTER = "".join([(len(repr(chr(i))) == 3) and chr(i) or "." for i in range(256)])


def hexdump(src, length=16, show=True):
    if isinstance(src, bytes):
        src = src.decode()
    results = list()
    for i in range(0, len(src), length):
        word = str(src[i : i + length])
        printable = word.translate(HEX_FILTER)
        hexa = " ".join([f"{ord(c):02X}" for c in word])
        hexwidth = length * 3
        results.append(f"{i:04} {hexa:<{hexwidth}} {printable}")
    if show:
        for line in results:
            print(line)
    else:
        return results


def recieve_from(connection):
    buffer = b""
    connection.settimeout(5)
    try:
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buffer += data
    except Exception as e:
        print("Error: ", e)
        pass
    return buffer


def request_hanlder(buffer):
    return


def response_handler(buffer):
    return
