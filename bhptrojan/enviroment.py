import os


def run(**args):
    print("[*] In enviroment module.")
    files = os.listdir(".")
    return str(files)
