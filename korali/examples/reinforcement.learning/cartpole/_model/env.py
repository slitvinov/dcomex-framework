#!/usr/bin/env python3
from cartpole import *
import pdb
import numpy as np
######## Defining Environment Storage

cart = CartPole()
maxSteps = 500

def env(s):

 # Initializing environment and random seed
 sampleId = s["Sample Id"]
 cart.reset(sampleId)
 s["State"] = cart.getState().tolist()
 step = 0
 done = False

 while not done and step < maxSteps:

  # Getting new action
  s.update()
  
  # Performing the action
  done = cart.advance(s["Action"])
  
  # Getting Reward
  s["Reward"] = cart.getReward()
   
  # Storing New State
  s["State"] = cart.getState().tolist()
  
  # Advancing step counter
  step = step + 1

 # Setting finalization status
 if (cart.isOver()):
  s["Termination"] = "Terminal"
 else:
  s["Termination"] = "Truncated"
