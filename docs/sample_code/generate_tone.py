"""Example code to show how play generated tones using System.play_dsp instead
of manually connecting and disconnecting DSP units.
"""

import curses
import sys
import time

import pyfmodex
from pyfmodex.enums import DSP_OSCILLATOR, DSP_TYPE

MIN_FMOD_VERSION = 0x00020108

# Create a System object and initialize.
system = pyfmodex.System()
VERSION = system.version
if VERSION < MIN_FMOD_VERSION:
    print(
        f"FMOD lib version {VERSION:#08x} doesn't meet "
        f"minimum requirement of version {MIN_FMOD_VERSION:#08x}"
    )
    sys.exit(1)

system.init(maxchannels=1)

# Create an oscillator DSP units for the tone.

dsp = system.create_dsp_by_type(DSP_TYPE.OSCILLATOR)
dsp.set_parameter_float(DSP_OSCILLATOR.RATE, 440)  # Musical note 'A'

# Main loop
def main(stdscr):
    """Draw a simple TUI, grab keypresses and let the user manipulate the
    DSP parameters.
    """
    stdscr.clear()
    stdscr.nodelay(True)

    # Create small visual display
    stdscr.addstr(
        "======================\n"
        "Generate Tone Example.\n"
        "======================\n"
        "\n"
        "Press 1 to play a sine wave\n"
        "Press 2 to play a sqaure wave\n"
        "Press 3 to play a saw wave\n"
        "Press 4 to play a triangle wave\n"
        "Press SPACE to stop the channel\n"
        "Press q to quit\n"
        "Press k and j to change volume\n"
        "Press h and l to change frequency"
    )

    channel = None
    while True:
        if channel:
            playing = "playing" if channel.is_playing else "stopped"
            volume = channel.volume
            frequency = channel.frequency
        else:
            playing = "stopped"
            volume = 0
            frequency = 0

        stdscr.move(13, 0)
        stdscr.clrtoeol()
        stdscr.addstr(f"Channel is {playing}")

        stdscr.move(14, 0)
        stdscr.clrtoeol()
        stdscr.addstr(f"Volume {volume:.2f}")

        stdscr.move(15, 0)
        stdscr.clrtoeol()
        stdscr.addstr(f"Frequency {frequency}")

        # Listen to the user
        try:
            keypress = stdscr.getkey()
            if keypress == "1":
                if channel:
                    channel.stop()
                channel = system.play_dsp(dsp, paused=True)
                channel.volume = 0.5
                dsp.set_parameter_int(DSP_OSCILLATOR.TYPE, 0)
                channel.paused = False
            elif keypress == "2":
                if channel:
                    channel.stop()
                channel = system.play_dsp(dsp, paused=True)
                channel.volume = 0.125
                dsp.set_parameter_int(DSP_OSCILLATOR.TYPE, 1)
                channel.paused = False
            elif keypress == "3":
                if channel:
                    channel.stop()
                channel = system.play_dsp(dsp, paused=True)
                channel.volume = 0.125
                dsp.set_parameter_int(DSP_OSCILLATOR.TYPE, 2)
                channel.paused = False
            elif keypress == "4":
                if channel:
                    channel.stop()
                channel = system.play_dsp(dsp, paused=True)
                channel.volume = 0.5
                dsp.set_parameter_int(DSP_OSCILLATOR.TYPE, 4)
                channel.paused = False
            elif keypress == " ":
                if channel:
                    channel.stop()
                channel = None
            elif keypress == "q":
                break

            if not channel:
                raise curses.error("no input")

            if keypress == "h":
                channel.frequency = max(channel.frequency - 500, 0)
            elif keypress == "j":
                channel.volume = max(channel.volume - 0.1, 0)
            elif keypress == "k":
                channel.volume = min(channel.volume + 0.1, 1)
            elif keypress == "l":
                channel.frequency = channel.frequency + 500
        except curses.error as cerr:
            if cerr.args[0] != "no input":
                raise cerr

        system.update()
        time.sleep(50 / 1000)


curses.wrapper(main)

# Shut down
dsp.release()
system.release()
