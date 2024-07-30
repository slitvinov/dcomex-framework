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
                content = tar.extractfile(
                    dirname +
                    "/prescribedTimeSteppingList.txt").read().decode('utf-8')
                dt = []
                nt = []
                for line in content.split("\n"):
                    if line:
                        nt0, dt0 = line.split(",")
                        nt.append(int(nt0))
                        dt.append(float(dt0))

                root = ET.parse(tar.extractfile(dirname + "/MSolveInput.xml"))
                params = {
                    key.tag: float(key.text)
                    for key in root.find('./Parameters') if key.tag in KEYS
                }
                content = tar.extractfile(dirname +
                                          "/status").read().decode('utf-8')
                status = int(content)
                content = tar.extractfile(
                    dirname +
                    "/tumorVolume_AnalysisNo_0.txt").read().decode('utf-8')
                volume = []
                time = []
                j = 0
                t = 0
                cnt = 0
                for v in content.split():
                    if v == "0.000000E+000":
                        break
                    volume.append(float(v))
                    t += dt[j]
                    if cnt == nt[j] - 1 and j < len(nt) - 1:
                        j += 1
                        cnt = 0
                    else:
                        cnt += 1
                    time.append(t)
                yield params, time, volume, status
