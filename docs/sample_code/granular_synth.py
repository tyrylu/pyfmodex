"""Example code to show how to play a string of sounds together without gaps,
using `delay`, to produce a granular synthesis style trick engine effect.
"""

import curses
import random
import sys
import time

import pyfmodex
from pyfmodex.enums import RESULT
from pyfmodex.exceptions import FmodError
from pyfmodex.flags import MODE, TIMEUNIT
from pyfmodex.structobject import Structobject

MIN_FMOD_VERSION = 0x00020108

soundnames = (
    "media/granular/truck_idle_off_01.wav",
    "media/granular/truck_idle_off_02.wav",
    "media/granular/truck_idle_off_03.wav",
    "media/granular/truck_idle_off_04.wav",
    "media/granular/truck_idle_off_05.wav",
    "media/granular/truck_idle_off_06.wav",
)

# Create a System object and initialize.
system = pyfmodex.System()
VERSION = system.version
if VERSION < MIN_FMOD_VERSION:
    print(
        f"FMOD lib version {VERSION:#08x} doesn't meet "
        f"minimum requirement of version {MIN_FMOD_VERSION:#08x}"
    )
    sys.exit(1)

system.init(maxchannels=2)

output_rate = system.software_format.sample_rate
dsp_block_len = system.dsp_buffer_size.size
master_channel_group = system.master_channel_group

sounds = []
for soundname in soundnames:
    sounds.append(system.create_sound(soundname, mode=MODE.IGNORETAGS))


def queue_next_sound(playingchannel=None):
    """Queue the next sound."""
    newsound = sounds[random.randrange(0, len(sounds))]
    newchannel = system.play_sound(newsound, paused=True)

    start_delay = 0
    if playingchannel:
        # Get the start time of the playing channel
        start_delay = playingchannel.delay.dsp_start

        # Grab the length of the playing sound, and its frequency, so we can
        # calculate where to place the new sound on the time line
        sound_len = playingchannel.current_sound.get_length(TIMEUNIT.PCM)
        freq = playingchannel.frequency

        # Now calculate the length of the sound in 'output samples'. For
        # instance,  if a 44khz sound is 22050 samples long, and the output
        # rate is 48khz, then we want to delay by 24000 output samples
        sound_len = int(sound_len / freq * output_rate)

        # Add output rate adjusted sound length to the clock value of the
        # sound that is currently playing
        start_delay += sound_len
    else:
        start_delay = newchannel.dsp_clock.parent_clock
        start_delay += 2 * dsp_block_len

    # Set the delay of the new sound to the end of the old sound
    newchannel.delay = Structobject(
        dsp_start=start_delay, dsp_end=0, stop_channels=False
    )

    # Randomize pitch/volume to make it sound more realistic / random
    newchannel.frequency *= (
        1 + random.uniform(-1, 1) * .02
    )  # @22khz, range fluctuates from 21509 to 22491

    newchannel.volume *= 1 - random.random() * 0.2  # 0.8 to 1.0

    newchannel.paused = False

    return newchannel


# Main loop
def main(stdscr):
    """Draw a simple TUI, grab keypresses and let the user manipulate the
    channel paused state.
    """
    stdscr.clear()
    stdscr.nodelay(True)

    # Create small visual display
    stdscr.addstr(
        "====================================\n"
        "Granular Synthesis SetDelay Example.\n"
        "====================================\n"
        "\n"
        "Press SPACE to toggle pause\n"
        "Press q to quit"
    )

    # Kick off the first two sounds. First one is immediate, second one will be
    # triggered to start after the first one.
    channels = []
    channels.append(queue_next_sound())
    channels.append(queue_next_sound(channels[0]))

    slot = 0
    while True:
        paused_state = "paused" if master_channel_group.paused else "playing"

        stdscr.move(7, 0)
        stdscr.clrtoeol()
        stdscr.addstr(f"Channels are {paused_state}")

        # Replace the sound that just finished with a new sound, to create
        # endless seamless stitching!
        try:
            is_playing = channels[slot].is_playing
        except FmodError as fmoderror:
            if fmoderror.result != RESULT.INVALID_HANDLE:
                raise fmoderror

        if not is_playing and not master_channel_group.paused:
            # Replace sound that just ended with a new sound, queued up to
            # trigger exactly after the other sound ends
            channels[slot] = queue_next_sound(channels[1 - slot])
            slot = 1 - slot  # flip

        # Listen to the user
        try:
            keypress = stdscr.getkey()
            if keypress == " ":
                master_channel_group.paused = not master_channel_group.paused
            elif keypress == "q":
                break
        except curses.error as cerr:
            if cerr.args[0] != "no input":
                raise cerr

        system.update()
        # If you wait too long (longer than the length of the shortest sound),
        # you will get gaps.
        time.sleep(10 / 1000)


curses.wrapper(main)

# Shut down
for sound in sounds:
    sound.release()
system.release()
