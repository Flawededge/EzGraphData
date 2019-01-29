# EzGraphData - Changelog
- Changelog
    -
This is going to be where I keep track of a to do list and changelog. The changes by version are going 

- To do list
    -
    
- Stuff I want to do in the future (Grows as I think of things)


    → Make a save plots button, where a range of predefined plots get saved to a folder
    → Add in a seperate window with useful formulae. Peukert's, internal resistance... 


- Changelog
    -

- **1.0 → 1.1 - Optimization branch -  File loading**

1.0.3 → 1.0.4

    - Added my own SoC implementation based off the confrence below
        → Still needs a lot of work, but it is getting pretty confusing
    - Moved the custom plot labels to the top
    - Rearranged the interface again. Still have some bits to add to it related to tuning my algorithm
    
Reference: 

‘A novel comprehensive evaluation method for state-of-health of lead-acid batteries’ (2018) 2018 International Conference on Power System Technology (POWERCON), Power System Technology (POWERCON), 2018 International Conference on, p. 3765. doi: 10.1109/POWERCON.2018.8601795.
    
1.0.2 → 1.0.3

    - Selecting multiple files at once to plot all of them at once
    - Changed the Peukert's equation around a bit to make it more accurate to what i'm comparing it to
    - Removed the original sample data, as it was too large for git, added in a couple different examples
        which should hopefully be a little bit more manageable

1.0.1 → 1.0.2

    - Redoing my processing, as it was taking too long
        - Have changed all the math to NumPy vectorised math, which makes it almost instant
        - Because it's so fast, i've added a plot to the on release of the sliders
    - Restructured the batterySpecs array to be easier to work with 
        - I did end up doing this, but it didn't help with the vector math as I had hoped, so no functional difference
    - Added in a check box to choose whether to clear the plot or keep the previous lines on it
    - Changed and moved the interface around to make it more compact, but more feature rich
        - Changed the spinners to doubleSpinners, as it makes more sense with the numbers I want to put in them
        - Removed sliders, as they don't properly interact with doubleSpinners
        - Added in a marked points box, which will display the max and min if you want
        - Added in a clear plot box to stack multiple lines on top of each other
        - Removed and moved a few of the text boxes, as they weren't adding anything to the display
    
1.0 → 1.0.1

    This version still has some issues. I'm going to make some changes to processing, so this is a backup if all goes wrong
    - Added in shelving. Any loaded and processed data will be saved in the 3 data.* files
    - Optimised my processing with a NumPy array. The access times seem to be better
    - Added in a '(Loaded in {time}s)' to give an indication of how efficient the loading is
    

- **Pre 1.0**
    - Make the gui do stuff in the first place
    - Add in file searching capability
    - Make the currently selected file be loaded 
        - Pressing the load button does this 
    - Add in better looking symbols for spinner boxes 
        - Can't do much about peukert's, they don't support floats
    - Make check boxes change when data is loaded
    - Add in processing of the data 
        - Using Pandas library
    
- **Make a plot window and make it do the things**
    - Choose which plotter to use → Using pyplot from matplotlib
    - Make separate window pop up → Plot window appears
    - Make update button make a fresh plot → It does that now
    
- Give the entire interface a bit of pizazz
    - Make the 'No file loaded' label reflect current progress
    - Add a progress bar → It shows progress, and there's a function to update it
        Add a line count → It's a thing
