# EzGraphData
- Intro
    -
This is my first python gui based project

It will "eventually" be able to plot any time based data it's given (assuming that the .csv headers are set correctly)


- To do list
    -

- ~~Make the gui do stuff in the first place~~
    - ~~Add in file searching capability~~
    - ~~Make the currently selected file be loaded~~ ! Pressing the load button does this 
    - ~~Add in better looking symbols for spinner boxes~~ ! Can't do much about peukert's, they don't support floats
    - ~~Make check boxes change when data is loaded~~
    - ~~Add in processing of the data~~ ! Using Pandas library
    
- **Make a plot window and make it do the things**
    - ~~Choose which plotter to use~~ ! Using pyplot from matplotlib
    - ~~Make separate window pop up~~ ! Plot window appears
    - ~~Make update button make a fresh plot~~ It does that now
    
- Give the entire interface a bit of pizazz
    - ~~Make the 'No file loaded' label reflect current progress~~
    - ~~Add a progress bar~~ ! It shows progress, and there's a function to update it
    - ~~Add a line count~~ ! It's a thing
    
    Version 1.0 - Hurrah
    
Things I want to do after it's working

	→ Sit back in awe at my first git project
    → Allow multiple data sets to be selected and overlayed
    → Cache processed data to decrease the time to update plots
    → Add in an estimator of how long to go based off previous runs

- Hello world guide
    - 

I'm using PyCharm with python 3.7 https://www.jetbrains.com/pycharm/\

Once you're in the python interpreter
All of the dependencies can be grabbed with:

    pip3 install -r dependencies.txt
    
If you want to update the gui, the first 2 lines in the script recompiles the mainwindow.py from the mainwindow.ui. 
Feel free to disable these 2 lines, but they end up having no effect on the operation of the code

    import os
    os.system("pyuic5 mainwindow.ui > mainwindow.py")