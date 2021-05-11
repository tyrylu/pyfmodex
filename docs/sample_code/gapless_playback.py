"""Example code to show how to schedule channel playback into the future with
sample accuracy. Uses several scheduled channels to synchronize two or more
sounds.
"""

import curses
import sys
import time
from enum import IntEnum

import pyfmodex
from pyfmodex.enums import TIMEUNIT
from pyfmodex.structobject import Structobject

MIN_FMOD_VERSION = 0x00020108


# pylint: disable=too-few-public-methods
class Note(IntEnum):
    """The notes we need to play our song."""

    C = 0
    D = 1
    E = 2


SONG = [
    Note.E,  # Ma-
    Note.D,  # ry
    Note.C,  # had
    Note.D,  # a
    Note.E,  # lit-
    Note.E,  # tle
    Note.E,  # lamb,
    Note.E,  # .....
    Note.D,  # lit-
    Note.D,  # tle
    Note.D,  # lamb,
    Note.D,  # .....
    Note.E,  # lit-
    Note.E,  # tle
    Note.E,  # lamb,
    Note.E,  # .....
    Note.E,  # Ma-
    Note.D,  # ry
    Note.C,  # had
    Note.D,  # a
    Note.E,  # lit-
    Note.E,  # tle
    Note.E,  # lamb,
    Note.E,  # its
    Note.D,  # fleece
    Note.D,  # was
    Note.E,  # white
    Note.D,  # as
    Note.C,  # snow.
    Note.C,  # .....
    Note.C,  # .....
    Note.C,  # .....
]

# Create a System object and initialize.
system = pyfmodex.System()
VERSION = system.version
if VERSION < MIN_FMOD_VERSION:
    print(
        f"FMOD lib version {VERSION:#08x} doesn't meet "
        f"minimum requirement of version {MIN_FMOD_VERSION:#08x}"
    )
    sys.exit(1)

system.init(maxchannels=len(SONG))

# Get information needed later for scheduling: the mixer block size, and the
# output rate of the mixer

dsp_block_len = system.dsp_buffer_size.size
output_rate = system.software_format.sample_rate

# Load our sounds - these are just sine wave tones at different frequencies.
sounds = [None] * len(Note)
sounds[Note.C] = system.create_sound("media/c.ogg")
sounds[Note.D] = system.create_sound("media/d.ogg")
sounds[Note.E] = system.create_sound("media/e.ogg")

# Create a channelgroup that the channels will play on.  We can use this
# channelgroup as our clock reference. It also means we can pause and pitch
# bend the channelgroup, without affecting the offsets of the delays, because
# the channelgroup clock which the channels feed off, will be pausing and
# speeding up/slowing down and still keeping the children in sync.
channelgroup = system.create_channel_group("Parent")

# Play all the sounds at once! Space them apart with set delay though so that
# they sound like they play in order.
CLOCK_START = 0
for note in SONG:

    # Pick a note from our tune
    sound = sounds[note]

    # Play the sound on the channelgroup we want to use as the parent clock
    # reference (for `delay` further down)
    channel = system.play_sound(sound, channelgroup, paused=True)

    if not CLOCK_START:
        CLOCK_START = channel.dsp_clock.parent_clock

        # Start the sound into the future, by two mixer blocks worth. Should be
        # enough to avoid the mixer catching up and hitting the clock value
        # before we've finished setting up everything. Alternatively the
        # channelgroup we're basing the clock on could be paused to stop it
        # ticking.
        CLOCK_START += dsp_block_len * 2
    else:
        # Get the length of the sound in samples
        sound_len = sound.get_length(TIMEUNIT.PCM)

        # Get the default frequency that the sound was recorded at
        freq = sound.default_frequency

        # Convert the length of the sound to 'output samples' for the output
        # timeline
        sound_len = int(sound_len / freq * output_rate)

        # Place the sound clock start time to this value after the last one
        CLOCK_START += sound_len

    # Schedule the channel to start in the future at the newly calculated
    # channelgroup clock value
    channel.delay = Structobject(dsp_start=CLOCK_START, dsp_end=0, stop_channels=False)

    # Unpause the sound. Note that you won't hear the sounds, they are
    # scheduled into the future.
    channel.paused = False

# Main loop
def main(stdscr):
    """Draw a simple TUI, grab keypresses and let the user manipulate the
    channel parameters.
    """
    stdscr.clear()
    stdscr.nodelay(True)

    # Create small visual display
    stdscr.addstr(
        "=========================\n"
        "Gapless Playback example.\n"
        "=========================\n"
        "\n"
        "Press SPACE to toggle pause\n"
        "Press k to increase pitch\n"
        "Press j to decrease pitch\n"
        "Press q to quit"
    )

    while True:
        paused_state = "Paused" if channelgroup.paused else "Playing"

        stdscr.move(9, 0)
        stdscr.clrtoeol()
        stdscr.addstr(
            f"Channels Playing {system.channels_playing.channels} : {paused_state}"
        )

        # Listen to the user
        try:
            keypress = stdscr.getkey()
            if keypress == " ":
                # Pausing the channelgroup, as the clock parent will pause any
                # scheduled sounds from continuing. If you paused the channel,
                # this would not stop the clock it is delayed against from
                # ticking, and you'd have to recalculate the delay for the
                # channel into the future again before it was unpaused.
                channelgroup.paused = not channelgroup.paused
            elif keypress == "k":
                for _ in range(50):
                    channelgroup.pitch += 0.01
                    system.update()
                    time.sleep(10 / 1000)
            elif keypress == "j":
                for _ in range(50):
                    if channelgroup.pitch > 0.1:
                        channelgroup.pitch -= 0.01
                        system.update()
                        time.sleep(10 / 1000)
            elif keypress == "q":
                break
        except curses.error as cerr:
            if cerr.args[0] != "no input":
                raise cerr

        system.update()
        time.sleep(50 / 1000)


curses.wrapper(main)

# Shut down
for sound in sounds:
    sound.release()
system.release()
