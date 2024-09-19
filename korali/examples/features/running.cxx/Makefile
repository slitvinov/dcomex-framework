P != python -m site --user-site
FLAGS_PYTHON != python3-config --cflags --libs --embed
MPI4PY_DIR != dirname -- "`$(PY) -c 'import mpi4py; print(mpi4py.__file__)'`"
CXXFLAGS_MPI4PY = -I'$(MPI4PY_DIR)'/include

MPICXX = mpicxx
run-tmcmc: run-tmcmc.cpp _model/heat2d.cpp
	$(MPICXX) $(CXXFLAGS) $(CXXFLAGS_MPI4PY) -std=c++17 -fPIE run-tmcmc.cpp _model/heat2d.cpp -o $@ -Wl,-R'$P/korali' -I'$P/korali' -L'$P/korali' -lkorali $(FLAGS_PYTHON)
run-tmcmc: _model/heat2d.h
