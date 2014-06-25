#!/usr/bin/env python
import numpy as np

benchMark = np.loadtxt("test_contract", skiprows=1, delimiter=',', usecols=[7])
benchMark_value = sum(benchMark)

SVR = np.loadtxt("test_result")
SVR_value = sum(SVR)

diff_value = SVR_value - benchMark_value

diff_percentage = diff_value/benchMark_value

print str(SVR_value)+" "+str(diff_value)+" "+str(diff_percentage)