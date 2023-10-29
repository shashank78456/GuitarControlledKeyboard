from scipy.io.wavfile import write
import sounddevice as sd
import wave  # for .wav file format
import struct  # Interpret bytes as packed binary data
import pyautogui  # for keyboard input
import math
import numpy as np
import pygame  # for UI
import sys
import os

# repositioning of window
os.environ["SDL_VIDEO_WINDOW_POS"] = "%d,%d" % (0, 0)

# interface

# main window
pygame.init()
w = 1270
h = 30
win = pygame.display.set_mode((w, h))
win.fill("white")

#Stop button
pygame.draw.rect(win, color="red", rect=(w - 100, 0, 100, 50))
font = pygame.font.SysFont("Arial", 20)
stop_text = font.render("STOP", True, "white")
win.blit(stop_text, (w - 80, 4))

#Instruction bar
keymap = font.render("A:ENTER     B:EXIT     C:UP     D:DOWN     E:LEFT     F:RIGHT     G:SPACE", True, "black")
win.blit(keymap, (250, 4))

pygame.display.flip()

# Quantization --> Conversion of Analog signals to Digital signals, capturing
# thousands of audio - samples per second.

fs = 48000  # (STANDARD VALUE) Sample rate - Number of samples per second that are taken of a waveform to create a discete digital signal.
seconds = 0.5  # Duration of recording

while (True):

    try:

        # recording and saving sound
        r = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype=np.int16)
        sd.wait()
        write('output.wav', fs, r)

        # reading audio file
        audio = wave.open("output.wav", "rb")
        l = fs

        # converting audio to list of binary data
        sound = []
        for i in range(l):
            k = audio.readframes(1)
            bin_data = struct.unpack("<h", k)
            sound.append(int(bin_data[0]))

        # scaling to 0-1
        m = max(sound)
        if (m != 0):
            for i in range(l):
                sound[i] = sound[i] / m

        # fourier transform
        fourier = np.absolute(np.fft.fft(sound))

        imax = np.argmax(fourier)

        t = 0.3 * fourier[imax]
        for i in range(l):
            if (fourier[i] >= t):
                imax = i
                break

        # calculating frequency
        frequency = round(imax * fs / (l * 2))  # channel = 2, Dunno why but this worked
        print(frequency)

        # Stop button and Quit configuration
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (w - 100 <= mouse[0] <= w):
                    sys.exit()

        # assigning keys
        if frequency >= 120:

            index = []
            for i in range(3, 8):
                index.append(i)

            alpha_index = ["C", "D", "E", "F", "G", "A", "B"]

            notes = []  # containing 42 entries
            for i in range(0, 5):
                for j in range(7):
                    notes.append(alpha_index[j] + str(index[i]))

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

            # checking input frequencies
            delta = []
            for i in range(0, 35):
                delta.append(math.fabs(frequency - freq_note[i]))

            res = min(delta)
            alpha = notes[delta.index(res)]
            alpha_req = alpha[0]

            print(alpha_req)

            # A:ENTER     B:EXIT     C:UP     D:DOWN     E:LEFT     F:RIGHT     G:SPACE
            if alpha_req == "C":
                pyautogui.press('up')
                print("Moving a step upwards")

            if alpha_req == "D":
                pyautogui.press('down')
                print("Moving a step downwards")

            if alpha_req == "E":
                pyautogui.press('left')
                print("Moving a step toward left")

            if alpha_req == "F":
                pyautogui.press('right')
                print("Moving a step toward right")

            if alpha_req == "G":
                pyautogui.press('space')
                print("Creating a space")

            if alpha_req == "A":
                pyautogui.press('enter')
                print("Moving to next line")

            if alpha_req == "B":
                pyautogui.hotkey('alt', 'f4')
                print("Exiting the window")

        del audio, frequency, r, sound, fourier, l, imax, m, bin_data, k

    except KeyboardInterrupt:
        break

# ----------------------------------------------------------------

