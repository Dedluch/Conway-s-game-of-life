import re
import numpy as np


def decode(path):
    #opens file, ignores comments and makes every line a string inside a list
    try:
        with open(path) as file:
            lines = [line.strip() for line in file if not line.startswith("#")]
    except OSError:
        return 2
    #splits pattern parameters to a list
    headerLine = lines[0].split(", ")
    #Regex to check for correct filetype
    if not re.match("\s*x\s*=\s*\d+\s*$", headerLine[0]):
        return 1
    elif not re.match("\s*y\s*=\s*\d+\s*$", headerLine[1]):
        return 1
    elif not re.match("\s*rule\s*=\s*B3\/S23\s*$", headerLine[2]):
        return 1

    lines.pop(0)
    encodedRLE = "\n".join(lines)

    width = headerLine[0].lstrip("x = ")
    width = int(width)

    #Whole decoding process
    countTag = ""
    row = []
    pattern = []

    for char in encodedRLE:
        if char.isdigit():
            countTag += char
        elif char == "b" and countTag == "":
            row.append(0)
        elif char == "o" and countTag == "":
            row.append(1)
        elif char == "b":
            row.extend([0] * int(countTag))
            countTag = ""
        elif char == "o":
            row.extend([1] * int(countTag))
            countTag = ""
        elif char == "$" or char == "!":
            if len(row) < width:
                remaining = width - len(row)
                row.extend([0] * remaining)
                pattern.append(row)
                row = []
            else:
                pattern.append(row)
                row = []
    return np.array(pattern)