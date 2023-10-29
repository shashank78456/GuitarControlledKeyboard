# Team HIGURE-RAKSHAS ( Namay, Shashank, Vatsal) : Control Keyboard and Mouse with literally anything that can create musical notes!

from scipy.io.wavfile import write
import sounddevice as sd  # Provides bindings for the PortAudio library (acquire and output real-time audio streams
# from your computer's hardware audio interfaces) and a few convenience functions to play and record NumPy arrays containing audio signals
import wave  # Interface for .wav file format
import struct  # Interpret bytes as packed binary data
import pyautogui  # Controls the mouse and keyboard to automate interactions with other applications
import math
import numpy as np
import sys  # Manipulate different parts of python runtime environment
import os  # Interact with OpSys
import pygame  # To create a new window

os.environ["SDL_VIDEO_WINDOW_POS"] = "%d,%d" % (0, 0)

# Interface

pygame.init()
w = 1270
h = 30
win = pygame.display.set_mode((w, h))
win.fill("white")
pygame.draw.rect(win, color="red", rect=(w - 100, 0, 100, 50))
font = pygame.font.SysFont("Arial", 20)
stop_text = font.render("STOP", True, "white")
win.blit(stop_text, (w - 80, 4))
keymap = font.render("A:ENTER     B:EXIT     C:UP     D:DOWN     E:LEFT     F:RIGHT     G:SPACE", True, "black")
win.blit(keymap, (250, 4))
pygame.display.flip()

# Quantization --> Conversion of Analog signals to Digital signals, capturing
# thousands of audio - samples per second.

fs = 48000  # (STANDARD VALUE) Sample rate - Number of samples per second that are taken of a waveform to
# create a discrete digital signal.
seconds = 0.5  # Duration of recording

while (True):
    try:
        # Recording sound and saving audio
        r = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype=np.int16)
        print("Recording")
        sd.wait()
        print("Finished recording")
        write('output.wav', fs, r)

        # reading audio file
        audio = wave.open("output.wav", "rb")
        l = audio.getnframes()

        # Converting Audio to Array using struct
        sound = []
        for i in range(l):
            wdata = audio.readframes(1)  # Write Data
            d = struct.unpack("<h", wdata)
            sound.append(int(d[0]))

        # Scaling to 0 - 1
        m = max(sound)
        if (m != 0):
            for i in range(l):
                sound[i] = sound[i] / m  # This gives a value between 0 and 1

        # Using Fast Fourier Transform ( fft )

        fourier = np.absolute(np.fft.fft(sound))

        imax = np.argmax(fourier)

        t = 0.3 * fourier[imax]

        for i in range(l):
            if (fourier[i] >= t):
                imax = i
                break

        # Calculating Frequency :

        frequency = round(imax * fs / (l * 2))  # Channel = 2 ; Dunno why but this worked! ;)
        print(frequency)

        # Stop button and Quit Config
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (w - 100 <= mouse[0] <= w):
                    sys.exit()

        # ------------------------------------------------------------------------------------------------

        if frequency >= 120:

            index = []
            for i in range(3, 8):
                index.append(i)

            alpha_index = ["C", "D", "E", "F", "G", "A", "B"]  # Notes used for control

            notes = []  # Containing 35 entries

            for i in range(0, 5):
                for j in range(7):
                    notes.append(alpha_index[j] + str(index[i]))

            # To find the note to perform the required action

            freq_C3 = 130.81

            freq_note = []
            freq_temp = freq_C3
            freq_note.append(round(freq_C3))
            for i in range(34):
                if notes[i][0] == 'B' or notes[i][0] == 'E':
                    print(notes[i][0], end=",")
                    freq_ele = freq_temp * math.pow(2, 1 / 12)
                    freq_temp = freq_ele
                else:
                    freq_ele = freq_temp * math.pow(2, 1 / 6)
                    freq_temp = freq_ele
                freq_note.append(round(freq_ele))

            delta = []  # To get to the desired Note
            for i in range(0, 35):
                delta.append(math.fabs(frequency - freq_note[i]))

            res = min(delta)
            alpha = notes[delta.index(res)]
            alpha_req = alpha[0]

            print(alpha_req)

            if alpha_req == "C":
                pyautogui.press(['up'])
                print("moving a step upwards")

            if alpha_req == "D":
                pyautogui.press(['down'])
                print("moving a step downwards")

            if alpha_req == "E":
                pyautogui.press(['left'])
                print("moving a step toward left")

            if alpha_req == "F":
                pyautogui.press(['right'])
                print("moving a step toward right")

            if alpha_req == "G":
                pyautogui.press(['space'])
                print("creating a space")

            if alpha_req == "A":
                pyautogui.press(['enter'])
                print("moving to next line")

            if alpha_req == "B":
                pyautogui.hotkey(['alt', 'f4'])
                print("exiting the window")
        else:
            print("frequency value out of feasible musical range! ")

        del audio, frequency, r, sound, fourier, l, imax, m, d, wdata

    except KeyboardInterrupt:
        break

# ------------------------------------------------------------------------------------------------

