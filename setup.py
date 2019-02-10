import pandas as pd
import numpy as np
import os
import shelve
import logging
import SoC  # Contains state of charge calculations
import importlib  # For reloading SoC while testing

# Config
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# You shouldn't need to change this. It's the name of the file which the program stores unused data on disk
# Feel free to delete the data file when you're done. It is mainly used to switch between data sets quickly
shelveName = 'data'
# Be aware, the file is overwritten on launch in an effort to avoid getting someone else's data file and it running
# Weird code on your computer

# These headers are checked if they are present, warnings will show if any are missing (can leave empty)
neededHeaders = ['TimeStamp', 'Supply Current', 'Supply Voltage', 'Load Current', 'Load Voltage', 'Soc1', 'Soc2',
                 'Soc3',
                 'Soc4',
                 'Soc5', 'B1SecondarySoC', 'B2SecondarySoC', 'B3SecondarySoC',
                 'B1Current', 'B2Current', 'B3Current', 'B4Current', 'B5Current',
                 'B1Voltage', 'B2Voltage', 'B3Voltage', 'B4Voltage', 'B5Voltage',
                 'B1RemainCapacity', 'B2RemainCapacity', 'B3RemainCapacity',
                 'B4RemainCapacity', 'B5RemainCapacity', 'B1EffectiveCurrent', 'B2EffectiveCurrent',
                 'B3EffectiveCurrent', 'B4EffectiveCurrent', 'B5EffectiveCurrent', 'B1RemainCapacityCoulombs',
                 'B2RemainCapacityCoulombs', 'B3RemainCapacityCoulombs', 'B4RemainCapacityCoulombs',
                 'B5RemainCapacityCoulombs', 'CANDevTemperature']
# The labels to display in the plot selection area. Dictionary in process needs to be formatted with same names

''' These are put directly into the plot variable. 'New name': '.csv header name' '''
outputDirect = {'Time': 'TimeStamp',
                'Temperature': 'CANDevTemperature',
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
                'B1RemainCapacityCoulombs': 'B1RemainCapacityCoulombs',
                'B2RemainCapacityCoulombs': 'B2RemainCapacityCoulombs',
                'B3RemainCapacityCoulombs': 'B3RemainCapacityCoulombs'}

''' These are variables which will need to be manually filled in within the process function '''
outputProcessing = ['bepTSoc1', 'digTSoc1', 'bluTSoc1',
                    'bepTSoc2', 'digTSoc2', 'bluTSoc2',
                    'bepTSoc3', 'digTSoc3', 'bluTSoc3',
                    'deltaT']

# Processing
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


# This function is run to process the data. It should return an array of arrays in the same format of outputProcessing
def process(mainData, filePath, state):
    mainData.loaded = False
    values = list(outputDirect.values())
    new = True

    # First get the modify date of the file, so changes can be detected
    fileDate = os.path.getmtime(filePath)
    with shelve.open(shelveName, flag='c+b') as data:
        logging.debug('Shelve opened')

        logging.debug('Checking for valid index')
        if 'index' in data.values():  # Check if an index exists
            logging.debug('Valid index found!')

            if filePath in data['index']:  # Check if the file exists in the index
                logging.info(f'{filePath} found in index, loading from shelve')

                oldDate = data.loc['index', filePath]
                oldDate = oldDate[filePath]

                if oldDate == fileDate:
                    logging.debug('File exists in shelf!')
                    # The file is probably the same, so the data only needs to be un-shelved
                    mainData.updateProgress(50, 'Loading stored')
                    mainData.plotData = data[filePath]
                else:
                    logging.debug('File is not up to date')
            else:  # The file is not in the index
                logging.info(f'{filePath} is a new file, loading from disk')
        else:  # No index exists
            logging.debug('No index found, making one')
            data['index'] = {}

        if new:
            # If we got to here, the file is either new or has been updated.. Either way time to load new data!
            state = [[True, True, True], [True, True, True], [True, True, True]]
            mainData.plotData = pd.read_csv(open(filePath))[values]  # Read from file

            mainData.updateProgress(50, 'Data loaded')  # Progress bar to keep the interface looking interesting

            # Convert time to readable format and add it to plotData
            mainData.plotData = mainData.plotData.assign(
                Time=pd.to_datetime(mainData.plotData['TimeStamp'], errors='coerce', format='%Y-%m-%d %H:%M:%S:%f'))

            mainData.updateProgress(70, 'Time applied')

            mainData.plotData['deltaT'] = mainData.plotData['Time']
            mainData.plotData['deltaT'] = mainData.plotData['deltaT'].diff()
            mainData.plotData.loc[0, 'deltaT'] = mainData.plotData.loc[1, 'deltaT']  # Make the first time not = NaN

            #  Turn all of the values into floats of how many hours have passed between results
            mainData.plotData['deltaT'] = [delta.total_seconds() / 3600 for delta in mainData.plotData['deltaT']]

            startTime = mainData.plotData['Time'][0]
            mainData.plotData['Time'] = [(i - startTime).total_seconds() / 3600 for i in mainData.plotData['Time']]
            mainData.plotData.set_index('Time')

            mainData.updateProgress(90, 'Stuff tweaked')

            # Time to shelve the output
            index = data['index']
            index[filePath] = fileDate
            data['index'] = index

    # /////////////////// Start of data processing /////////////////////////////

    # mainData.plotData['bepTSoc1'] = mainData.plotData['B1Current'].copy()
    # mainData.plotData['bepTSoc2'] = mainData.plotData['B2Current'].copy()
    # mainData.plotData['bepTSoc3'] = mainData.plotData['B3Current'].copy()
    # mainData.plotData['diggleSoc1'] = mainData.plotData['B1Current'].copy()
    # mainData.plotData['diggleSoc2'] = mainData.plotData['B2Current'].copy()
    # mainData.plotData['diggleSoc3'] = mainData.plotData['B3Current'].copy()

    output = [['bepTSoc1', 'digTSoc1', 'bluTSoc1'],
              ['bepTSoc2', 'digTSoc2', 'bluTSoc2'],
              ['bepTSoc3', 'digTSoc3', 'bluTSoc3']]

    current = ['B1Current', 'B2Current', 'B3Current']
    voltage = ['B1Voltage', 'B2Voltage', 'B3Voltage']
    batteries = mainData.batterySpecs

    importlib.reload(SoC)  # Update the file so I can make quick changes without recompiling
    for out, cur, bat, vol, active in zip(output, current, batteries, voltage,
                                          state):  # Cycle through each battery individually

        if active[0]:
            mainData.plotData[out[0]] = SoC.bepSoC(mainData, mainData.plotData[cur], bat)
        if active[1]:
            mainData.plotData[out[1]] = SoC.digSoC(mainData, mainData.plotData[cur], bat, mainData.plotData[vol])
        if active[2]:
            mainData.plotData[out[2]] = SoC.bluSoC(mainData, mainData.plotData[cur], bat, mainData.plotData[vol])

    logging.info(f"Min 1: {np.min(mainData.plotData['bepTSoc1'])}")
    logging.info(f"Min 2: {np.min(mainData.plotData['bepTSoc2'])}")
    logging.info(f"Min 3: {np.min(mainData.plotData['bepTSoc3'])}")

    with shelve.open(shelveName, flag='w+b') as data:
        data[filePath] = mainData.plotData  # Update the shelf with all of the plot data
    mainData.updateProgress(100, 'Plot processed!')
    logging.debug('Data processed')
    mainData.loaded = True
