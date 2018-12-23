import dmenu
from subprocess import call
from pykeyboard import PyKeyboard
import re
import pyotp

entries = []

class Entry:
    def __init__(self, title, user, secret, type):
        self.id = -1
        self.title = title
        self.user = user
        self.secret = secret
        self.type = type

    def __repr__(self):
        return str(self.id) + ": " + self.title + "\t" + self.user

    def __str__(self):
        return str(self.id) + ": " + self.title + "\t" + self.user

    def setID(self, id):
        self.id = id

    def getTitle(self):
        return self.title

    def getUser(self):
        return self.user

    def getSecret(self):
        return self.secret

    def getType(self):
        return self.type

    def getID(self):
        return self.id

def getAvailableCodes():
    return [str(entry) for entry in entries]

def typeToken(entry):
    totp = pyotp.TOTP(entry.getSecret())
    PyKeyboard().type_string(totp.now())

def parseEntry(line):
    reg = re.search("([^;\n]+);([^;\n]+);([^;\n]+);([^;\n]+)", line)
    return Entry(reg.group(1), reg.group(2), reg.group(3), reg.group(4))

def parseSelection(line):
    return entries[int(re.search("(\d?):", line).group(1)) - 1]


def initEntries():
    with open("SECRETS") as secrets:
        i = 1
        for line in secrets.readlines():
            entry = parseEntry(line)
            entry.setID(i)
            entries.append(entry)
            i = i + 1

def start():
    initEntries()

start()
typeToken(parseSelection(dmenu.show(getAvailableCodes())))
