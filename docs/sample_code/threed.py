"""Sample code to show basic positioning of 3D sounds."""

import curses
import sys

import pyfmodex
from pyfmodex.flags import MODE

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

system.init(maxchannels=3)

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
        "Press space to toggle listener auto moveement\n"
        "Press q to quit\n"
        "\n"
    )

    listener_automove = True
    listener_prevposx = 0
    while True:
        listener_posx = listener.position[0]

        environment = list("|" + 47 * "." + "|")
        environment[pos_ch1 - 1 : pos_ch1 + 2] = list("<1>")
        environment[pos_ch2 - 1 : pos_ch2 + 2] = list("<2>")
        environment[int(listener_posx / DISTANCEFACTOR) + 25] = "L"

        stdscr.addstr(11, 0, "".join(environment))
        stdscr.addstr("\n")

        # Listen to the user
        keypress = stdscr.getkey()
        if keypress == "1":
            channel1.paused = not channel1.paused
        elif keypress == "2":
            channel2.paused = not channel2.paused
        elif keypress == "3":
            system.play_sound(sound3)
        elif keypress == "h":
            listener_posx = max(-24 * DISTANCEFACTOR, listener_posx - DISTANCEFACTOR)
        elif keypress == "l":
            listener_posx = min(23 * DISTANCEFACTOR, listener_posx + DISTANCEFACTOR)
        elif keypress == "q":
            break

        # Update the listener
        listener.position = [listener_posx, 0, 0]
        listener_prevposx = listener_posx

        system.update()


curses.wrapper(main)

# Shut down
sound1.release()
sound2.release()
sound3.release()

system.close()
system.release()
