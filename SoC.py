import pandas as pd
import numpy as np
import logging
import linecache
import sys

''' State of charge algorithms. 

    This is to seperate the code out a bit to make it a bit easier to read and to update with new bits
    
        Current algorithms
    → bepSoC - Peukert's on discharge, 0.85 efficiency on charge
    → digSoC - My custom algorithm based off a conference. Temp and peukert's ish
    → bluSoC - No clue how this thing works. I'll get there eventually
    
        Standard parameters
    mainData - The main class self
    cur - Current array (In the form of a pd array)
    bat - The Peukert's value, efficiency and capacity in a dictionary
'''


def bepSoC(mainData, cur, bat):
    # Process negative values, I >= -20c rating
    negMask = cur.where(cur < 0, 0)
    negMask.where(negMask >= -bat['cap'] / 20, 0, True)
    out = -mainData.plotData['deltaT'] / (
            20 * (bat['cap'] / (-negMask * 20))).fillna(0)

    # Process positive values
    posMask = cur.where(cur > 0, 0)
    out += (mainData.plotData['deltaT'] * posMask * bat['eff']) / bat['cap']

    # Process negative values, I > 20c rating
    peuMask = cur.where(cur < -bat['cap'] / 20, 0)
    out -= mainData.plotData['deltaT'] / (
            20 * ((bat['cap'] / (-peuMask * 20)) ** bat['peu'])).fillna(0)

    # Sum up all results and limit the max value
    out[0] = 1
    out = out.cumsum()  # Sum all of the changes in capacity
    out -= (out.clip(1, None) - 1).cummax()  # Subtract numbers over 100%
    out *= 100  # Increase the scale by 100x to range into 0 → 100

    return out


def digSoC(mainData, cur, bat, volt):
    try:
        temp = mainData.plotData['CANDevTemperature']
        volt = volt.rolling(window=100, min_periods=1, center=False).mean()  # Smooth the voltage

        # Work out current in c
        A = (cur / bat['cap'])

        # δT → % of useful capacity based off temperature. This is the charging effective capacity
        T = (-0.00008 * (temp ** 2) + 0.0081 * temp + 0.85)

        # Assign letters to make complicated equation more manageable
        a, b, c, d = mainData.spinA.value() / 1000, mainData.spinB.value() / 1000, \
                     mainData.spinC.value() / 1000, mainData.spinD.value() / 1000
        # Apply the Symmetrical Sigmoidal to get the discharging effective capacity
        Ka = A.where(A < 0, 0)
        Ka = T * (d + ((a - d) / (1 + (-Ka / c) ** b))).fillna(0)

        # Process negative values, I < 0. δ% = A * K(A) * δt
        out = (A * Ka * mainData.plotData['deltaT']) / 100

        # Calculate a window difference of the current to figure out when in CC or CV mode (lots of smoothing)
        diff = abs(cur.rolling(window=600, min_periods=0, center=False, win_type='triang').mean().diff().rolling(
            window=1000, min_periods=0, center=True, win_type='hanning').mean() * 10000) - 1

        # CC → (100.6265 - (6.3626e-10 * (e ** (9.1904V)))
        mask = volt.where(diff < 0, np.NAN) / 6  # Take only the CC values and convert to 1 cell voltage
        eff = ((100.6265 - (6.3626e-10 * (np.exp(9.1904 * mask)))) / 100).fillna(0)  # Calculate the efficiency

        # CV → (-44.211 * A + 100) / 100 ! Where A is 'C charging'
        mask = A.where(diff > 0, np.NAN)  # Take only the CV values
        eff += ((-44.211 * mask + 100) / 100).fillna(0)  # Calculate the efficiency

        # Calculate the delta percentages
        A = A.where(cur > 0, 0)
        out += (mainData.plotData['deltaT'] * eff * T * A)

        out[0] = 1  # Start at 100%
        out = out.cumsum()  # Sum all the changes in capacity
        out -= (
                out.clip(1, None) - 1).cummax()  # Subtract numbers over 100%
        out *= 100  # Increase the scale by 100x

        return out

    except:
        PrintException()
        return cur


def bluSoC(mainData, cur, bat, volt):
    1 + 1

    return cur


def PrintException():  # A bit of code to make finding errors easier
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))
