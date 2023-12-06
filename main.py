from os import system, get_terminal_size, _exit, name
from time import sleep
from sys import argv

import numpy as np
import keyboard

import patterns
import decoder

SIZE = list(get_terminal_size())
HEIGHT = SIZE[1] - 3
PATTERN_OFFSET = (5,5)
FPS_LIMITER = 20


def main():
    #Checks for correct number of arguments
    if len(argv) not in [2, 3]:
        print("Usage: python ./Conway.py [-m --Menu] [-c --Custom <path-to-file>]")
        _exit(2)
    #Menu functionality
    elif len(argv) == 2 and argv[1] == "-m" or argv[1] == "--Menu":
        print("What pattern would you like to see?")
        print("1. Gosper's Glider Gun")
        print("2. Snark")
        print("3. Snark oscillator")
        print("4. AK-94")
        print("5. David Hilbert")
        print("6. Raccuci's p 38")
        while True:
            selection = input("Type the corresponding number and press ENTER: ")
            if not selection.isdigit():
                continue
            elif int(selection) in range(1, 7):
                break
        match int(selection):
            case 1:
                screen = initialize(patterns.gosperGliderGun)
            case 2:
                screen = initialize(patterns.snark)
            case 3:
                screen = initialize(patterns.snarkMore)
            case 4:
                screen = initialize(patterns.ak)
            case 5:
                screen = initialize(patterns.davidHilbert)
            case 6:
                screen = initialize(patterns.raccuci)
            case _:
                print("There was an error with your selection")
                _exit(4)
    #Custom pattern handling
    elif len(argv) == 3 and argv[1] == "-c" or argv[1] == "--Custom":
        pattern = decoder.decode(argv[2])
        #These statements check if the decoder returned a correct value of the type np.ndarray
        if type(pattern) == np.ndarray and pattern.size > 0:
            screen = initialize(pattern)
        elif type(pattern) == int and pattern == 1:
            print("Incorrect file format. Only runs on lifewiki RLE files")
            _exit(3)
        elif type(pattern) == int and pattern == 2:
            print("No such file found")
            _exit(3)
    else:
        print("Usage: python ./Conway.py [-m --Menu] [-c --Custom <path-to-file>]")
        _exit(2)
    width = len(screen[0])
    #main loop 
    try:
        while True:
            run(screen, width)
            global FPS_LIMITER
            if keyboard.is_pressed("left arrow") and FPS_LIMITER > 2:
                FPS_LIMITER -= 2
            if keyboard.is_pressed("right arrow") and FPS_LIMITER < 80:
                FPS_LIMITER += 2
    except KeyboardInterrupt:
        print("Simulation stopped by user")
        _exit(0)


#running the simulation
def run(screen, width):
    update(screen)
    buffer = screen.copy()
    #check the rules for every cell 
    for row in range(HEIGHT):
        for pixel in range(width):
            counter = get_neighbors(buffer, row, pixel)
            if buffer[row, pixel] == 1 and counter < 2 or counter > 3:
                screen[row, pixel] = 0
            elif (buffer[row, pixel] == 1 and counter == 2) or (buffer[row, pixel] == 0 and counter == 3):
                screen[row, pixel] = 1
    sleep(1 / FPS_LIMITER)


#sets the inital matrix of the game of life
def initialize(pattern):
    #sets the width to width of the pattern loaded + 3 times the offset
    #done to save on performance
    width = len(pattern[0]) + PATTERN_OFFSET[1] * 3
    board = np.zeros((HEIGHT, width), dtype=np.int8)
    if HEIGHT < len(pattern) or width < len(pattern[0]):
        print("Resize your terminal window and try again")
        _exit(1)
    #inserts loaded pattern into previously declared 2darray of zeros
    pos = PATTERN_OFFSET
    board[pos[0]:pos[0]+pattern.shape[0], pos[1]:pos[1]+pattern.shape[1]] = pattern
    return board


#prints current matrix of game of life
def update(screen):
    if name == "nt":
        system('cls')
    else:
        system("clear")
    for row in screen:
        for cell in row:
            if cell == 0:
                print(" ", end="")
            else:
                print("█", end="")
        print()
    print(f"Use arrow keys to increase/decrease FPS. Current FPS: {FPS_LIMITER} \nPress Ctrl + C to quit")


#returns number of neighbors that are of value 1
def get_neighbors(screen, x, y):
    height, width = len(screen), len(screen[0])
    result = 0
    for i in range(-1, 2):
       for j in range(-1, 2):
            #checks if currently indexed neighbor is not out of bounds
            if x + i < 0 or x + i > height - 1:
                continue
            elif y + j < 0 or y + j > width - 1:
                continue
            elif i == 0 and j == 0:
                continue
            else:
                result += screen[x + i][y + j]

    return result


if __name__ == "__main__":
    main()