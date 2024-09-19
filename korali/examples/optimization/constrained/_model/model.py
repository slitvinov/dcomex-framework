#!/usr/bin/env python

# Testfunction form CCI'2006: g09

def model(k):
  d = k["Parameters"]
  res = (d[0] - 10.0)**2 + 5.0 * (d[1] - 12.0)**2 + d[2]**4 \
            + 3.0 * (d[3] - 11.0)**2 + 10.0 * d[4]**6 + 7.0 * d[5]**2 + d[6]**4. \
            - 4.0 * d[5] * d[6] - 10.0 * d[5] - 8.0 * d[6]
  
  k["F(x)"] = -res

# Constraints

def g1(k):
  v = k["Parameters"]
  k["F(x)"] = -127.0 + 2 * v[0] * v[0] + 3.0 * pow(v[1], 4) + \
                v[2] + 4.0 * v[3] * v[3] + 5.0 * v[4]

def g2(k):
  v = k["Parameters"]
  k["F(x)"] = -282.0 + 7.0 * v[0] + 3.0 * v[1] + 10.0 * v[2] * v[2] + v[3] - v[4]

def g3(k):
  v = k["Parameters"]
  k["F(x)"] = -196.0 + 23.0 * v[0] + v[1] * v[1] + 6.0 * v[5] * v[5] - 8.0 * v[6]

def g4(k):
  v = k["Parameters"]
  k["F(x)"] = 4.0 * v[0] * v[0] + v[1] * v[1] - 3.0 * v[0] * v[1] + 2.0 * v[
      2] * v[2] + 5.0 * v[5] - 11.0 * v[6]
