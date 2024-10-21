import openpyxl
import re

tstart = {
    "4T1": 10,
    "B16F10": 10,
    "MCA205": 4,
    "E0771": 7,
}
w = openpyxl.load_workbook("data.xlsx")


def get():
    D = ((t.value, s[t.row][c.column - 1].value) for t in Time)
    D = ((time, volume) for time, volume in D if volume is not None)
    return zip(*D)


D = {}
for s in w:
    for v in s["B"]:
        if v.value == 0:
            row = v.row
    Time = [t for t in s["B"][row - 1:]]
    for c in s[row - 1][2:]:
        if c.value is not None:
            name = c.value.lower()
            if re.match("^control", name):
                time, volume = get()
                D[s.title, name] = time, volume
            elif re.match("^apdl", name):
                time, volume = get()
                D[s.title, name] = time, volume
print(D)
