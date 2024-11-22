import random
import os
import itertools

mph = "gmsh1752_reexported.mphtxt"
csv = "tICsgmsh1752.csv"
data_dir = os.path.expanduser(os.path.join("~", ".local", "share"))

par = (
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
l1l = 7, 8, 9, 10, 11
l2l = 8, 9, 10, 12
l3l = 9, 10, 13
random.seed(12345)
i = 0
for j in range(100):
    Val = {}
    for name, type, a, *rest in par:
        if type == "rnd":
            b, = rest
            Val[name] = random.uniform(a, b)
        elif type == "fix":
            Val[name] = a if isinstance(a, str) else "%.16e" % a
    for l1, l2, l3 in itertools.product(l1l, l2l, l3l):
        if l1 < l2 < l3:
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
                for name, *rest in par:
                    f.write("""\
    <%s>%s</%s>
""" % (name, Val[name], name))
                for name, a in ("location", l1), ("location_2",
                                                  l2), ("location_3", l3):
                    f.write("""\
    <%s>%.16e</%s>
""" % (name, a, name))
                f.write("""\
  </Parameters>
</MSolve4Korali>
""")
                i += 1
