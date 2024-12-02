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

color = {
    "4T1": "r",
    "B16F10": "g",
    "MCA205": "b",
    "E0771": "m",
}


def convert(key):
    return True if key.text == "true" else False if key.text == "false" else float(
        key.text)


def read11(path):
    for status_path in glob.glob(
            os.path.join(path, "[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]",
                         "status")):
        dirname = os.path.dirname(status_path)
        root = ET.parse(os.path.join(dirname, "MSolveInput.xml"))
        params = {key.tag: convert(key) for key in root.find('./Parameters')}
        volume_path = os.path.join(dirname, "tumorVolume_AnalysisNo_1.txt")
        time_path = os.path.join(dirname,
                                 "timeStepTotalTimes_AnalysisNo_1.txt")
        with open(status_path) as status_file, open(
                volume_path) as volume_file, open(time_path) as time_file:
            status = int(status_file.read())
            volume = []
            time = []
            for t, v in zip(time_file.read().split(),
                            volume_file.read().split()):
                if v == "0.000000E+000":
                    break
                time.append(float(t))
                volume.append(float(v))
        yield params, time, volume, status, status_path


def experiment(path):
    if openpyxl is None:
        raise ModuleNotFoundError(
            "utils.experiment needs `openpyxl' python package")
    w = openpyxl.load_workbook(path)

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
    return D
