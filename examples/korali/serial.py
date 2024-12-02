import korali


def env(s):
    action = None
    s["State"] = [0.0]
    for step in range(2):
        s.update()
        s["Reward"] = 0.0
        s["State"] = [0.0]
        action = s["Action"]
    s["Termination"] = "Terminal"


k = korali.Engine()
e = korali.Experiment()
e["Problem"]["Type"] = "Reinforcement Learning / Continuous"
e["Problem"]["Environment Function"] = env
e["Problem"]["Testing Frequency"] = 0
e["Random Seed"] = 0xC0FFEE
e["Variables"][0]["Name"] = "Position"
e["Variables"][1]["Name"] = "Force"
e["Variables"][1]["Type"] = "Action"
e["Variables"][1]["Initial Exploration Noise"] = 1.0
e["Solver"]["Type"] = "Agent / Continuous / VRACER"
e["Solver"]["Mode"] = "Training"
e["Solver"]["Experiences Between Policy Updates"] = 1
e["Solver"]["Episodes Per Generation"] = 1
e["Solver"]["Experience Replay"]["Start Size"] = 10
e["Solver"]["Experience Replay"]["Maximum Size"] = 10
e["Solver"]["Learning Rate"] = 0.1
e["Solver"]["Neural Network"]["Engine"] = "Korali"
e["Solver"]["Neural Network"]["Optimizer"] = "Adam"
e["Solver"]["Neural Network"]["Hidden Layers"][0]["Type"] = "Layer/Linear"
e["Solver"]["Neural Network"]["Hidden Layers"][0]["Output Channels"] = 4
e["Solver"]["Termination Criteria"]["Max Generations"] = 1
e["Console Output"]["Verbosity"] = "Minimal"

k.run(e)
