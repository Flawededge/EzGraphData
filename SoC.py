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


def bepSoC(mainData, cur, bat, volt):
    # Process negative values, I >= -20c rating
    negMask = cur.where(cur < 0, 0)
    negMask.where(negMask >= -bat['cap'] / 20, 0, True)
    out = -mainData.plotData['deltaT'] / (
            20 * (bat['cap'] / (-negMask * 20))).fillna(0)

    # Process positive values
    if mainData.adjustedChargeEfficiency.isChecked():
        A = (cur / bat['cap'])
        temp = mainData.plotData['CANDevTemperature']  # Give the temperature a
        volt = volt.rolling(window=100, min_periods=1, center=False).mean()  # Smooth the voltage
        T = (-0.00008 * (temp ** 2) + 0.0081 * temp + 0.85)  # Temperature coefficient

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
    else:
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


# Variable setup for blueSoC
OCV_Tempco = 0.0008  # From ln 197 - Not sure why it's set at this number, but i'll play with it


# Ref_OCV  # Variable taken from the battery table


def bluSoC(mainData, cur, bat, volt):
    # Variable setup
    NominalVoltage = 12
    RestThresholdMultiplier, K0, K1, K2, Ref_OCV, OVP_Gain_D, Self_Discharge = \
        setupBatteryVariables(batteryTypes[mainData.battType.currentIndex()])
    OCV_Tempco = mainData.tempCo.value()
    temp = mainData.plotData['CANDevTemperature'] - mainData.tempAdj.value()

    # # Start of actual processing
    # try:
    #     cur[0] = 100  # Set the first iteration to 100%
    #     prev = cur[0]
    #     for count in range(len(cur.index)):  # For loop, skip first iteration
    #
    #         if count == 0:
    #             soc = prev
    #         OCV = (NominalVoltage * K0) * (1.0 + (OCV_Tempco * (temp - 25.0)) + (K1 * (SOC - Ref_OCV)) + (K2 * (SOC - Ref_OCV) ** 2))
    #
    # except:
    #     PrintException()
    #     return cur
    return cur


batteryTypes = [
    'BS_SOC_BATTERY_TYPE_FLOODED_RESERVE',  # 0
    'BS_SOC_BATTERY_TYPE_FLOODED_COMBINATION',  # 1
    'BS_SOC_BATTERY_TYPE_FLOODED_DEEP_CYCLE',  # 2
    'BS_SOC_BATTERY_TYPE_AGM_STD',  # 3
    'BS_SOC_BATTERY_TYPE_AGM_SPL',  # 4
    'BS_SOC_BATTERY_TYPE_GEL_CELL',  # 5
    'BS_SOC_BATTERY_TYPE_FFLY_CELL']  # 6


