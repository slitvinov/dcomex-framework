#!/usr/bin/env python3
import os
import sys
sys.path.append('./_model')
from env import *
import argparse
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument(
    '--env',
    help='Environment to run (navigation, balance or sampling)',
    default="navigation",
    type=str,
    required=False)    
parser.add_argument(
    '--maxGenerations',
    help='Maximum Number of generations to run',
    default=300,
    type=int,
    required=False)    
parser.add_argument(
    '--learningRate',
    help='Learning rate for the selected optimizer',
    default=1e-4,
    type=float,
    required=False)
args = parser.parse_args()

print("Running VMAS environment with arguments:")
print(args)

nStates = { 
    "navigation" : 18,
    "balance" : 16,
    "sampling" : 24 
    }

vmasEnv = createEnv(args.env)

####### Defining Korali Problem

import korali
k = korali.Engine()
e = korali.Experiment()

### Defining the Navigation problem's configuration
e["Problem"]["Type"] = "Reinforcement Learning / Continuous"
e["Problem"]["Agents Per Environment"] = 3
e["Problem"]["Environment Function"] = lambda sample : env(vmasEnv, sample)
e["Problem"]["Testing Frequency"] = 100
e["Problem"]["Policy Testing Episodes"] = 10

nState = nStates[args.env]
for i in range(nState):
    e["Variables"][i]["Name"] = "State No " + str(i)
    e["Variables"][i]["Type"] = "State"

nAction = 2
for i in range(nAction):
    e["Variables"][nState+i]["Name"] = "Action No " + str(i)
    e["Variables"][nState+i]["Type"] = "Action"
    e["Variables"][nState+i]["Lower Bound"] = -1.
    e["Variables"][nState+i]["Upper Bound"] = +1.
    e["Variables"][nState+i]["Initial Exploration Noise"] = 0.5

### Defining Agent Configuration 

e["Solver"]["Type"] = "Agent / Continuous / VRACER"
e["Solver"]["Mode"] = "Training"
e["Solver"]["Multi Agent Relationship"] = "Individual"
e["Solver"]["Experiences Between Policy Updates"] = 1
e["Solver"]["Episodes Per Generation"] = 10

e["Solver"]["Experience Replay"]["Start Size"] = 32768
e["Solver"]["Experience Replay"]["Maximum Size"] = 262144
e["Solver"]["Experience Replay"]["Off Policy"]["REFER Beta"]= 0.3

e["Solver"]["Discount Factor"] = 0.99
e["Solver"]["Learning Rate"] = args.learningRate
e["Solver"]["Mini Batch"]["Size"] = 128
e["Solver"]["State Rescaling"]["Enabled"] = True
e["Solver"]["Reward"]["Rescaling"]["Enabled"] = True

### Configuring the neural network and its hidden layers

e["Solver"]["Neural Network"]["Engine"] = "OneDNN"
e["Solver"]["Neural Network"]["Optimizer"] = "Adam"
e["Solver"]["Policy"]["Distribution"] = "Clipped Normal"

e["Solver"]["Neural Network"]["Hidden Layers"][0]["Type"] = "Layer/Linear"
e["Solver"]["Neural Network"]["Hidden Layers"][0]["Output Channels"] = 256

e["Solver"]["Neural Network"]["Hidden Layers"][1]["Type"] = "Layer/Activation"
e["Solver"]["Neural Network"]["Hidden Layers"][1]["Function"] = "Elementwise/SoftReLU"

e["Solver"]["Neural Network"]["Hidden Layers"][2]["Type"] = "Layer/Linear"
e["Solver"]["Neural Network"]["Hidden Layers"][2]["Output Channels"] = 256

e["Solver"]["Neural Network"]["Hidden Layers"][3]["Type"] = "Layer/Activation"
e["Solver"]["Neural Network"]["Hidden Layers"][3]["Function"] = "Elementwise/SoftReLU"

### Defining Termination Criteria

e["Solver"]["Termination Criteria"]["Max Experiences"] = 1e7
e["Solver"]["Termination Criteria"]["Max Generations"] = args.maxGenerations

### Setting file output configuration

e["File Output"]["Enabled"] = True
e["File Output"]["Use Multiple Files"] = False
e["File Output"]["Frequency"] = 100
e["File Output"]["Path"] = f"_vracer_result_{args.env}_coop"

### Running Experiment

k.run(e)
