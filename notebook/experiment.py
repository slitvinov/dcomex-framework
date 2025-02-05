import itertools
import math
import os
import re
import sys
import tarfile
import xml.etree.ElementTree as ET
import glob
try:
    import openpyxl
except ImportError:
    scipy = None

tstart = {
    "4T1": 10,
    "B16F10": 10,
    "MCA205": 4,
    "E0771": 7,
}


path = "data.new.xlsx"
if openpyxl is None:
    raise ModuleNotFoundError(
        "utils.experiment needs `openpyxl' python package")
w = openpyxl.load_workbook(path, data_only=True)

def get():
    D = ((t.value, s[t.row][c.column - 1].value) for t in Time)
    D = ((time, volume) for time, volume in D if volume is not None)
    return zip(*D)

D = {}
Where = "A", "B", "C", "D", "E", "F", "G", "H"

for s in w:
    print(s.title)
    Time = [ ]
    Row = [ ]
    it = iter(s["D"] if s.title == "4T1" else s["C"])
    for v in it:
        if v.value == 0:
            Time = [ 0 ]
            break
    for v in it:
        if v.value == None:
            break
        Time.append(v.value)
        Row.append(v.row)
    where = iter(Where)
    for x in where:
        if s[x][0].value != None and re.match("^Time[ ]*", s[x][0].value):
            break
    else:
        assert 0

    for i in range(4):
        volume = [ ]
        x = next(where)
        for row in Row:
            volume.append(s[x][row].value)
        print(Time, volume)
    continue
    exit(0)
    for c in s[row - 1][2:]:
        if c.value is not None:
            name = c.value.lower()
            if re.match("^control", name):
                time, volume = get()
                D[s.title, name] = time, volume
            elif re.match("^apdl", name):
                time, volume = get()
                D[s.title, name] = time, volume
    exit(0)
# print(D)