# A mess of a function to get all of the initial specs of the battery set properly
def setupBatteryVariables(bType):
    baseData = inputVariables
    out = {}
    if bType == 'BS_SOC_BATTERY_TYPE_FLOODED_RESERVE':
        fRestThresholdMultiplier = baseData['FLOOD_RES_REST_TH_MULT']  # Multiplier for RestTimer
        fK0 = baseData['FLOOD_RES_K0']  # First order constant for OCV equation
        fK1 = baseData['FLOOD_RES_K1']  # First order constant for OCV equation
        fK2 = baseData['FLOOD_RES_K2']  # Second order constant for OCV equation
        fRef_OCV = baseData['FLOOD_RES_REF_OCV']  # State_of_Charge_For_First_Order_OCV
        fOVP_Gain_D = baseData[
            'FLOOD_RES_OVP_GAIN_FACTOR']  # Variable associated with battery type from the observation
        # that the effective amperage drain is less efficient at high currents, than low.  May turn out to be universal constant.
        fSelf_Discharge = baseData['FLOOD_RES_SELF_DISCHARGE']

    elif bType == 'BS_SOC_BATTERY_TYPE_FLOODED_COMBINATION':  # lets use this one for low maint. Calcium styles
        fRestThresholdMultiplier = baseData['FLOOD_COMBO_REST_TH_MULT']  # Multiplier for RestTimer
        fK0 = baseData['FLOOD_COMBO_K0']  # First order constant for OCV equation
        fK1 = baseData['FLOOD_COMBO_K1']  # First order constant for OCV equation
        fK2 = baseData['FLOOD_COMBO_K2']  # Second order constant for OCV equation
        fRef_OCV = baseData['FLOOD_COMBO_REF_OCV']  # State_of_Charge_For_First_Order_OCV
        fOVP_Gain_D = baseData[
            'FLOOD_COMBO_OVP_GAIN_FACTOR']  # Variable associated with battery type from the observation
        # that the effective amperage drain is less efficient at high currents, than low.  May turn out to be universal constant.
        fSelf_Discharge = baseData['FLOOD_COMBO_SELF_DISCHARGE']

    elif bType == 'BS_SOC_BATTERY_TYPE_FLOODED_DEEP_CYCLE':
        fRestThresholdMultiplier = baseData['DEEP_CYCLE_REST_TH_MULT']  # Multiplier for RestTimer
        fK0 = baseData['DEEP_CYCLE_K0']  # First order constant for OCV equation
        fK1 = baseData['DEEP_CYCLE_K1']  # First order constant for OCV equation
        fK2 = baseData['DEEP_CYCLE_K2']  # Second order constant for OCV equation
        fRef_OCV = baseData['DEEP_CYCLE_REF_OCV']  # State_of_Charge_For_First_Order_OCV
        fOVP_Gain_D = baseData[
            'DEEP_CYCLE_OVP_GAIN_FACTOR']  # Variable associated with battery type from the observation
        # that the effective amperage drain is less efficient at high currents, than low.  May turn out to be universal constant.
        fSelf_Discharge = baseData['DEEP_CYCLE_SELF_DISCHARGE']

    elif bType == 'BS_SOC_BATTERY_TYPE_AGM_STD':
        fRestThresholdMultiplier = baseData['AGM_STD_REST_TH_MULT']  # Multiplier for RestTimer
        fK0 = baseData['AGM_STD_K0']  # First order constant for OCV equation
        fK1 = baseData['AGM_STD_K1']  # First order constant for OCV equation
        fK2 = baseData['AGM_STD_K2']  # Second order constant for OCV equation
        fRef_OCV = baseData['AGM_STD_REF_OCV']  # State_of_Charge_For_First_Order_OCV - Units:  SOC %.
        # Intended to be the SOC at which the base OCV is obtained.
        fOVP_Gain_D = baseData['AGM_STD_OVP_GAIN_FACTOR']  # Variable associated with battery type from the observation
        # that the effective amperage drain is less efficient at high currents, than low.  May turn out to be universal constant.
        fSelf_Discharge = baseData['AGM_STD_SELF_DISCHARGE']

    elif bType == 'BS_SOC_BATTERY_TYPE_AGM_SPL':
        fRestThresholdMultiplier = baseData['AGM_SPL_REST_TH_MULT']  # Multiplier for RestTimer
        fK0 = baseData['AGM_SPL_K0']  # First order constant for OCV equation
        fK1 = baseData['AGM_SPL_K1']  # First order constant for OCV equation
        fK2 = baseData['AGM_SPL_K2']  # Second order constant for OCV equation
        fRef_OCV = baseData['AGM_SPL_REF_OCV']  # State_of_Charge_For_First_Order_OCV - Units:  SOC %.
        # Intended to be the SOC at which the base OCV is obtained.
        fOVP_Gain_D = baseData['AGM_SPL_OVP_GAIN_FACTOR']  # Variable associated with battery type from the observation
        # that the effective amperage drain is less efficient at high currents, than low.  May turn out to be universal constant.
        fSelf_Discharge = baseData['AGM_SPL_SELF_DISCHARGE']

    elif bType == 'BS_SOC_BATTERY_TYPE_GEL_CELL':
        fRestThresholdMultiplier = baseData['GEL_CELL_REST_TH_MULT']  # Multiplier for RestTimer
        fK0 = baseData['GEL_CELL_K0']  # First order constant for OCV equation
        fK1 = baseData['GEL_CELL_K1']  # First order constant for OCV equation
        fK2 = baseData['GEL_CELL_K2']  # Second order constant for OCV equation
        fRef_OCV = baseData['GEL_CELL_REF_OCV']  # State_of_Charge_For_First_Order_OCV - Units:  SOC %.
        # Intended to be the SOC at which the base OCV is obtained.
        fOVP_Gain_D = baseData['GEL_CELL_OVP_GAIN_FACTOR']  # Variable associated with battery type from the observation
        # that the effective amperage drain is less efficient at high currents, than low.  May turn out to be universal constant.
        fSelf_Discharge = baseData['GEL_CELL_SELF_DISCHARGE']

    elif bType == 'BS_SOC_BATTERY_TYPE_FFLY_CELL':
        fRestThresholdMultiplier = baseData['FFLY_CELL_REST_TH_MULT']  # Multiplier for RestTimer
        fK0 = baseData['FFLY_CELL_K0']  # First order constant for OCV equation
        fK1 = baseData['FFLY_CELL_K1']  # First order constant for OCV equation
        fK2 = baseData['FFLY_CELL_K2']  # Second order constant for OCV equation
        fRef_OCV = baseData['FFLY_CELL_REF_OCV']  # State_of_Charge_For_First_Order_OCV - Units:  SOC %.
        # Intended to be the SOC at which the base OCV is obtained.
        fOVP_Gain_D = baseData[
            'FFLY_CELL_OVP_GAIN_FACTOR']  # Variable associated with battery type from the observation
        # that the effective amperage drain is less efficient at high currents, than low.  May turn out to be universal constant.
        fSelf_Discharge = baseData['FFLY_CELL_SELF_DISCHARGE']

    else:
        raise ValueError('setupBatteryVariables: Battery type is incorrect')

    return fRestThresholdMultiplier, fK0, fK1, fK2, fRef_OCV, fOVP_Gain_D, fSelf_Discharge


