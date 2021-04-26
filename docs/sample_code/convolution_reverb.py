"""Sample code to demonstrate how to set up a convolution reverb DSP and work
with it.
"""

import curses
import sys
import time
from ctypes import c_short, sizeof

import pyfmodex
from pyfmodex.enums import (CHANNELCONTROL_DSP_INDEX, DSP_CONVOLUTION_REVERB,
                            DSP_TYPE, DSPCONNECTION_TYPE, SOUND_FORMAT)
from pyfmodex.flags import MODE, TIMEUNIT

MIN_FMOD_VERSION = 0x00020108

# Create a System object and initialize
system = pyfmodex.System()
VERSION = system.version
if VERSION < MIN_FMOD_VERSION:
    print(
        f"FMOD lib version {VERSION:#08x} doesn't meet "
        f"minimum requirement of version {MIN_FMOD_VERSION:#08x}"
    )
    sys.exit(1)

system.init(maxchannels=1)

# Create a new channel group to hold the convolution DSP unit
reverbgroup = system.create_channel_group("reverb")

# Create a new channel group to hold all the channels and process the dry path
maingroup = system.create_channel_group("main")

# Create the convolution DSP unit and set it as the tail of the channel group
reverbunit = system.create_dsp_by_type(DSP_TYPE.CONVOLUTIONREVERB)
reverbgroup.add_dsp(CHANNELCONTROL_DSP_INDEX.TAIL, reverbunit)

# Open the impulse response wav file, but use FMOD_OPENONLY as we want to read
# the data into a seperate buffer
irsound = system.create_sound("media/standrews.wav", mode=MODE.DEFAULT | MODE.OPENONLY)

# For simplicity of the example, if the impulse response is the wrong format
# just display an error
if irsound.format.format != SOUND_FORMAT.PCM16:
    print(
        "Impulse Response file is the wrong audio format. It should be 16bit"
        " integer PCM data."
    )
    sys.exit(1)

# The reverb unit expects a block of data containing a single 16 bit int
# containing the number of channels in the impulse response, followed by PCM 16
# data
short_size = sizeof(c_short)
irsound_channels = irsound.format.channels
irsound_data_length = irsound.get_length(TIMEUNIT.PCMBYTES)
irdata = (c_short * (1 + irsound_data_length))()
irsound_data = irsound.read_data(irsound_data_length)[0]

irdata[0] = irsound_channels
irdata[1:] = list(irsound_data)

reverbunit.set_parameter_data(DSP_CONVOLUTION_REVERB.PARAM_IR, irdata)

# Don't pass any dry signal from the reverb unit, instead take the dry part of
# the mix from the main signal path
reverbunit.set_parameter_float(DSP_CONVOLUTION_REVERB.PARAM_DRY, -80)

# We can now release the sound object as the reverb unit has created its
# internal data
irsound.release()

# Load up and play a sample clip recorded in an anechoic chamber
sound = system.create_sound("media/singing.wav", mode=MODE.THREED | MODE.LOOP_NORMAL)
channel = system.play_sound(sound, channel_group=maingroup, paused=True)

# Create a send connection between the channel head and the reverb unit
channel_head = channel.get_dsp(CHANNELCONTROL_DSP_INDEX.HEAD)
reverb_connection = reverbunit.add_input(channel_head, DSPCONNECTION_TYPE.SEND)

channel.paused = False

# Main loop
def main(stdscr):
    """Draw a simple TUI, grab keypresses and let the user manipulate the
    reverb connection.
    """
    wet_volume = 1
    dry_volume = 1

    stdscr.clear()
    stdscr.nodelay(True)

    # Create small visual display
    stdscr.addstr(
        "====================\n"
        "Convolution Example.\n"
        "====================\n"
        "\n"
        "Press k and j to change dry mix\n"
        "Press h and l to change wet mix\n"
        "Press q to quit"
    )

    while True:
        stdscr.addstr(8, 0, f"wet mix [{wet_volume:.2f}] | dry mix [{dry_volume:.2f}]")

        # Listen to the user
        try:
            keypress = stdscr.getkey()
            if keypress == "h":
                wet_volume = max(wet_volume - 0.05, 0)
            elif keypress == "l":
                wet_volume = min(wet_volume + 0.05, 1)
            elif keypress == "j":
                dry_volume = max(dry_volume - 0.05, 0)
            elif keypress == "k":
                dry_volume = min(dry_volume + 0.05, 1)
            elif keypress == "q":
                break
        except curses.error as cerr:
            if cerr.args[0] != "no input":
                raise cerr

        reverb_connection.mix = wet_volume
        maingroup.volume = dry_volume

        system.update()
        time.sleep(50 / 1000)


curses.wrapper(main)

# Shut down
sound.release()
maingroup.release()
reverbgroup.remove_dsp(reverbunit)
reverbunit.disconnect_all(inputs=True, outputs=True)
reverbunit.release()
reverbgroup.release()
system.release()
