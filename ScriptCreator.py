inputFilename = 'F:\\Dtan Temp\\ForChrisDiggle\\Battery scripts\\Pseudo Scripts\\YAM6AGM.txt'
outputFilename = 'scriptOutput.txt'
capacity = 130  # Capacity in Ah
startCount = 0

with open(inputFilename) as f:
    out = ''
    curPer = 100
    for count, i in enumerate(f.readlines()):
        count = count + startCount
        print(i[:-1], end='')
        i = i.split()
        if i[0] == 'per':  # Percent  \////////////////////////////////////////////////////////////////////////////////\
            current = float(i[1]) * capacity
            print(f'| Percent, {i[1]}C, {i[2]}A')
            if i[3] == '-':  # Discharging
                curPer -= int(i[2])
                out += f'''{count}0,LOAD,SET,,CC,14.4,{current},Step {count}
{count}1,LOAD,ON,,,,,
{count}8,BMS,WAITUNDERSOCJMP,{count}9,1,{curPer},,Discharge {current}A till {curPer}
{count}9,LOAD,OFF,,,,,\n'''
            elif i[3] == '+':  # Charging
                curPer += int(i[2])
                out += f'''{count}0,SOURCE,SET,,CC,14.4,{current},Step {count}
{count}1,SOURCE,ON,,,,,
{count}8,BMS,WAITOVERSOCJMP,{count}9,1,{curPer},,Discharge {current}A till {curPer}
{count}9,SOURCE,OFF,,,,,\n'''

        elif i[0] == 'tim':  # Time  \/////////////////////////////////////////////////////////////////////////////////\
            current = float(i[1]) * capacity
            time = int(i[2])
            print(f'| Percent, {i[1]}C, {i[2]}A')
            if i[3] == '-':  # Discharging
                out += f'''{count}0,LOAD,SET,,CC,14.4,{current},Step {count}
{count}1,LOAD,ON,,,,,
{count}8,LOAD,WAITTIME,{time},,,,Discharge {current}A for {time} min
{count}9,LOAD,OFF,,,,,\n'''
            elif i[3] == '+':  # Charging
                out += f'''{count}0,SOURCE,SET,,CC,14.4,{current},Step {count}
{count}1,SOURCE,ON,,,,,
{count}8,SOURCE,WAITTIME,{time},,,,Discharge for {time} at {current}A
{count}9,SOURCE,OFF,,,,,\n'''

        elif i[0] == 'chg':  # Charge \////////////////////////////////////////////////////////////////////////////////\
            current = float(i[1]) * capacity
            under = float(i[2]) * capacity
            afterWait = int(i[3])

            out += f'''{count}0,SOURCE,SET,,CC,14.4,{current},Charge at {current}A until {under}A threshold
{count}1,SOURCE,ON,,,,,
{count}2,SOURCE,WAITUNDERCURRENT,,,,{under},
{count}8,SOURCE,WAITTIME,{afterWait},,,,Wait an extra {afterWait} min at {current}A
{count}9,SOURCE,OFF,,,,,\n'''

        elif i[0] == 'vlt':  # Wait under volt \///////////////////////////////////////////////////////////////////////\
            current = float(i[1]) * capacity
            underVolt = float(i[2])

            out += f'''{count}0,LOAD,SET,,CC,14.4,{current},0.05C down to 10.8v
{count}1,LOAD,ON,,,,,
{count}2,LOAD,WAITUNDERVOLT,,,{underVolt},,20c discharge end point
{count}3,LOAD,OFF,,,,,\n'''

with open(outputFilename, 'w+') as f:
    f.write(out)

quit()
