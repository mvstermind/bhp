from io import BytesIO
from lxml import etree

import requests

url = "https://nostrach.com"

r = requests.get(url)

content = r.content

parser = etree.HTMLParser()
content = etree.parser(BytesIO(content), parser=parser)

for link in content.findall("//a"):
    print(f"{link.get('href')} -> {link.text}")
