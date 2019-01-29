import pandas as pd
import numpy as np
import os
import shelve
import logging
import math

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
                 'B3EffectiveCurrent', 'B4EffectiveCurrent', 'B5EffectiveCurrent', 'B1remainCapacityCoulombs',
                 'B2remainCapacityCoulombs', 'B3remainCapacityCoulombs', 'B4remainCapacityCoulombs',
                 'B5remainCapacityCoulombs', 'CANDevTemperature']
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
                'B1RemainCapacityCoulombs': 'B1remainCapacityCoulombs',
                'B2RemainCapacityCoulombs': 'B2remainCapacityCoulombs',
                'B3RemainCapacityCoulombs': 'B3remainCapacityCoulombs'}

''' These are variables which will need to be manually filled in within the process function'''
outputProcessing = ['bepTSoc1', 'bepTSoc2', 'bepTSoc3',
                    'diggleSoc1', 'diggleSoc2', 'diggleSoc3', 'curDiff1', 'curDiff2', 'curDiff3',
                    'deltaT']


# Processing
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


# This function is run to process the data. It should return an array of arrays in the same format of outputProcessing
def process(mainData, filePath, initial=False):
    mainData.loaded = False
    values = list(outputDirect.values())

    if initial:  # If loading a new file, grab new data
        # First get the modify date of the file, so changes can be detected
        fileDate = os.path.getmtime(filePath)
        with shelve.open(shelveName, flag='c+b') as data:
            oldDate = None
            logging.debug('Shelve opened')
            if 'index' not in data.keys():
                logging.debug('No index found: Making new index')
                data['index'] = {}
            elif filePath in data['index']:
                logging.debug(f'Looking for: {filePath}')
                logging.debug(f"Index found: {data['index']}")
                oldDate = data['index']
                oldDate = oldDate[filePath]

                if oldDate == fileDate:
                    logging.debug('File exists in shelf!')
                    # The file is probably the same, so the data only needs to be un-shelved
                    mainData.updateProgress(50, 'Loading stored')
                    mainData.plotData = data[filePath]
                    return  # There's nothing more to do here, so back to the program
                else:
                    logging.debug('File is not up to date')
            else:
                logging.debug(f"Index found: {data['index']}")
                logging.debug(f'Looking for: {filePath}')
                logging.debug('File does not exist in index')

        # If we got to here, the file is either new or has been updated.. Either way time to load new data!
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
        with shelve.open(shelveName, flag='w+b') as data:
            index = data['index']
            index[filePath] = fileDate
            data['index'] = index

    # /////////////////// Start of data processing /////////////////////////////

    mainData.plotData['bepTSoc1'] = mainData.plotData['B1Current'].copy()
    mainData.plotData['bepTSoc2'] = mainData.plotData['B2Current'].copy()
    mainData.plotData['bepTSoc3'] = mainData.plotData['B3Current'].copy()
    mainData.plotData['diggleSoc1'] = mainData.plotData['B1Current'].copy()
    mainData.plotData['diggleSoc2'] = mainData.plotData['B2Current'].copy()
    mainData.plotData['diggleSoc3'] = mainData.plotData['B3Current'].copy()

    process = [['bepTSoc1', 'B1Current'], ['bepTSoc2', 'B2Current'], ['bepTSoc3', 'B3Current']]
    dig = ['diggleSoc1', 'diggleSoc2', 'diggleSoc3']
    voltage = ['B1Voltage', 'B2Voltage', 'B3Voltage']
    difference = ['curDiff1', 'curDiff2', 'curDiff3']

    for i, [out, cur] in enumerate(process):  # Cycle through each battery individually
        volt = mainData.plotData[voltage[i]].rolling(window=100, min_periods=1,
                                                     center=False).mean()  # Smooth the voltage
        cur = mainData.plotData[cur]  # Give the current a variable as well

        # # BEP SoC

        # Process negative values, I >= -20c rating
        negMask = cur.where(cur < 0, 0)
        negMask.where(negMask >= -mainData.cap[i] / 20, 0, True)
        mainData.plotData[out] = -mainData.plotData['deltaT'] / (
                20 * (mainData.cap[i] / (-negMask * 20))).fillna(0)

        # Process positive values
        posMask = cur.where(cur > 0, 0)
        mainData.plotData[out] += (mainData.plotData['deltaT'] * posMask * mainData.eff[i]) / mainData.cap[i]

        # Process negative values, I > 20c rating
        peuMask = cur.where(cur < -mainData.cap[i] / 20, 0)
        mainData.plotData[out] -= mainData.plotData['deltaT'] / (
                20 * ((mainData.cap[i] / (-peuMask * 20)) ** mainData.peu[i])).fillna(0)

        # # Diggle SoC
        '''Positive values - Cu = Incoming% + Σ { δt * ß * δT * A } 'Equation 15')
            
            δt - Time
            
            ß - Charging efficiency =   /|Constant Current (V → Voltage)    : (100.6265 - (6.3626e-10 * (e ** (9.1904V))) / 100
            'Fig 4, 5'                  \|Constant Voltage (A → C discharge): (-44.211 * A + 100) / 100
            
            δT - Temperature coefficient = ((-0.02069 * (t ** 2)) + (1.8904 * t) + 64.4967) / 100
            'Figure 3 (0.05c line)'
            
            A - Current discharge based on c rating = Current / Capacity
        
            Negative values - Cu = Σ { (K / δT) * A }
            
            K - Attached to peukert's (I have no idea what range of values it'gonna be)
            
        '''

        #  δT → % of useful capacity based off temperature
        t = mainData.plotData['CANDevTemperature']
        T = -0.00008 * (t ** 2) + 0.0081 * t + 0.85
        # T = 0.00008011 * (t ** 2) + 0.008087 * t + 0.8479
        cap = mainData.cap[i] * T

        # Working out A, which is Current / Capacity
        A = cur / (mainData.cap[i] * T)

        # Process negative values, I >= -20c rating
        mainData.plotData[dig[i]] = -mainData.plotData['deltaT'] / (
                20 * (cap / (-negMask * 20))).fillna(0)

        # Process negative values, I < -20c rating
        mainData.plotData[dig[i]] -= mainData.plotData['deltaT'] / (
                20 * ((cap / (-peuMask * 20)) ** mainData.peu[i])).fillna(0)

        # Calculate a window difference of the current to figure out when in CC or CV mode (lots of smoothing)
        diff = abs(cur.rolling(window=600, min_periods=0, center=False, win_type='triang').mean().diff().rolling(
            window=1000, min_periods=0, center=True, win_type='hanning').mean() * 10000) - 1
        mainData.plotData[difference[i]] = diff

        # CC → (100.6265 - (6.3626e-10 * (e ** (9.1904V)))
        mask = volt.where(diff < 0, np.NAN) / 6  # Take only the CC values and convert to 1 cell voltage
        eff = ((100.6265 - (6.3626e-10 * (np.exp(9.1904 * mask)))) / 100).fillna(0)  # Calculate the efficiency

        # CV → (-44.211 * A + 100) / 100 ! Where A is 'C charging'
        mask = A.where(diff > 0, np.NAN)  # Take only the CV values
        eff += ((-44.211 * mask + 100) / 100).fillna(0)  # Calculate the efficiency

        # Calculate the delta percentages
        A = A.where(cur > 0, 0)
        mainData.plotData[dig[i]] += (mainData.plotData['deltaT'] * eff * T * A)

        mainData.plotData.loc[0, dig[i]] = 1  # Start at 100%
        mainData.plotData[dig[i]] = mainData.plotData[dig[i]].cumsum()  # Sum all the changes in capacity
        mainData.plotData[dig[i]] -= (
                    mainData.plotData[dig[i]].clip(1, None) - 1).cummax()  # Subtract numbers over 100%
        mainData.plotData[dig[i]] *= 100  # Increase the scale by 100x

        # Set the starting capacity to 100%
        mainData.plotData.loc[0, out] = 1
        mainData.plotData[out] = mainData.plotData[out].cumsum()  # Sum all of the changes in capacity
        mainData.plotData[out] -= (mainData.plotData[out].clip(1, None) - 1).cummax()  # Subtract numbers over 100%
        mainData.plotData[out] *= 100  # Increase the scale by 100x
        mainData.updateProgress(i * 33, 'Calculating')

    logging.info(f"Min 1: {np.min(mainData.plotData['bepTSoc1'])}")
    logging.info(f"Min 2: {np.min(mainData.plotData['bepTSoc2'])}")
    logging.info(f"Min 3: {np.min(mainData.plotData['bepTSoc3'])}")

    with shelve.open(shelveName, flag='w+b') as data:
        data[filePath] = mainData.plotData  # Update the shelf with all of the plot data
    mainData.updateProgress(100, 'Plot processed!')
    logging.debug('Data processed')
    mainData.loaded = True
