import pandas as pd
import numpy as np

# Config
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# These headers are checked if they are present, warnings will show if any are missing (can leave empty)
neededHeaders = ['Time', 'Supply Current', 'Supply Voltage', 'Load Current', 'Load Voltage', 'Soc1', 'Soc2', 'Soc3',
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
outputProcessing = ['bepTSoc1', 'bepTSoc2', 'bepTSoc3', 'deltaT']


# Processing
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


# This function is run to process the data. It should return an array of arrays in the same format of outputProcessing
# mainData.data is the full .csv file in a dictionary
def process(mainData, filePath, initial=False):
    values = list(outputDirect.values())
    values.append('Time')

    if initial:  # If loading a new file, grab new data
        mainData.data = pd.read_csv(open(filePath))
        try:
            mainData.plotData = mainData.data[values]
        except Exception as e:
            print(e)

        mainData.updateProgress(50, 'Data loaded')

        mainData.lines = len(mainData.data.index)
        mainData.stepWidth = mainData.lines // 100

        # Convert time to readable format
        mainData.plotData = mainData.plotData.assign(
            Time=pd.to_datetime(mainData.plotData['Time'], errors='coerce', format='%Y-%m-%d %H:%M:%S:%f'))

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

    # /////////////////// Start of data processing /////////////////////////////
    else:
        db = mainData.plotData  # Simplify variable names
        bat = mainData.batterySpecs

        final = ['bepTSoc1', 'bepTSoc2', 'bepTSoc3']  # Stores the output part of the array
        current = ['B1Current', 'B2Current', 'B3Current']  # Stores the I input

        mainData.updateProgress(0, 'Processing plot')

        # This for loop is doing peukert's and efficiency
        for index in range(3):
            # deltaT, Capacity (Ah), Peukert's, Efficiency
            t, c, k, e = db['deltaT'], bat[index]['cap'], bat[index]['peu'], bat[index]['eff']
            tmp = [100]
            cur = 1

            for step, I in enumerate(db[current[index]]):
                if not step:
                    continue

                if I < 0:
                    cur = cur - (t[step] / (20 * abs((c / (20 * I)) ** k)))
                elif I > 0:
                    cur = cur + (t[step] / (c / (I * e)))

                if cur > 1:
                    cur = 1

                # print(I, cur, t[step])

                tmp.append(cur * 100)

                if step % mainData.stepWidth:
                    mainData.updateProgress((step // (mainData.stepWidth * 3)) + (index * 33))

            db[final[index]] = tmp
        mainData.updateProgress(100, 'Plot processed!')
    print('Data processed')
