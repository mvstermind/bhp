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


def proxy_hanlder(client_socket, remote_host, remote_port, recieve_first):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    if recieve_first:
        remote_buffer = response_handler(remote_socket)
        hexdump(remote_buffer)

    remote_buffer = response_handler(remote_buffer)
    if len(remote_buffer):
        print("[<==] Sent %d bytes to local host" % len(remote_buffer))
        client_socket.send(remote_buffer)

    while True:
        local_buffer = recieve_from(client_socket)
        if len(local_buffer):
            line = "[<==] Recieved %d bytes from local host" % len(local_buffer)
            print(line)
            hexdump(local_buffer)

            local_buffer = request_hanlder(local_buffer)
            remote_socket.send(local_buffer)

        remote_buffer = recieve_from(remote_socket)
        if len(remote_buffer):
            print("[<==] Recieved %d bytes from remote host" % len(remote_buffer))
            hexdump(remote_buffer)

            remote_buffer = response_handler(remote_buffer)
            client_socket.send(remote_buffer)

        if not len(local_buffer) or not len(remote_buffer):
            client_socket.close()
            remote_socket.close()
            print("[*] There is no more data. Closing the connection")
            break
