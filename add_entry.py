import base64
import re
import requests

from io import BytesIO
from pyzbar.pyzbar import decode
from PIL import Image
from entry import Entry
from urllib.parse import unquote


def openAsBase64Image(base64string):
    if "data:image" in base64string:
        base64string = re.search("data:image/.*;base64,(.*)", base64string).group(1)
    return Image.open(BytesIO(base64.b64decode(base64string)))


def openFromPath(path):
    if "http" in path:
        res = requests.get(path)
        return Image.open(BytesIO(res.content))
    return Image.open(path)


def entryFromQR(image):
    res = unquote(decode(image)[0].data.decode('utf-8'))
    regex_res = re.search("//(.*)/(.*)\?secret=(.*)&issuer=(.*)&algorithm=(.*)&digits=(\d*)&period=(\d*)", res)
    qr_type, label, secret, issuer, algo, digits, period = regex_res.groups()

    return Entry(label, issuer, secret, algo, digits, qr_type)


def writeToFile(entry):
    file = open("SECRETS", "a")
    file.write("\n" + entry.getFileEntry())
