"""Example code to demonstrate how to manipulate DSP network to have two
different effects on seperately filtered, different audio paths from a single
sound.
"""

import curses
import sys
import time

import pyfmodex
from pyfmodex.enums import (CHANNELCONTROL_DSP_INDEX, DSP_MULTIBAND_EQ,
                            DSP_MULTIBAND_EQ_FILTER_TYPE, DSP_TYPE,
                            SPEAKERMODE)
from pyfmodex.flags import MODE
from pyfmodex.structobject import Structobject

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

# In this special case we want to use stereo output and not worry about varying
# matrix sizes depending on user speaker mode
software_format = Structobject(
    sample_rate=48000, speaker_mode=SPEAKERMODE.STEREO, raw_speakers=0
)
system.software_format = software_format

# Initialize FMOD
system.init(maxchannels=1)

sound = system.create_sound("media/drumloop.wav", mode=MODE.LOOP_NORMAL)
channel = system.play_sound(sound)

# Create the DSP effects
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

# Connect up the DSP network

# When a sound is played, a subnetwork is set up in the DSP network which looks
# like this (wavetable is the drumloop sound, and it feeds its data from right
# to left):
#
# [DSPHEAD]<---[DSPCHANNELMIXER]<---[CHANNEL HEAD]<---[WAVETABLE - DRUMLOOP.WAV]
group_master = system.master_channel_group
dsphead = group_master.get_dsp(CHANNELCONTROL_DSP_INDEX.HEAD)
dspchannelmixer, _ = dsphead.get_input(0)

# Now disconnect channeldsp head from the wavetable to make it look like this:
#
# [DSPHEAD]    [DSPCHANNELMIXER]<---[CHANNEL HEAD]<---[WAVETABLE - DRUMLOOP.WAV]
dsphead.disconnect_from(dspchannelmixer)

# Now connect the two effects to channeldsp head and store the two connections
# this makes so we can set their matrix later

#           [DSPLOWPASS]
#          /x
# [DSPHEAD]    [DSPCHANNELMIXER]<---[CHANNEL HEAD]<---[WAVETABLE - DRUMLOOP.WAV]
#          \y
#           [DSPHIGHPASS]
dsplowpassconnection = dsphead.add_input(dsplowpass)  # x
dsphighpassconnection = dsphead.add_input(dsphighpass)  # y

# Now connect the channelmixer to the 2 effects
#           [DSPLOWPASS]
#          /x          \
# [DSPHEAD]             [DSPCHANNELMIXER]<---[CHANNEL HEAD]<---[WAVETABLE - DRUMLOOP.WAV]
#          \y          /
#           [DSPHIGHPASS]

dsplowpass.add_input(dspchannelmixer)  # Ignore connection - we dont care about it.
dsphighpass.add_input(dspchannelmixer)  # Ignore connection - we dont care about it.

# Now the drumloop will be twice as loud, because it is being split into 2,
# then recombined at the end. What we really want is to only feed the
# dsphead<-dsplowpass through the left speaker for that effect, and
# dsphead<-dsphighpass to the right speaker for that effect. We can do that
# simply by setting the pan, or speaker matrix of the connections

#           [DSPLOWPASS]
#          /x=1,0      \
# [DSPHEAD]             [DSPCHANNELMIXER]<---[CHANNEL HEAD]<---[WAVETABLE - DRUMLOOP.WAV]
#          \y=0,1      /
#           [DSPHIGHPASS]

lowpassmatrix = [
    1, 0,  # output to front left: take front left input signal at 1
    0, 0,  # output to front right: silence
]
highpassmatrix = [
    0, 0,  # output to front left: silence
    0, 1,  # output to front right: take front right input signal at 1
]

# Upgrade the signal coming from the channel mixer from mono to stereo
# Otherwise the lowpass and highpass will get mono signals
dspchannelmixer.channel_format = Structobject(
    channel_mask=0, num_channels=0, source_speaker_mode=SPEAKERMODE.STEREO
)

# Now set the above matrices
dsplowpassconnection.set_mix_matrix(lowpassmatrix, 2, 2)
dsphighpassconnection.set_mix_matrix(highpassmatrix, 2, 2)

dsplowpass.bypass = True
dsphighpass.bypass = True

dsplowpass.active = True
dsphighpass.active = True

# Main loop
def main(stdscr):
    """Draw a simple TUI, grab keypresses and let the user manipulate the
    DSP states.
    """
    pan = 0

    stdscr.clear()
    stdscr.nodelay(True)

    # Create small visual display
    stdscr.addstr(
        "==============================\n"
        "DSP Effect Per Speaker Sample.\n"
        "==============================\n"
        "\n"
        "Press 1 to toggle lowpass (left speaker)\n"
        "Press 2 to toggle highpass (right speaker)\n"
        "Press h and l to pan sound\n"
        "Press q to quit"
    )

    while True:
        stdscr.addstr(
            10,
            0,
            f"Lowpass (left) is {'inactive' if dsplowpass.bypass else 'active  '}",
        )
        stdscr.addstr(
            11,
            0,
            f"Highpass (right) is {'inactive' if dsphighpass.bypass else 'active  '}",
        )
        stdscr.addstr(12, 0, f"Pan is {pan:.1f} ")

        # Listen to the user
        try:
            keypress = stdscr.getkey()
            if keypress == "1":
                dsplowpass.bypass = not dsplowpass.bypass
            elif keypress == "2":
                dsphighpass.bypass = not dsphighpass.bypass
            elif keypress == "h":
                pan = max(pan - 0.1, -1)
                channel.set_pan(pan)
            elif keypress == "l":
                pan = min(pan + 0.1, 1)
                channel.set_pan(pan)
            elif keypress == "q":
                break
        except curses.error as cerr:
            if cerr.args[0] != "no input":
                raise cerr

        system.update()
        time.sleep(50 / 1000)


curses.wrapper(main)

# Shut down
sound.release()
dsplowpass.release()
dsphighpass.release()
system.release()
