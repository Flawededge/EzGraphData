import pandas as pd
import numpy as np
import os
import shelve


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
outputProcessing = ['bepTSoc1', 'bepTSoc2', 'bepTSoc3', 'deltaT']


# Processing
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


# This function is run to process the data. It should return an array of arrays in the same format of outputProcessing
def process(mainData, filePath, initial=False):
    values = list(outputDirect.values())
    new = False
    if initial:  # If loading a new file, grab new data
        # First get the modify date of the file, so changes can be detected

        print('/././././././././././././././')
        fileDate = os.path.getmtime(filePath)
        with shelve.open(shelveName, flag='c+b') as data:
            oldDate = None
            print('Shelve opened')
            if 'index' not in data.keys():
                print('No index found: Making new index')
                data['index'] = {}
            elif filePath in data['index']:
                print(f'Looking for: {filePath}')
                print(f"Index found: {data['index']}")
                oldDate = data['index']
                oldDate = oldDate[filePath]

                if oldDate == fileDate:
                    print('File exists in shelf!')
                    # The file is probably the same, so the data only needs to be un-shelved
                    mainData.updateProgress(50, 'Loading stored')
                    mainData.plotData = data[filePath]
                    return  # There's nothing more to do here, so back to the program
                else:
                    print('File is not up to date')
            else:
                print(f"Index found: {data['index']}")
                print(f'Looking for: {filePath}')
                print('File does not exist in index')

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

        new = True

    # /////////////////// Start of data processing /////////////////////////////

    db = mainData.plotData  # Simplify variable names
    bat = mainData.batterySpecs

    final = ['bepTSoc1', 'bepTSoc2', 'bepTSoc3']  # Stores the output part of the array
    current = ['B1Current', 'B2Current', 'B3Current']  # Stores the I input

    tmp = np.ones([len(mainData.plotData.index), 1])
    tmp[0] = 100
    # This for loop is doing peukert's and efficiency
    for index in range(3):
        mainData.updateProgress(0, final[index])
        if mainData.change[final[index]] or new:
            # deltaT, Capacity (Ah), Peukert's, Efficiency
            t, c, k, e = db['deltaT'], bat[index]['cap'], bat[index]['peu'], bat[index]['eff']

            for step, I in enumerate(db[current[index]]):
                if not step:
                    continue

                if I < 0:
                    tmp[step] = tmp[step - 1] - (t[step] / (20 * abs((c / (20 * I)) ** k)))
                elif I > 0:
                    tmp[step] = tmp[step - 1] + (t[step] / (c / (I * e)))

                if tmp[step] > 1:
                    tmp[step] = 1

                if step % (len(mainData.plotData.index) // 100):
                    mainData.updateProgress(step // (len(mainData.plotData.index) // 100))

            mainData.plotData[final[index]] = tmp * 100  # Add or update plot data

        mainData.change[final[index]] = False  # Mark the current variable as up to date

    with shelve.open(shelveName, flag='w+b') as data:
        data[filePath] = mainData.plotData  # Update the shelf with all of the plot data
    mainData.updateProgress(100, 'Plot processed!')
    print('Data processed')
