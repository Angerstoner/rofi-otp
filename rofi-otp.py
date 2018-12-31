import dmenu
import re
from pyotp import TOTP
from rofi import Rofi
from pykeyboard import PyKeyboard
from entry import Entry
from addEntry import entryFromQR, openFromPath, openAsBase64Image, writeToFile

menu = "rofi"
entries = []


def showInDMenu(entries, prompt="Entries", mode="selection"):
    return dmenu.show(entries, prompt=prompt)


def showInRofi(entries, prompt="Entries", mode="selection"):
    if (mode == "prompt"):
        return Rofi().text_entry(prompt)
    index, key = Rofi().select(prompt, entries)
    return entries[index]

menus = {
    "dmenu": showInDMenu,
    "rofi": showInRofi
}

def getAvailableCodes():
    return [str(entry) for entry in entries]


def typeToken(entry):
    totp = TOTP(entry.getSecret())
    PyKeyboard().type_string(totp.now())


def parseEntry(line):
    reg = re.search("([^;\n]+);([^;\n]+);([^;\n]+);([^;\n]+);(\d);([^;\n]+)", line)
    return Entry(reg.group(1), reg.group(2), reg.group(3), reg.group(4), reg.group(5), reg.group(6))


def parseSelection(line):
    return entries[int(re.search("(\d+):", line).group(1)) - 1]


def addEntry():
    add_by_qr_path = "Add by QR-Code (path/url)"
    add_by_qr_image = "Add by QR-Code (base64 image)"
    add_manually = "Add manually"
    selection = menus[menu]([add_by_qr_path, add_by_qr_image, add_manually])
    if selection == add_by_qr_path:
        path = menus[menu]([], "Please enter the image path", "prompt")
        new_entry = entryFromQR(openFromPath(path))
    elif selection == add_by_qr_image:
        data = menus[menu]([], "Please enter the image data in base64 encoding", "prompt")
        new_entry = entryFromQR(openAsBase64Image(data))
    else:
        new_entry = Entry(None, None, None, None, None, None)
        print("not implemented")
    writeToFile(new_entry)


def editEntry():
    print("EDIT")


def showEntry():
    print("SHOW")


entryOptions = {
    "Add": addEntry,
    "Edit": editEntry,
    "Show": showEntry
}


def initEntries():
    with open("SECRETS") as secrets:
        i = 1
        for line in secrets.readlines():
            entry = parseEntry(line)
            entry.setID(i)
            entries.append(entry)
            i = i + 1


def openMenu():
    menulines = ["Add", "Edit", "Show"]
    for entry in getAvailableCodes():
        menulines.append(entry)
    return menus[menu](menulines)


def start():
    initEntries()
    selection = openMenu()
    if selection in entryOptions:
        entryOptions[selection]()
    else:
        typeToken(parseSelection(selection))


start()

