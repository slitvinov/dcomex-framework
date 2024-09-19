#!/usr/bin/env python3
from cartpole import *
import pdb
import numpy as np
import time
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

 # Simulate slow run
 print("[env] init: sleep 5 seconds..")
 time.sleep(5)

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

def multienv(s):

 # Initializing environment and random seed
 sampleId = s["Sample Id"]
 launchId = s["Launch Id"]
 if s["Mode"] == "Training":
    envId = sampleId % 3
 else:
    envId = 0
 cart.reset(sampleId * 1024 + launchId)
 s["State"] = cart.getState().tolist()
 step = 0
 done = False

 while not done and step < maxSteps:
  
  s.update()
  
  # Performing the action
  done = cart.advance(s["Action"])
  
  # Getting Reward
  
  s["Reward"] = cart.getReward()
  
  reward = cart.getReward()
  if (envId == 0):
    s["Reward"] = cart.getReward()
  elif (envId == 1):
    s["Reward"] = cart.getReward() - 1
  else:
    s["Reward"] = cart.getReward() * 0.1
   
  # Storing New State
  s["State"] = cart.getState().tolist()
  
  # Advancing step counter
  step = step + 1

 # Setting finalization status
 if (cart.isOver()):
  s["Termination"] = "Terminal"
 else:
  s["Termination"] = "Truncated"
