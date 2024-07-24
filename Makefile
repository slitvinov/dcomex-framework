.POSIX:
.SUFFIXES:
.SUFFIXES: .sh
PY = python3
PREFIX = /usr
USER = 0
ARCH = x64

M = \
follow.py\
graph.py\
kahan.py\
pyproject.toml\
remote.py\
setup.cfg\

B = \
bin/bio\
bin/ode2vtk\
bin/time2volume\

all: lbin lib
lbin: $B
	mkdir -p -- '$(PREFIX)/bin'
	for i in $B; do cp -- "$$i" '$(PREFIX)/bin' || exit 2; done

lib: $M
	'$(PY)' -m pip install .

ldotnet:
	mkdir -p -- '$(PREFIX)/bin' && \
	case '$(ARCH)' in \
	    x64) wget -q https://download.visualstudio.microsoft.com/download/pr/e94bb674-1fb1-4966-b2f0-bc9055ea33fc/428b37dee8ffb641fd1e45b401b2994c/dotnet-sdk-6.0.424-linux-x64.tar.gz && \
		 tar zxf dotnet-sdk-6.0.424-linux-x64.tar.gz -C '$(PREFIX)/bin' ;; \
	    arm64) wget -q https://download.visualstudio.microsoft.com/download/pr/5f4b8e71-b03a-45cb-9a81-3cfcb51ef346/eb9509f0a061be1106689c1fbf5d5169/dotnet-sdk-6.0.424-linux-arm64.tar.gz && \
		   tar zxf dotnet-sdk-6.0.424-linux-arm64.tar.gz -C '$(PREFIX)/bin' ;; \
	    *) printf "error: unknown arch '%s'\n" '$(ARCH)'; \
	       exit 1 ;; \
	esac

lmsolve:
	mkdir -p -- '$(PREFIX)/share'
	cp -- \
	msolve/CSparse.dll \
	msolve/DotNumerics.dll \
	msolve/MGroup.Constitutive.ConvectionDiffusion.dll \
	msolve/MGroup.Constitutive.Structural.dll \
	msolve/MGroup.FEM.ConvectionDiffusion.dll \
	msolve/MGroup.FEM.dll \
	msolve/MGroup.FEM.Structural.dll \
	msolve/MGroup.LinearAlgebra.Distributed.dll \
	msolve/MGroup.LinearAlgebra.dll \
	msolve/MGroup.MSolve4Korali.dll \
	msolve/MGroup.MSolve4Korali.runtimeconfig.json \
	msolve/MGroup.MSolve.Core.dll \
	msolve/MGroup.NumericalAnalyzers.Discretization.dll \
	msolve/MGroup.NumericalAnalyzers.dll \
	msolve/MGroup.Solvers.dll \
	msolve/Triangle.dll \
	msolve/RealisticMeshWithTetElements.mphtxt \
	msolve/t_ICs_realisticMesh_AdvancedModel.csv \
	msolve/RealisticMeshWithTetElements_TumorCoordinates.csv \
	'$(PREFIX)/share'

lkorali:
	cd korali && make 'USER = $(USER)' install

.sh:
	sed \
	-e 's,%mph%,"$(PREFIX)"/share/RealisticMeshWithTetElements.mphtxt,g' \
	-e 's,%csv%,"$(PREFIX)"/share/t_ICs_realisticMesh_AdvancedModel.csv,g' \
	-e 's,%dll%,"$(PREFIX)"/share/MGroup.MSolve4Korali.dll,g' \
	$< > $@
	chmod a+x $@
