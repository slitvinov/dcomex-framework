import random
import os

mph = "gmsh1752_reexported.mphtxt"
csv = "tICsgmsh1752.csv"
data_dir = os.path.expanduser(os.path.join("~", ".local", "share"))

par = (
    ("location", "fix", 7.01),
    ("location_2", "fix", 9.01),
    ("location_3", "fix", 11.01),
    ("includeImmuno", "fix", "true"),
    ("useSingleImmunoTherapy", "fix", "false"),
    ("miTumor", "rnd", 5, 50),
    ("k_th_tumor", "rnd", 7.5231e-12, 7.5231e-10),
    ("pv", "rnd", 0.6666, 6.6661),
    ("Sv", "rnd", 5000, 20000),
    ("k1", "rnd", 1.1574e-6, 3.9884e-06),
    ("Lp", "rnd", 1.56e-8, 5e-7),
    ("sf", "rnd", 0.136, 0.146),
    ("Per", "rnd", 4.16e-9, 6.225e-8),
    ("K_T", "rnd", 1.2731E-6, 1.2731E-4),
    ("k_on", "rnd", 1.1574E-8, 1.1574E-2),
    ("kd", "rnd", 2.9981e+04, 9.2966e+04),
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
