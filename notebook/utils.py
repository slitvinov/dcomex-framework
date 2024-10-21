import itertools
import math
import os
import re
import sys
import tarfile
import xml.etree.ElementTree as ET
import glob


def convert(key):
    return True if key.text == "true" else False if key.text == "false" else float(
        key.text)


def fix_time(time):
    t = 0
    n = len(time)
    ans = [0]
    for i in range(n - 1):
        dt = time[i + 1] - time[i]
        if i > 0 and not math.isclose(dt, prev):
            t += prev
        else:
            t += dt
        ans.append(t)
        prev = dt
    return ans


def read(path):
    root = ET.parse(path)
    params = [
        float(root.find('./Parameters/' + key).text)
        for key in ("k1", "mu", "svTumor")
    ]
    root = ET.parse(os.path.join(os.path.dirname(path), "MSolveOutput-x.xml"))
    time, volume = zip(
        *[[float(t.get("time")), float(t.text)]
          for t in root.findall("./TumorVolumes/TumorVolume")])
    return params, fix_time(time), volume


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
        yield params, time, volume, status
