from blueSeasTestingFunctions import setupBatteryVariables
import numpy as np
import sys

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Possible battery types:
batteryTypes = [
    'BS_SOC_BATTERY_TYPE_FLOODED_RESERVE',  # 0
    'BS_SOC_BATTERY_TYPE_FLOODED_COMBINATION',  # 1
    'BS_SOC_BATTERY_TYPE_FLOODED_DEEP_CYCLE',  # 2
    'BS_SOC_BATTERY_TYPE_AGM_STD',  # 3
    'BS_SOC_BATTERY_TYPE_AGM_SPL',  # 4
    'BS_SOC_BATTERY_TYPE_GEL_CELL',  # 5
    'BS_SOC_BATTERY_TYPE_FFLY_CELL']  # 6


def calculateOVP(batNum, SOC, temp, curVoltage):
    RestThresholdMultiplier, K0, K1, K2, Ref_OCV, OVP_Gain_D, Self_Discharge = setupBatteryVariables(
        batteryTypes[batNum])
    OCV = (nominal_voltage * K0) * (1 + OCV_TempCoefficient * (temp - 25)) + \
          (K1 * (SOC - Ref_OCV)) + \
          (K2 * pow(SOC - Ref_OCV, 2))

    OVP = curVoltage - OCV
    return OCV


nominal_voltage = 12

currentVoltage = 12.5  # Live voltage reading
currentCurrent = 10  # Current reading in A
timeStep = 1000  # How long each reading is apart is milliseconds

OCV_TempCoefficient = 0.0008

outputData = np.zeros([len(batteryTypes), 101 * 61, 3])

for typ in range(len(batteryTypes)):
    print(f'\nWorking on #{typ}: {batteryTypes[typ]}')
    for s in range(0, 101, 1):
        for t in range(-20, 41, 1):
            print(f'\r{t}, {s}', end='')
            outputData[typ][s * 61 + t + 20] = [s, t, calculateOVP(typ, s, t)]
            sys.stdout.flush()

print()

for i in range(len(batteryTypes)):
    print(f'Plotting {batteryTypes[i]}')
    X = outputData[i][:, 0]
    Y = outputData[i][:, 1]
    Z = outputData[i][:, 2]

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    ax.scatter(X, Y, Z)
plt.show()
