from PyQt5 import QtWidgets
import datetime

# Config
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# These headers are checked if they are present, warnings will show if any are missing (can leave empty)
neededHeaders = ['Supply Current', 'Supply Voltage', 'Load Current', 'Load Voltage', 'Soc1', 'Soc2', 'Soc3', 'Soc4',
                 'Soc5', 'B1SecondarySoC', 'B2SecondarySoC', 'B3SecondarySoC',
                 'B1Current', 'B2Current', 'B3Current', 'B4Current', 'B5Current',
                 'B1Voltage', 'B2Voltage', 'B3Voltage', 'B4Voltage', 'B5Voltage',
                 'B1RemainCapacity', 'B2RemainCapacity', 'B3RemainCapacity',
                 'B4RemainCapacity', 'B5RemainCapacity', 'B1EffectiveCurrent', 'B2EffectiveCurrent',
                 'B3EffectiveCurrent', 'B4EffectiveCurrent', 'B5EffectiveCurrent', 'B1remainCapacityCoulombs',
                 'B2remainCapacityCoulombs', 'B3remainCapacityCoulombs', 'B4remainCapacityCoulombs',
                 'B5remainCapacityCoulombs', 'CANDevTemperature']
# The labels to display in the plot selection area. Dictionary in process needs to be formatted with same names

''' These are put directly into the plot variable. 'New name': '.csv header name' '''
outputDirect = {'Temperature': 'CANDevTemperature',
                'Supply Current': 'Supply Current',
                'Supply Voltage': 'Supply Voltage',
                'Load Current': 'Load Current',
                'Load Voltage': 'Load Voltage',
                'bepSoc1': 'Soc1',
                'bepSoc2': 'Soc2',
                'bepSoc3': 'Soc3',
                'bluSoc1': 'B1SecondarySoC',
                'bluSoc2': 'B2SecondarySoC',
                'bluSoc3': 'B3SecondarySoC',
                'B1Current': 'B1Current',
                'B2Current': 'B2Current',
                'B3Current': 'B3Current',
                'B1Voltage': 'B1Voltage',
                'B2Voltage': 'B2Voltage',
                'B3Voltage': 'B3Voltage',
                'B1RemainCapacityCoulombs': 'B1remainCapacityCoulombs',
                'B2RemainCapacityCoulombs': 'B2remainCapacityCoulombs',
                'B3RemainCapacityCoulombs': 'B3remainCapacityCoulombs'}

''' These are variables which will need to be manually filled in within the process function'''
outputProcessing = ['bepTSoc1', 'bepTSoc2', 'bepTSoc3']


# Processing
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


# This function is run to process the data. It should return an array of arrays in the same format of outputProcessing
# mainData.data is the full .csv file in a dictionary
def process(mainData, initial=False):
    dictFormat = dict.fromkeys(neededHeaders + list(outputDirect.keys()))
    outData, prev = [], None  # Initialize the used variables

    if initial:  # Add in all of the items which don't change if it's being run from load data
        for count, i in enumerate(mainData.data):
            for plotName, header in outputDirect.items():
                dictFormat[plotName] = i[header]
            outData.append(dictFormat)

            if count % (mainData.step * 50) == 0:
                mainData.progressBar.setValue(40 + count // (mainData.step * 50))
                print(f'Time column: {40 + count // (mainData.step * 50)}%')

        # for i in mainData.data:  # TODO : Get the output processing to operate
        #     if prev is None:
        #         timeDiff = 0  # First time difference is 0
        #
        #         # Set the calculated values
        #         dictFormat['bepTSoc1'] = 100
        #         dictFormat['bepTSoc2'] = 100
        #         dictFormat['bepTSoc3'] = 100
        #         outData = [dictFormat]
        #     else:
        #         diff = i['Time'] - prev['Time']  # Difference in milliseconds
        #         diff = (diff.days * 86400000) + (diff.seconds * 1000) + (diff.microseconds / 1000)

        prev = i  # Update the previous value
    return outData
