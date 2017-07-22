#!/usr/bin/python3
from collections import namedtuple
import random

all_diacritics = []

INPUT_FILE=None

# Extends the concept of a "character" to include unicode dates
class UnicodeChar:
    def __init__(self, code, version):
        self.char = chr(code)
        self.code = code
        self.version = version

    def __hex__(self):
        return str(code, 16)

    def __str__(self):
        return self.char

    def __repr__(self):
        TEMPLATE = "{UnicodeChar {char}char (hex: {code})}"
        return TEMPLATE.format(char=self.char, code=self.code)

# take input file, and read it into memory
def read_diacritics(file_name):
    with open(file_name, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for line in reader:
            # line[0]: the char code
            # line[1]: first unicode version
            diacritics.append(UnicodeChar(line[0], line[1]))

# Builds all diacritics as known at time of writing (July 2017)
# Source: https://en.wikipedia.org/wiki/Combining_character
def build_diacritics():
    DIACRITICS = [
        (range(0x0300, 0x036F), 4.1),
        (range(0x1DC0, 0x1DFF), 5.2),
        (range(0x20D0, 0x20FF), 5.1),
        (range(0xFE20, 0xFE2F), 8.0)
    ]
    for code_range, version in DIACRITICS:
        for code in code_range:
            all_diacritics.append(UnicodeChar(code, version))

# actually write the diacritics
# line: line to write diacritics to
# percentage: what percentage (0 to 1 inclusive) of accents to add
# version: max version to support (0 = latest)
def write_diacritics(line, percentage=1, version=0):
    output = ""
    if version > 0:
        # filter any UnicodeChar's (uc) with versions too high.
        diacritics = list(filter(lambda uc:(uc.version <= version), all_diacritics))
    else:
        diacritics = all_diacritics

    for char in line:
        num_diacritics = int(len(diacritics)*percentage)

        random.shuffle(diacritics)

        output += char
        for i in range(num_diacritics):
            output += str(diacritics[i])
    return output

def console():
    text = input("Text to accentize: ")

    version = input("Maximum Unicode Version (leave blank for latest): ")
    try:
        version = float(version)
    except ValueError:
        version = 0

    percentage = input("Percentage of available diacritics to use (0-100 inclusive): ")
    percentage.replace('%', '')
    try:
        percentage = int(percentage) / 100
    except ValueError:
        percentage = 1
    
    print(write_diacritics(text, percentage=percentage, version=version))
    
if __name__ == '__main__':
    if INPUT_FILE:
        read_diacritics(INPUT_FILE)
    else:
        build_diacritics()
    console()
