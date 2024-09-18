import itertools
import math
import os
import re
import tarfile
import xml.etree.ElementTree as ET

KEYS = set(("miTumor", "k_th_tumor", "pv", "Sv", "k1", "Lp", "sf", "Per",
            "K_T", "k_on", "kd", "location", "totalTimeNoImmuno"))


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
    with tarfile.open(path, 'r') as tar:
        for member in tar.getmembers():
            if re.match("^[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]/status$",
                        member.name):
                dirname = re.sub("/status$", "", member.name)
                root = ET.parse(tar.extractfile(dirname + "/MSolveInput.xml"))
                params = {
                    key.tag: float(key.text)
                    for key in root.find('./Parameters') if key.tag in KEYS
                }
                status = int(tar.extractfile(dirname +
                                          "/status").read().decode('utf-8'))
                volume_file = tar.extractfile(
                    dirname +
                    "/tumorVolume_AnalysisNo_0.txt").read().decode('utf-8')
                time_file = tar.extractfile(
                    dirname +
                    "/timeStepTotalTimes_AnalysisNo_0.txt").read().decode('utf-8')
                volume = [ ]
                time = [ ]
                for t, v in zip(time_file.split(), volume_file.split()):
                    if v == "0.000000E+000":
                        break
                    time.append(float(t))
                    volume.append(float(v))
                yield params, time, volume, status
