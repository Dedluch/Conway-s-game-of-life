# Conway's game of life simulated in Python
#### Description:
Simulation of Conway's game of life that runs in terminal made in python\
Check out this [wikipedia](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) page if not familiar with the concept
#### Usage
You need at least __Python 3.10__ and the libraries listed in requirements.txt by running\
```pip install -r requirements.txt```\
To lauch, run __main.py__ in a terminal window with specified arguments:\
-m or --Menu\
Runs with the menu that has some pre-installed patterns to check out\
-c or --Custom \<path-to-file\>\
Runs with the pattern represented in a RLE file of [specified format](https://conwaylife.com/wiki/Run_Length_Encoded)
#### Custom patterns
You can find and download some custom patterns [here](https://conwaylife.com/wiki/). In order to get them, expand Pattern files table and download shown RLE file.
#### Features
+ FPS limiter that works by pressing left or right arrow
+ Loading of custom patterns in RLE format
+ A few pre-decoded patterns if you don't want to download new ones
+ Dynamic array width to save performance when running on too big terminal window
### Documentation
The project consists of three python files:
+ main.py
+ decoder.py
+ patterns.py
#### main.py
This is where most of the code is. The program handles command line arguments, menu, logic for each of cells and updating the screen.\
##### main function
Handles menu, command line arguments, keyboard and has the main program loop running.
##### run function
checks every cell on the screen for rules of the game of life
##### initialize function
sets up the starting grid of cells and inserts specified pattern into it
##### update function
displays each generation on screen by printing each cell one by one
##### get_neighbors function
helper function that's used in _run_, counts living cells in 3x3 grid around specified cell
#### decoder.py
This file contains one function that's used for parsing RLE files, uses regex to check if file is of correct format and outputs 2D array of cells that is represented by the file
#### patterns.py
A collection of pre-decoded initial patterns that you can select through the menu in the main program, used a seperate file to not clutter the main script
### Exit codes of the main program
+ 0 - Simulation stopped by user
+ 1 - Too small terminal window to correctly display the pattern
+ 2 - Incorrect usage 
+ 3 - A problem with specified file
+ 4 - Error in menu selection, the default case