P != python -m site --user-site
I != python3-config --cflags --libs
MPICXX = mpicxx
run-tmcmc: run-tmcmc.cpp _model/heat2d.cpp
	$(MPICXX) $(CXXFLAGS) run-tmcmc.cpp _model/heat2d.cpp -o $@ -Wl,-R'$P/korali' -I'$P/korali' -L'$P/korali' $I -std=c++17 -fPIE -lkorali -lpython3.9
