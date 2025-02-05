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
D = {}
Where = "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"
for s in w:
    Time = [ ]
    it = iter(s["D"] if s.title == "4T1" else s["C"])
    for v in it:
        if v.value == 0:
            Time = [ 0 ]
            Row = [v.row]
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
            volume.append(s[x][row - 1].value)
        D[s.title, "control_%d" % i] = Time, volume
print(D)
