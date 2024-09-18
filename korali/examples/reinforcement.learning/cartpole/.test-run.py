#! /usr/bin/env python3
from subprocess import call
import os

r = call(["python3", "run-vracer.py", "--maxGenerations", "10"])
if r!=0:
  exit(r)

r = call(["python3", "run-vracer.py", "--maxGenerations", "10", "--concurrentWorkers", "3"])
if r!=0:
  exit(r)

r = call(["python3", "run-dvracer.py", "--maxGenerations", "10"])
if r!=0:
  exit(r)

exit(0)
