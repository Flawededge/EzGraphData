# # This file is to keep the main file clean of the messy functions


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
