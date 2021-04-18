"""Sample code to show basic positioning of 3D sounds."""

import curses
import sys
import time
from math import sin

import pyfmodex
from pyfmodex.flags import MODE

INTERFACE_UPDATETIME = 50
DISTANCEFACTOR = 1
MIN_FMOD_VERSION = 0x00020108

# Create system object and initialize
system = pyfmodex.System()
VERSION = system.version
if VERSION < MIN_FMOD_VERSION:
    print(
        f"FMOD lib version {VERSION:#08x} doesn't meet "
        f"minimum requirement of version {MIN_FMOD_VERSION:#08x}"
    )
    sys.exit(1)

system.init(maxchannels=3)

THREED_SETTINGS = system.threed_settings
THREED_SETTINGS.distance_factor = DISTANCEFACTOR

# Load some sounds
sound1 = system.create_sound("media/drumloop.wav", mode=MODE.THREED)
sound1.min_distance = 0.5 * DISTANCEFACTOR
sound1.max_distance = 5000 * DISTANCEFACTOR
sound1.mode = MODE.LOOP_NORMAL

sound2 = system.create_sound("media/jaguar.wav", mode=MODE.THREED)
sound2.min_distance = 0.5 * DISTANCEFACTOR
sound2.max_distance = 5000 * DISTANCEFACTOR
sound2.mode = MODE.LOOP_NORMAL

sound3 = system.create_sound("media/swish.wav")

# Play sounds at certain positions
channel1 = system.play_sound(sound1, paused=True)
channel1.position = (-10 * DISTANCEFACTOR, 0, 0)
channel1.paused = False

channel2 = system.play_sound(sound2, paused=True)
channel2.position = (15 * DISTANCEFACTOR, 0, 0)
channel2.paused = False

# Main loop
def main(stdscr):
    """Draw a simple TUI, grab keypresses and let the user manipulate a simple
    environment with a listener and some sounds.
    """
    listener = system.listener(0)
    pos_ch1 = int((channel1.position[0]) / DISTANCEFACTOR) + 25
    pos_ch2 = int((channel2.position[0]) / DISTANCEFACTOR) + 25

    stdscr.clear()
    stdscr.nodelay(True)

    # Create small visual display
    stdscr.addstr(
        "===========\n"
        "3D Example.\n"
        "===========\n"
        "\n"
        "Press 1 to toggle sound 1 (16bit Mono 3D)\n"
        "Press 2 to toggle sound 2 (8bit Mono 3D)\n"
        "Press 3 to play a sound (16bit Stereo 2D)\n"
        "Press h or l to move listener (when in still mode)\n"
        "Press space to toggle listener still mode\n"
        "Press q to quit"
    )

    listener_automove = True
    listener_prevposx = 0
    listener_velx = 0
    clock = 0
    while True:
        tic = time.time()

        listener_posx = listener.position[0]
        environment = list("|" + 48 * "." + "|")
        environment[pos_ch1 - 1 : pos_ch1 + 2] = list("<1>")
        environment[pos_ch2 - 1 : pos_ch2 + 2] = list("<2>")
        environment[int(listener_posx / DISTANCEFACTOR) + 25] = "L"

        stdscr.addstr(11, 0, "".join(environment))
        stdscr.addstr("\n")

        # Listen to the user
        try:
            keypress = stdscr.getkey()
            if keypress == "1":
                channel1.paused = not channel1.paused
            elif keypress == "2":
                channel2.paused = not channel2.paused
            elif keypress == "3":
                system.play_sound(sound3)
            elif keypress == " ":
                listener_automove = not listener_automove
            elif keypress == "q":
                break

            if not listener_automove:
                if keypress == "h":
                    listener_posx = max(
                        -24 * DISTANCEFACTOR, listener_posx - DISTANCEFACTOR
                    )
                elif keypress == "l":
                    listener_posx = min(
                        23 * DISTANCEFACTOR, listener_posx + DISTANCEFACTOR
                    )
        except curses.error as cerr:
            if cerr.args[0] != "no input":
                raise cerr

        # Update the listener
        if listener_automove:
            listener_posx = sin(clock * 0.05) * 24 * DISTANCEFACTOR
        listener_velx = (listener_posx - listener_prevposx) * (
            1000 / INTERFACE_UPDATETIME
        )

        listener.position = (listener_posx, 0, 0)
        listener.velocity = (listener_velx, 0, 0)
        listener_prevposx = listener_posx

        clock += 30 * (1 / INTERFACE_UPDATETIME)
        system.update()

        toc = time.time()
        time.sleep(max(0, INTERFACE_UPDATETIME / 1000 - (toc - tic)))


curses.wrapper(main)

# Shut down
sound1.release()
sound2.release()
sound3.release()

system.close()
system.release()
