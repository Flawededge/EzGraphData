# EzGraphData
- Intro
    -
This is my first python gui based project

It will "eventually" be able to plot any time based data it's given (assuming that the .csv headers are set correctly)


- To do list
    -

- ~~Make the gui do stuff in the first place~~
    - ~~Add in file searching capability~~
    - Make the currently selected file be loaded
    - ~~Add in better looking symbols for spinner boxes~~
    - ~~Make check boxes change when data is loaded~~
    
- **Make a plot window and make it do the things**
    - Choose which plotter to use
    - Make separate window pop up
    - Make update button make a fresh plot

- Give a way to run a function to process each column differently

- Make the gui user friendly
    
- Give the entire interface a bit of pizazz
    - Make the 'No file loaded' label reflect current progress
    - Make the 'Not plotted yet' label reflect 
    
- 

And after that's done:

	1.0 → Sit back in awe at my first git project

    → Allow multiple data sets to be selected and overlayed
    → Add in an easy way to use functions to change how data is processed

- Get started guide
    - 

I'm using PyCharm with python 3.7 \
All of the dependencies can be grabbed with:

    pip3 install -r dependencies.txt
    
If you want to update the gui, the first 2 lines in the script recompiles the mainwindow.py from the mainwindow.ui. 
Feel free to disable these 2 lines, but they end up having no effect on the operation of the code

    import os
    os.system("pyuic5 mainwindow.ui > mainwindow.py")
    
