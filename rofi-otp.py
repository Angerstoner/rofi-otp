import dmenu
import re
from pyotp import TOTP
from rofi import Rofi
from pykeyboard import PyKeyboard
from entry import Entry
from add_entry import entryFromQR, openFromPath, openAsBase64Image, writeToFile

menu = "rofi"
entries = []


def show_in_dmenu(entries, prompt="Entries"):
    return dmenu.show(entries, prompt=prompt)


def show_in_rofi(entries, prompt="Entries", mode="selection"):
    if mode == "prompt":
        return Rofi().text_entry(prompt)
    index, key = Rofi().select(prompt, entries, rofi_args=['-i'])
    return entries[index]


menus = {
    "dmenu": show_in_dmenu,
    "rofi": show_in_rofi
}


def get_available_codes():
    return [str(entry) for entry in entries]


def type_token(entry):
    totp = TOTP(entry.getSecret())
    PyKeyboard().type_string(totp.now())


def parse_entry(line):
    reg = re.search("([^;\n]+);([^;\n]+);([^;\n]+);([^;\n]+);(\d);([^;\n]+)", line)
    return Entry(reg.group(1), reg.group(2), reg.group(3), reg.group(4), reg.group(5), reg.group(6))


def parse_selection(line):
    return entries[int(re.search("(\d+):", line).group(1)) - 1]


def add_entry():
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


def edit_entry():
    print("EDIT")


def show_entry():
    print("SHOW")


entryOptions = {
    "Add": add_entry,
    "Edit": edit_entry,
    "Show": show_entry
}


def init_entries():
    with open("SECRETS") as secrets:
        i = 1
        for line in secrets.readlines():
            entry = parse_entry(line)
            entry.setID(i)
            entries.append(entry)
            i = i + 1


def open_menu():
    menu_lines = ["Add", "Edit", "Show"]
    for entry in get_available_codes():
        menu_lines.append(entry)
    return menus[menu](menu_lines)


def start():
    init_entries()
    selection = open_menu()
    if selection in entryOptions:
        entryOptions[selection]()
    else:
        type_token(parse_selection(selection))


start()
