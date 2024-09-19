#!/usr/bin/env python3

## In this example, we demonstrate how Korali finds values for the
## variables that maximize the objective function, given by a
## user-provided computational model.

# Importing computational model
import sys
sys.path.append('./_model')
from model import *

# Starting Korali's Engine
import korali
k = korali.Engine()

# Creating new experiment
e = korali.Experiment()

# Configuring Problem.
e["Problem"]["Type"] = "Optimization"
e["Problem"]["Objective Function"] = negative_rosenbrock

# Defining the problem's variables.
for i in range(5):
    e["Variables"][i]["Name"] = "X" + str(i)
    e["Variables"][i]["Initial Value"] = -10

# Configuring Adam parameters
e["Solver"]["Type"] = "Optimizer/AdaBelief"
e["Solver"]["Eta"] = 0.1
e["Solver"]["Termination Criteria"]["Max Generations"] = 5000

# Configuring results path
e["Console Output"]["Frequency"] = 250
e["File Output"]["Frequency"] = 250
e["File Output"]["Path"] = '_korali_result_adabelief'

# Running Experiment
k.run(e)
