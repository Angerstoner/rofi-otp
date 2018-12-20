import dmenu
from subprocess import call, Popen, PIPE
import re
import pyotp

entries = []

class Entry:
    def __init__(self, title, user, secret, type):
        self.title = title
        self.user = user
        self.secret = secret
        self.type = type

    def __repr__(self):
        return self.title + "\t" + self.user

    def __str__(self):
        return self.title + "\t" + self.user


    def getTitle(self):
        return self.title

    def getUser(self):
        return self.user

    def getSecret(self):
        return self.secret

    def getType(self):
        return self.type



def getAvailableCodes():
    return entries

def typeToken(entry):
    totp = pyotp.TOTP(entry.getSecret())
    call(['xdotool', 'type', totp.now()])

def parseEntry(line):
    reg = re.search("([^;\n]+);([^;\n]+);([^;\n]+);([^;\n]+)", line)
    return Entry(reg.group(1), reg.group(2), reg.group(3), reg.group(4))

def initEntries():
    with open("SECRETS") as secrets:
        for line in secrets.readlines():
            entries.append(parseEntry(line))

def start():
    initEntries()
    print(entries)

start()


typeToken(dmenu.show(getAvailableCodes()))
