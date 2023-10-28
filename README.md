# GuitarControlledKeyboard

Guitar ____ is a program which can be used to play games using a guitar (or use certain keys on the keyboard using guitar) . 
It makes the game more challenging and triggers your guitar playing abilities.

## Requirements

python3 and its
libraries and modules:
1. sounddevice
2. struct
3. math
4. numpy
5. scipy
6. wave
7. pyautogui
8. os
9. sys
10. pygame

## Instructions

Make sure you have the requirements installed
1. use git clone or download the zip file 
2. execute the ____.py file
3. The notes C,D,E,F,G,A,B on scales 3 to 7 have been assigned keys as follows:
   * C: "UP"
   * D: "DOWN"
   * E: "LEFT"
   * F: "RIGHT"
   * G: "SPACE"
   * A: "ENTER"
   * B: "EXIT"
4. Play the guitar and enjoy!!!

## Working
* The program records audio on regular intervals and stores it on a .wav file.
* It then read the file and constructs a bit array. This is where analog sound wave is 'digitalised'.
* It performs fourier transform on the array and calculates the dominating frequency in that audio data set.
* It then checks the frequency and performs the keyboard action.
* We have also implemented UI through pygame for the ease of the user.

