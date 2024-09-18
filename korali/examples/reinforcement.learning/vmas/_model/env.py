#!/usr/bin/env python3
from vmas import make_env
import numpy as np

######## Defining Environment
maxSteps = 100

def createEnv(name):
    return make_env(
        scenario=name,
        num_envs=1, # number of parallel envs
        n_agents=3,
        device="cpu",
        continuous_actions=True,
        dict_spaces=False,  # env returns values as list of list, not dict
        wrapper=None,
        seed=None)


######## Defining Environment Interaction Loop
def env(vmasEnv, s):

 # Initializing environment and random seed
 sampleId = s["Sample Id"]
 states = vmasEnv.reset()

 # Transform output from tensors to lists
 states = [state.tolist()[0] for state in states]

 s["State"] = states
 step = 0
 done = False

 while not done and step < maxSteps:

  # Getting new action
  s.update()

  actions = s["Action"]

  # Trnsform to vmas actions
  actions = [[action] for action in actions]
  
  # Performing the action
  states, rews, dones, _ = vmasEnv.step(actions)

  # Transform vmas outputs from tensors to lists
  states = [state.tolist()[0] for state in states]
  rews = [rew.tolist()[0] for rew in rews]
  isOver = dones.tolist()[0]
  
  # Getting Reward
  s["Reward"] = rews
   
  # Storing New State
  s["State"] = states
  
  # Advancing step counter
  step = step + 1

 # Setting finalization status
 if (isOver):
  s["Termination"] = "Terminal"
 else:
  s["Termination"] = "Truncated"
