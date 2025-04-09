import random
import os

mph = "gmsh1752_reexported.mphtxt"
csv = "tICsgmsh1752.csv"
data_dir = os.path.expanduser(os.path.join("~", ".local", "share"))

par = (
    ("includeImmuno", "fix", "false"),
    ("k1", "rnd", 1.1574e-6, 3.9884e-06),
    ("kd", "fix", 2.9981e+04),
    ("k_on", "fix", 1.1574E-8),
    ("K_T", "fix", 1.2731E-6),
    ("k_th_tumor", "rnd", 7.5231e-12, 7.5231e-10),
    ("location_2", "fix", 9.01),
    ("location_3", "fix", 11.01),
    ("location", "fix", 7.01),
    ("Lp", "rnd", 1.56e-8, 5e-7),
    ("miTumor", "rnd", 5, 50),
    ("Per", "fix", 4.16e-9),
    ("pv", "rnd", 0.6666, 6.6661),
    ("sf", "fix", 0.136),
    ("Sv", "rnd", 5000, 20000),
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
            if type == "rnd":
                b, = rest
                f.write("""\
    <%s>%.16e</%s>
""" % (name, random.uniform(a, b), name))
            elif type == "fix":
                if isinstance(a, str):
                    f.write("""\
    <%s>%s</%s>
""" % (name, a, name))
                else:
                    f.write("""\
    <%s>%.16e</%s>
""" % (name, a, name))
            else:
                assert False
        f.write("""\
  </Parameters>
</MSolve4Korali>
""")
