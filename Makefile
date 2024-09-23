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

all: bin lib
bin: $B
	mkdir -p -- '$(PREFIX)/bin'
	for i in $B; do cp -- "$$i" '$(PREFIX)/bin' || exit 2; done

lib: $M
	'$(PY)' -m pip install .

dotnet:
	mkdir -p -- '$(PREFIX)/bin'
	case '$(ARCH)' in \
	    x64) wget -q https://download.visualstudio.microsoft.com/download/pr/e94bb674-1fb1-4966-b2f0-bc9055ea33fc/428b37dee8ffb641fd1e45b401b2994c/dotnet-sdk-6.0.424-linux-x64.tar.gz && \
		 tar zxf dotnet-sdk-6.0.424-linux-x64.tar.gz -C '$(PREFIX)/bin' ;; \
	    arm64) wget -q https://download.visualstudio.microsoft.com/download/pr/5f4b8e71-b03a-45cb-9a81-3cfcb51ef346/eb9509f0a061be1106689c1fbf5d5169/dotnet-sdk-6.0.424-linux-arm64.tar.gz && \
		   tar zxf dotnet-sdk-6.0.424-linux-arm64.tar.gz -C '$(PREFIX)/bin' ;; \
	    *) printf "error: unknown arch '%s'\n" '$(ARCH)'; \
	       exit 1 ;; \
	esac

msolve:
	mkdir -p -- '$(PREFIX)/share'
	cp -- \
	msolve/Castle.Core.dll \
	msolve/Compute.Bindings.IntelMKL.dll \
	msolve/CSparse.dll \
	msolve/DotNumerics.dll \
	msolve/DrugDeliveryModel.dll \
	msolve/MGroup.Constitutive.ConvectionDiffusion.dll \
	msolve/MGroup.Constitutive.Structural.dll \
	msolve/MGroup.DrugDeliveryModel.Tests.dll \
	msolve/MGroup.Environments.dll \
	msolve/MGroup.FEM.ConvectionDiffusion.dll \
	msolve/MGroup.FEM.dll \
	msolve/MGroup.FEM.Structural.dll \
	msolve/MGroup.LinearAlgebra.Distributed.dll \
	msolve/MGroup.LinearAlgebra.dll \
	msolve/MGroup.MSolve.Core.dll \
	msolve/MGroup.NumericalAnalyzers.Discretization.dll \
	msolve/MGroup.NumericalAnalyzers.dll \
	msolve/MGroup.Solvers.dll \
	msolve/Microsoft.TestPlatform.CommunicationUtilities.dll \
	msolve/Microsoft.TestPlatform.CoreUtilities.dll \
	msolve/Microsoft.TestPlatform.CrossPlatEngine.dll \
	msolve/Microsoft.TestPlatform.PlatformAbstractions.dll \
	msolve/Microsoft.TestPlatform.Utilities.dll \
	msolve/Microsoft.VisualStudio.CodeCoverage.Shim.dll \
	msolve/Microsoft.VisualStudio.TestPlatform.Common.dll \
	msolve/Microsoft.VisualStudio.TestPlatform.ObjectModel.dll \
	msolve/Moq.dll \
	msolve/MPI.dll \
	msolve/Newtonsoft.Json.dll \
	msolve/System.Xml.XPath.XmlDocument.dll \
	msolve/testhost.dll \
	msolve/Triangle.dll \
	msolve/xunit.abstractions.dll \
	msolve/xunit.assert.dll \
	msolve/xunit.core.dll \
	msolve/xunit.execution.dotnet.dll \
	msolve/xunit.runner.reporters.netcoreapp10.dll \
	msolve/xunit.runner.utility.netcoreapp10.dll \
	msolve/xunit.runner.visualstudio.dotnetcore.testadapter.dll \
	msolve/RealisticMeshWithTetElements_t_nodes_initialCs.csv \
	msolve/t_ICs_243tetMesh_AdvancedModel.csv \
	msolve/tICsBiggerRadiusRexported.csv \
	msolve/t_ICs_gmsh1158_cmsl.csv \
	msolve/t_ICs_gmsh1285_cmsl.csv \
	msolve/tICsgmsh1752.csv \
	msolve/t_ICs_gmsh902.csv \
	msolve/t_ICs_realisticMesh_AdvancedModel.csv \
	msolve/t_ICs_realisticMesh_UPDATEDModel.csv \
	msolve/t_nodes_cmsl_Mesh243.csv \
	msolve/DrugDeliveryModel.exe \
	msolve/DrugDeliveryModel.deps.json \
	msolve/DrugDeliveryModel.runtimeconfig.json \
	msolve/MGroup.DrugDeliveryModel.Tests.runtimeconfig.json \
	'$(PREFIX)/share'

korali:
	cd korali && make 'USER = $(USER)' install

.sh:
	sed \
	-e 's,%mph%,"$(PREFIX)"/share/RealisticMeshWithTetElements.mphtxt,g' \
	-e 's,%csv%,"$(PREFIX)"/share/t_ICs_realisticMesh_AdvancedModel.csv,g' \
	-e 's,%dll%,"$(PREFIX)"/share/MGroup.MSolve4Korali.dll,g' \
	$< > $@
	chmod a+x $@

.PHONY: korali msolve lib dotnet bin all
