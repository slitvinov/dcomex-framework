#include <korali.hpp>

static void env(korali::Sample &s) {
  MPI_Comm *comm;
  int i, rank, size, step;
  double state[1] = {0};
  std::array<double, 1> action;

  comm = (MPI_Comm *)korali::getWorkerMPIComm();
  MPI_Comm_rank(*comm, &rank);
  MPI_Comm_size(*comm, &size);
  if (rank == 0)
    s["State"] = state;
  for (step = 0; step < 5; step++) {
    if (rank == 0) {
      s.update();
      s["State"] = state;
      s["Reward"] = 0.0;
      action = s["Action"];
    }
    MPI_Bcast(action.data(), 1, MPI_DOUBLE, 0, *comm);
    for (i = 0; i < size; i++) {
      printf("rank ID step [action]: %d %d %d [%g]\n", rank,
             (int)s["Sample Id"], step, action[0]);
      MPI_Barrier(*comm);
    }
  }
  if (rank == 0)
    s["Termination"] = "Terminal";
}

int main() {
  auto e = korali::Experiment();
  auto k = korali::Engine();
  e["Problem"]["Type"] = "Reinforcement Learning / Continuous";
  e["Problem"]["Environment Function"] = &env;
  e["Variables"][0]["Name"] = "Position";
  e["Variables"][1]["Name"] = "Force";
  e["Variables"][1]["Type"] = "Action";
  e["Variables"][1]["Initial Exploration Noise"] = 1.0;
  e["Solver"]["Type"] = "Agent / Continuous / VRACER";
  e["Solver"]["Mode"] = "Training";
  e["Solver"]["Experiences Between Policy Updates"] = 1;
  e["Solver"]["Episodes Per Generation"] = 1;
  e["Solver"]["Experience Replay"]["Start Size"] = 10;
  e["Solver"]["Experience Replay"]["Maximum Size"] = 10;
  e["Solver"]["Learning Rate"] = 0.1;
  e["Solver"]["Neural Network"]["Engine"] = "Korali";
  e["Solver"]["Neural Network"]["Optimizer"] = "Adam";
  e["Solver"]["Neural Network"]["Hidden Layers"][0]["Type"] = "Layer/Linear";
  e["Solver"]["Neural Network"]["Hidden Layers"][0]["Output Channels"] = 4;
  e["Solver"]["Termination Criteria"]["Max Generations"] = 3;
  k["Conduit"]["Type"] = "Distributed";
  k["Conduit"]["Ranks Per Worker"] = 2;

  MPI_Init(NULL, NULL);
  k.setMPIComm(MPI_COMM_WORLD);
  k.run(e);
  MPI_Finalize();
}
