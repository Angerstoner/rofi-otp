import base64
import re
import requests

from io import BytesIO
from pyzbar.pyzbar import decode
from PIL import Image
from entry import Entry
from urllib.parse import unquote


def openAsBase64Image(base64string):
    img_data = base64.b64encode(base64string.encode())
    filename = "qrbase64temp.png"
    with open(filename, "wb") as fh:
        fh.write(base64.decodebytes(img_data))

    return Image.frombytes('RGB', (256, 256), base64.decodebytes(img_data))


def openFromPath(path):
    if "http" in path:
        res = requests.get(path)
        return Image.open(BytesIO(res.content))
    return Image.open(path)


def entryFromQR(image):
    res = unquote(decode(image)[0].data.decode('utf-8'))
    regex_res = re.search("//(.*)/(.*)\?secret=(.*)&issuer=(.*)&algorithm=(.*)&digits=(\d*)&period=(\d*)", res)
    qr_type, label, issuer, secret, algo, digits, period = regex_res.groups()

    return Entry(label, issuer, secret, algo, digits, qr_type)


def writeToFile(entry):
    file = open("SECRETS", "a")
    file.write("\n" + entry.getFileEntry())

# writeToFile(entryFromQR(openFromPath("qr.png")))
