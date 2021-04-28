"""Example code to show how to apply some built in software effects to sounds.
"""

import curses
import sys
import time

import pyfmodex
from pyfmodex.enums import (DSP_MULTIBAND_EQ, DSP_MULTIBAND_EQ_FILTER_TYPE,
                            DSP_TYPE)

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

mastergroup = system.master_channel_group
sound = system.create_sound("media/drumloop.wav")
channel = system.play_sound(sound)

# Create some effects to play with
dsplowpass = system.create_dsp_by_type(DSP_TYPE.MULTIBAND_EQ)
dsplowpass.set_parameter_int(
    DSP_MULTIBAND_EQ.A_FILTER, DSP_MULTIBAND_EQ_FILTER_TYPE.LOWPASS_24DB
)
dsplowpass.set_parameter_float(DSP_MULTIBAND_EQ.A_FREQUENCY, 1000)
dsplowpass.set_parameter_float(DSP_MULTIBAND_EQ.A_Q, 4)

dsphighpass = system.create_dsp_by_type(DSP_TYPE.MULTIBAND_EQ)
dsphighpass.set_parameter_int(
    DSP_MULTIBAND_EQ.A_FILTER, DSP_MULTIBAND_EQ_FILTER_TYPE.HIGHPASS_24DB
)
dsphighpass.set_parameter_float(DSP_MULTIBAND_EQ.A_FREQUENCY, 4000)
dsphighpass.set_parameter_float(DSP_MULTIBAND_EQ.A_Q, 4)

dspecho = system.create_dsp_by_type(DSP_TYPE.ECHO)

dsphighpass.set_parameter_float(DSP_MULTIBAND_EQ.A_FREQUENCY, 4000)
dsphighpass.set_parameter_float(DSP_MULTIBAND_EQ.A_Q, 4)
dspflange = system.create_dsp_by_type(DSP_TYPE.FLANGE)

# Add them to the master channel group.  Each time an effect is added (to
# position 0) it pushes the others down the list.
mastergroup.add_dsp(0, dsplowpass)
mastergroup.add_dsp(0, dsphighpass)
mastergroup.add_dsp(0, dspecho)
mastergroup.add_dsp(0, dspflange)

# By default, bypass all effects.  This means let the original signal go
# through without processing. It will sound 'dry' until effects are enabled by
# the user.
dsplowpass.bypass = True
dsphighpass.bypass = True
dspecho.bypass = True
dspflange.bypass = True

# Main loop
def main(stdscr):
    """Draw a simple TUI, grab keypresses and let the user manipulate the
    DSP states.
    """
    stdscr.clear()
    stdscr.nodelay(True)

    # Create small visual display
    stdscr.addstr(
        "================\n"
        "Effects Example.\n"
        "================\n"
        "\n"
        "Press SPACE to pause/unpause sound\n"
        "Press 1 to toggle dsplowpass effect\n"
        "Press 2 to toggle dsphighpass effect\n"
        "Press 3 to toggle dspecho effect\n"
        "Press 4 to toggle dspflange effect\n"
        "Press q to quit"
    )

    while True:
        stdscr.addstr(
            11,
            0,
            "%-8s: lowpass[%s] highpass[%s] echo [%s] flange[%s]"
            % (
                "Paused" if channel.paused else "Playing",
                " " if dsplowpass.bypass else "x",
                " " if dsphighpass.bypass else "x",
                " " if dspecho.bypass else "x",
                " " if dspflange.bypass else "x",
            ),
        )

        # Listen to the user
        try:
            keypress = stdscr.getkey()
            if keypress == " ":
                channel.paused = not channel.paused
            elif keypress == "1":
                dsplowpass.bypass = not dsplowpass.bypass
            elif keypress == "2":
                dsphighpass.bypass = not dsphighpass.bypass
            elif keypress == "3":
                dspecho.bypass = not dspecho.bypass
            elif keypress == "4":
                dspflange.bypass = not dspflange.bypass
            elif keypress == "q":
                break
        except curses.error as cerr:
            if cerr.args[0] != "no input":
                raise cerr

        system.update()
        time.sleep(50 / 1000)


curses.wrapper(main)

# Shut down
mastergroup.remove_dsp(dsplowpass)
mastergroup.remove_dsp(dsphighpass)
mastergroup.remove_dsp(dspecho)
mastergroup.remove_dsp(dspflange)

dsplowpass.release()
dsphighpass.release()
dspecho.release()
dspflange.release()

sound.release()
system.release()
