.POSIX:
.SUFFIXES:
.SUFFIXES: .c
.SUFFIXES: .cpp
.SUFFIXES: .o

PY = python3
MPICXX = mpicxx
LINK = $(MPICXX)
USER = 0
CXXFLAGS_EIGEN3 != pkg-config --cflags eigen3
CXXFLAGS_GSL != pkg-config --cflags gsl
MPI4PY_DIR != dirname -- "`$(PY) -c 'import mpi4py; print(mpi4py.__file__)')`"
CXXFLAGS_MPI4PY = -I'$(MPI4PY_DIR)'/include
CXXFLAGS = -O2 -g
CXXFLAGS_STD = -std=c++17
CXXFLAGS_PYTHON != pkg-config --cflags python3
LDFLAGS_GSL != pkg-config --libs gsl

include obj.mk
include py.mk

libkorali.so: $O
	$(LINK) -shared $O $(LDFLAGS_GSL) $(LDFLAGS_MPI) $(LDFLAGS) -o $@

.c.o:
	$(CC) -c -fPIC $(CFLAGS) $(CFLAGS_MPI) $< -o $@

.cpp.o:
	$(MPICXX) -c -fPIC $(CXXFLAGS_STD) -I. -Isource $(CXXFLAGS_EIGEN3) $(CXXFLAGS_GSL) $(CXXFLAGS_MPI) $(CXXFLAGS_MPI4PY) $(CXXFLAGS_PYBIND11) $(CXXFLAGS_PYTHON) $(CXXFLAGS) $< -o $@


clean:
	rm -f $O libkorali.so

install: libkorali.so $P
	case '$(USER)' in \
	    0) p=`$(PY) -c "import site; print(site.getsitepackages()[0])"` || exit 2 ;; \
	    *) p=`$(PY) -m site --user-site` || exit 2 ;; \
	esac && \
	for i in $P; \
	do d=`dirname -- "$$i"` && \
	   mkdir -p -- "$$p/$$d/" && \
	   cp -- "$$i" "$$p/$$d/" || exit 2; \
	done && \
	cp -- libkorali.so "$$p/korali/" && \
	printf '%s\n' "$$p"
