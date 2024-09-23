ARG BASE_IMAGE
FROM $BASE_IMAGE
COPY . /src
WORKDIR /src
RUN make bin
RUN make dotnet
RUN make lib
RUN make msolve
RUN pip install pip install git+https://github.com/slitvinov/GliomaSolver
RUN MAKEFLAGS=-j4 make lkorali
