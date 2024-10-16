import paramiko


def ssh_command(ip, port, user, passwd, cmd):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port=port, username=user, password=passwd)

    _, stdout, stderr = client.exec_command(cmd)
    output = stdout.readlines() + stderr.readlines()
    if output:
        print("--- Result ---")
        for line in output:
            print(line.strip())


if __name__ == "__main__":
    import getpass

    user = input("Username: ")
    password = getpass.getpass("Password: ")

    ip = input("IP Address: ") or "192.168.1.203"
    port = input("Port; ") or "id"
    cmd = input("Command: ") or "id"
    ssh_command(ip, port, user, password, cmd)
