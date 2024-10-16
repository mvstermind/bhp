import os
import paramiko
import socket
import sys
import threading


CWD = os.path.dirname(os.path.realpath(__file__))
HOSTKEY = paramiko.RSAKey(filename=os.path.join(CWD, "test_rsa.key"))


class Server(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        if (username == "tim") and (password == "secret"):
            return paramiko.AUTH_SUCCESSFUL


if __name__ == "__main__":
    server = "192.168.1.207"
    ssh_port = 2222
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((server, ssh_port))
        sock.listen(100)
        print("[+] Listening for connections...")
        client, addr = sock.accept()

    except Exception as e:
        print("[-] Issues with listening: " + str(e))
        sys.exit(1)

    else:
        print(f"[+] Recieved connection from {addr}")

    bhSession = paramiko.Transport(client)
    bhSession.add_server_key(HOSTKEY)
    server = Server()
    bhSession.start_server(server=server)

    chan = bhSession.accept(20)
    if chan is None:
        print("*** No channel.")
        sys.exit(1)

    print("[+] Authorized!")
    print(chan.recv(1024).decode())
    chan.send("Welcome in bh_ssh")
    try:
        while True:
            command = input("Give a command:")
            if command != "exit":
                r = chan.recv(8192)
                print(r.decode())
            else:
                chan.send("exit")
            print("END")
            bhSession.close()
            break
    except KeyboardInterrupt:
        bhSession.close()
