"""Sample code to show basic positioning of 3D sounds."""

import sys
import time

import pyfmodex
from pyfmodex.flags import INIT_FLAGS, MODE

MIN_FMOD_VERSION = 0x00020108

# Create system object and initialize
system = pyfmodex.System()
VERSION = system.version
if VERSION < MIN_FMOD_VERSION:
    print(
        f"FMOD lib version 0x{VERSION:08x} doesn't meet "
        f"minimum requirement of version 0x{MIN_FMOD_VERSION:08x}"
    )
    sys.exit(1)

system.init(maxchannels=100, flags=INIT_FLAGS.NORMAL)

DISTANCEFACTOR = system.threed_settings.distance_factor

# Load some sounds
sound1 = system.create_sound("media/drumloop.wav", mode=MODE.THREED)
sound1.min_distance = 0.5 * DISTANCEFACTOR
sound1.max_distance = 5000 * DISTANCEFACTOR
sound1.mode = MODE.LOOP_NORMAL

sound2 = system.create_sound("media/jaguar.wav", mode=MODE.THREED)
sound2.min_distance = 0.5 * DISTANCEFACTOR
sound2.max_distance = 5000 * DISTANCEFACTOR
sound2.mode = MODE.LOOP_NORMAL

sound3 = system.create_sound("media/swish.wav", mode=MODE.TWOD)

# Play sounds at certain positions
channel1 = system.play_sound(sound1, paused=True)
channel1.position = (-10 * DISTANCEFACTOR, 0, 0)
channel1.paused = False

channel2 = system.play_sound(sound2, paused=True)
channel2.position = (15 * DISTANCEFACTOR, 0, 0)
channel2.paused = False

# Main loop
listener = system.listener(0)
POS_CH1 = int((channel1.position[0]) / DISTANCEFACTOR) + 25
POS_CH2 = int((channel2.position[0]) / DISTANCEFACTOR) + 25
while True:
    tic = time.time()
    LISTENER_POSX = listener.position[0]

    # Create small visual display
    print("===============================================")
    print("3D Example.")
    print("Copyright (c) Firelight Technologies 2004-2021.")
    print("===============================================")
    print()
    print("Press 1 to toggle sound 1 (16bit Mono 3D)")
    print("Press 2 to toggle sound 2 (8bit Mono 3D)")
    print("Press 3 to play a sound (16bit Stereo 2D)")
    print("Press h or l to move listener")
    print("Press q to quit")
    print()

    ENVIRONMENT = list("|" + 47 * "." + "|")
    ENVIRONMENT[POS_CH1 - 1 : POS_CH1 + 2] = list("<1>")
    ENVIRONMENT[POS_CH2 - 1 : POS_CH2 + 2] = list("<2>")
    ENVIRONMENT[int(LISTENER_POSX / DISTANCEFACTOR) + 25] = "L"

    print("".join(ENVIRONMENT))
    print()

    # Listen to the user
    keypress = input("Your input: ")
    if keypress == "1":
        channel1.paused = not channel1.paused
    elif keypress == "2":
        channel2.paused = not channel2.paused
    elif keypress == "3":
        system.play_sound(sound3, paused=False)
    elif keypress == "h":
        LISTENER_POSX = max(-24 * DISTANCEFACTOR, LISTENER_POSX - DISTANCEFACTOR)
    elif keypress == "l":
        LISTENER_POSX = min(23 * DISTANCEFACTOR, LISTENER_POSX + DISTANCEFACTOR)
    elif keypress == "q":
        break

    # Update the listener
    listener.position = [LISTENER_POSX, 0, 0]

    system.update()

# Shut down
sound1.release()
sound2.release()
sound3.release()

system.close()
system.release()
