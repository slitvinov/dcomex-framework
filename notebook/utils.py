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
    w = openpyxl.load_workbook(path, data_only=True)
    D = {}
    Where = "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"
    for s in w:
        Time = []
        it = iter(s["D"] if s.title == "4T1" else s["C"])
        for v in it:
            if v.value == 0:
                Time = [0]
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
            volume = []
            x = next(where)
            for row in Row:
                volume.append(s[x][row - 1].value)
            D[s.title, "control_%d" % i] = Time, volume
    return D
