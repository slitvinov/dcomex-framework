import tarfile
import re


def read(path):
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
                    t += dt[j]
                    if cnt == nt[j] - 1:
                        j += 1
                        cnt = 0
                    else:
                        cnt += 1
                    volume.append(v)
                    time.append(t)
                yield {}, time, volume


i = read("a.tar.gz")
params, time, volume = next(i)

for t, v in zip(time, volume):
    print(f"{t:.16e} {v}")
