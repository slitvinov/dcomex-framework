def Engine():
  from libkorali import Engine
  return Engine()


def Experiment():
  from libkorali import Experiment
  return Experiment()


def getWorkerMPIComm():
  from libkorali import getWorkerMPI4PyComm
  return getWorkerMPI4PyComm()
