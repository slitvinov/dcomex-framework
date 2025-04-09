import random
import os

mph = "gmsh1752_reexported.mphtxt"
csv = "tICsgmsh1752.csv"
data_dir = os.path.expanduser(os.path.join("~", ".local", "share"))

par = (
    ("includeImmuno", "fix", "true"),
    ("k1", "uniform", 1.1574e-6, 3.9884e-06),
    ("kd", "uniform", 2.9981e+04, 9.2966e+04),
    ("keepLogs", "fix", "true"),
    ("k_on", "uniform", 1.1574e-8, 1.1574e-2),
    ("k_th_tumor", "uniform", 7.5231e-12, 7.5231e-10),
    ("K_T", "uniform", 1.2731e-6, 1.2731e-4),
    ("location_2", "choice", (6, 7, 8)),
    ("location_3", "choice", (9, 10, 11)),
    ("location", "choice", (3, 4, 5)),
    ("Lp", "uniform", 1.56e-8, 5e-7),
    ("miTumor", "uniform", 5, 50),
    ("Per", "uniform", 4.16e-9, 6.225e-8),
    ("pv", "uniform", 0.6666, 6.6661),
    ("sf", "uniform", 0.136, 0.146),
    ("Sv", "uniform", 5000, 20000),
    ("useSingleImmunoTherapy", "fix", "false"),
)
random.seed(12345)
for i in range(1024):
    dir = "%08d" % i
    os.makedirs(dir, exist_ok=True)
    print(os.path.join(dir, "MSolveInput.xml"))
    with open(os.path.join(dir, "MSolveInput.xml"), "w") as f:
        f.write("""\
<MSolve4Korali version="1.0">
  <Paths>
    <OutputDir>./</OutputDir>
  </Paths>
  <Mesh>
    <MeshFile>%s</MeshFile>
    <InitialConditionsFile>%s</InitialConditionsFile>
  </Mesh>
  <Physics type="TumorGrowthFull" isCSparse="false" />
  <Output><TumorVolume/></Output>
  <Parameters>
""" % (os.path.join(data_dir, mph), os.path.join(data_dir, csv)))
        for name, type, a, *rest in par:
            if type == "uniform":
                b, = rest
                f.write("""\
    <%s>%.16e</%s>
""" % (name, random.uniform(a, b), name))
            elif type == "fix":
                if isinstance(a, str):
                    f.write("""\
    <%s>%s</%s>
""" % (name, a, name))
            elif type == "choice":
                f.write("""\
    <%s>%s</%s>
""" % (name, random.choice(a), name))
            else:
                assert False
        f.write("""\
  </Parameters>
</MSolve4Korali>
""")