inputVariables = {
    'DISCHARGE_REST_TIME_INIT': 2.0 / 4.5,  # 2 hrs  - average cycle time is roughly 4.5
    'SOC_INIT': 99.0,
    'PRECISE_SOC_INIT': 99.0,
    'FULL_CHARGE_TIMEOUT': 0.25 / 5.0,  # About 15 min - this timer only executes once every 5 cycles
    'ABSORBTION_FUDGE': 0.3,  # decrease full charge voltage by this amount too account for temp diff
    'ZERO_CROSS_ACCURACY': 0.08,  # How accurate is the zero crossing (+/- 0.1 A plus fudge
    'SOC_MAX_VALUE': 100.0,
    'SOC_MIN_VALUE': 0.0,
    'SURFACE_CHARGE': 4.0,  # Estimated % of battery that is the surface charge: 1%

    'FLOOD_RES_REST_TH_MULT': 0.001,  # Multiplier for RestTimer
    'FLOOD_RES_K0': 1.008,  # First order constant for OCV equation
    'FLOOD_RES_K1': 0.00065,  # First order constant for OCV equation
    'FLOOD_RES_K2': -0.000001,  # Second order constant for OCV equation
    'FLOOD_RES_REF_OCV': 10.0,  # State_of_Charge_For_First_Order_OCV
    'FLOOD_RES_OVP_GAIN_FACTOR': 6.0,
    'FLOOD_RES_SELF_DISCHARGE': 3.0,  # wk 4/22/08 adding for self discharge

    'FLOOD_COMBO_REST_TH_MULT': 0.001,  # Multiplier for RestTimer
    'FLOOD_COMBO_K0': 0.999,  # First order constant for OCV equation
    'FLOOD_COMBO_K1': 0.0009,  # First order constant for OCV equation
    'FLOOD_COMBO_K2': -0.000001,  # Second order constant for OCV equation
    'FLOOD_COMBO_REF_OCV': 10.0,  # State_of_Charge_For_First_Order_OCV
    'FLOOD_COMBO_OVP_GAIN_FACTOR': 6.0,
    'FLOOD_COMBO_SELF_DISCHARGE': 1.5,  # wk 4/22/08 adding for self discharge

    'DEEP_CYCLE_REST_TH_MULT': 0.001,  # wk Multiplier for RestTimer
    'DEEP_CYCLE_K0': 0.99,  # 0.96 Revised WK First order constant for OCV equation
    'DEEP_CYCLE_K1': 0.0009,  # 0.00128 First order constant for OCV equation
    'DEEP_CYCLE_K2': -0.000002,  # -0.000002Second order constant for OCV equation
    'DEEP_CYCLE_REF_OCV': 10.0,
# State_of_Charge_For_First_Order_OCV - Units:  SOC %.  Intended to be the SOC at which the base OCV is obtained.
    'DEEP_CYCLE_OVP_GAIN_FACTOR': 6.0,
# Variable associated with battery type ... from the observation that the effective amperage drain': 0.5 at 12V
    'DEEP_CYCLE_SELF_DISCHARGE': 2.5,  # 2.0 wk 4/22/08 adding for self discharge

    'AGM_STD_REST_TH_MULT': 0.001,  # wk Multiplier for RestTimer
    'AGM_STD_K0': 0.99,  # First order constant for OCV equation
    'AGM_STD_K1': 0.00091,  # Revised WK First order constant for OCV equation
    'AGM_STD_K2': 0.0,  # Second order constant for OCV equation
    'AGM_STD_REF_OCV': 8.0,
# State_of_Charge_For_First_Order_OCV - Units:  SOC %.  Intended to be the SOC at which the base OCV is obtained.
    'AGM_STD_OVP_GAIN_FACTOR': 6.0,
# Variable associated with battery type ... from the observation that the effective amperage drain': 0.5 at 12V
    'AGM_STD_SELF_DISCHARGE': 1.0,  # wk guessing for AGM's

    'AGM_SPL_REST_TH_MULT': 0.001,  # wk Multiplier for RestTimer
    'AGM_SPL_K0': 0.9637,  # First order constant for OCV equation
    'AGM_SPL_K1': 0.00138,  # Revised WK First order constant for OCV equation
    'AGM_SPL_K2': 0.0,  # Second order constant for OCV equation
    'AGM_SPL_REF_OCV': 6.0,
# State_of_Charge_For_First_Order_OCV - Units:  SOC %.  Intended to be the SOC at which the base OCV is obtained.
    'AGM_SPL_OVP_GAIN_FACTOR': 6.0,
# Variable associated with battery type ... from the observation that the effective amperage drain': 0.5 at 12V
    'AGM_SPL_SELF_DISCHARGE': 1.0,  # wk guessing for AGM's

    'GEL_CELL_REST_TH_MULT': 0.001,  # wk Multiplier for RestTimer
    'GEL_CELL_K0': 0.99,  # First order constant for OCV equation
    'GEL_CELL_K1': 0.00095,  # Revised WK First order constant for OCV equation
    'GEL_CELL_K2': 0.0,  # Second order constant for OCV equation
    'GEL_CELL_REF_OCV': 10.0,
# State_of_Charge_For_First_Order_OCV - Units:  SOC %.  Intended to be the SOC at which the base OCV is obtained.
    'GEL_CELL_OVP_GAIN_FACTOR': 6.0,
# Variable associated with battery type ... from the observation that the effective amperage drain': 0.5 at 12V
    'GEL_CELL_SELF_DISCHARGE': 1.0,  # wk guessing for Gel

    'FFLY_CELL_REST_TH_MULT': 0.001,  # wk Multiplier for RestTimer
    'FFLY_CELL_K0': 0.946,  # First order constant for OCV equation
    'FFLY_CELL_K1': 0.00203,  # Revised WK First order constant for OCV equation
    'FFLY_CELL_K2': -8.428e-6,  # Second order constant for OCV equation
    'FFLY_CELL_REF_OCV': 10.0,
# State_of_Charge_For_First_Order_OCV - Units:  SOC %.  Intended to be the SOC at which the base OCV is obtained.
    'FFLY_CELL_OVP_GAIN_FACTOR': 6.0,
# Variable associated with battery type ... from the observation that the effective amperage drain': 0.5 at 12V
    'FFLY_CELL_SELF_DISCHARGE': 0.5  # atb - should be really small - guessing
}

def PrintException():  # A bit of code to make finding errors easier
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))
