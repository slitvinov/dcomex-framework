import random
import os

mph = "RealisticMeshWithTetElements.mphtxt"
csv = "t_ICs_realisticMesh_AdvancedModel.csv"
data_dir = os.path.expanduser(os.path.join("~", ".local", "share"))

par = (
    ("miTumor", "rnd", 5, 50),  #
    ("k_th_tumor", "rnd", 7.5231e-12, 7.5231e-10),
    ("pv", "rnd", 0.6666, 6.6661),
    ("Sv", "rnd", 5000, 20000),
    ("k1", "rnd", 1.1574e-6, 3.9884e-06),
    ("Lp", "rnd", 1.56e-8, 7.47e-6),
    ("sf", "fix", 0.136, 0.146),
    ("Per", "fix", 4.16e-9, 6.225e-8),
    ("K_T", "fix", 1.2731E-6, 1.2731E-4),
    ("k_on", "fix", 1.1574E-8, 1.1574E-2),
    ("kd", "fix", 2.9981e+04, 9.2966e+04),
    ("location", "fix", 25, 30),
)

random.seed(12345)
n = 10
for i in range(n):
    dir = "%08d" % i
    os.makedirs(dir, exist_ok=True)
    print(os.path.join(dir, "MSolveInput.xml"))
    with open(os.path.join(dir, "MSolveInput.xml"), "w") as f:
        f.write("""\
<MSolve4Korali version="1.0">
  <Mesh>
    <MeshFile>%s</MeshFile>
    <InitialConditionsFile>%s</InitialConditionsFile>
  </Mesh>
  <Physics type="TumorGrowthFull" isCSparse="false" />
  <Parameters>
""" % (os.path.join(data_dir, mph), os.path.join(data_dir, csv)))
        for name, type, a, b, *rest in par:
            if type == "rnd":
                f.write("""\
    <%s>%.16e</%s>
""" % (name, random.uniform(a, b), name))
            elif type == "fix":
                f.write("""\
    <%s>%.16e</%s>
""" % (name, a, name))
            else:
                assert False
        f.write("""\
  </Parameters>
</MSolve4Korali>
""")

