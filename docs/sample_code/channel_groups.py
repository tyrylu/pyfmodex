"""Sample code to show how to put channels into channel groups."""

import curses
import sys
import time

import pyfmodex
from pyfmodex.flags import MODE

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

system.init(maxchannels=6)


# Load some sounds
sounds = []
sounds.append(system.create_sound("media/drumloop.wav", mode=MODE.LOOP_NORMAL))
sounds.append(system.create_sound("media/jaguar.wav", mode=MODE.LOOP_NORMAL))
sounds.append(system.create_sound("media/swish.wav", mode=MODE.LOOP_NORMAL))
sounds.append(system.create_sound("media/c.ogg", mode=MODE.LOOP_NORMAL))
sounds.append(system.create_sound("media/d.ogg", mode=MODE.LOOP_NORMAL))
sounds.append(system.create_sound("media/e.ogg", mode=MODE.LOOP_NORMAL))

group_a = system.create_channel_group("Group A")
group_b = system.create_channel_group("Group B")
group_master = system.master_channel_group

# Instead of being independent, set the group A and B to be children of the
# master group
group_master.add_group(group_a)
group_master.add_group(group_b)

# Start all the sounds
for idx, sound in enumerate(sounds):
    system.play_sound(sound, channel_group=group_a if idx < 3 else group_b)

# Change the volume of each group, just because we can! (reduce overall noise)
group_a.volume = 0.5
group_b.volume = 0.5

# Main loop
def main(stdscr):
    """Draw a simple TUI, grab keypresses and let the user manipulate the
    channel groups.
    """
    stdscr.clear()
    stdscr.nodelay(True)

    # Create small visual display
    stdscr.addstr(
        "=======================\n"
        "Channel Groups Example.\n"
        "=======================\n"
        "\n"
        "Group A : drumloop.wav, jaguar.wav, swish.wav\n"
        "Group B : c.ogg, d.ogg, e.ogg\n"
        "\n"
        "Press a to mute/unmute group A\n"
        "Press b to mute/unmute group B\n"
        "Press m to mute/unmute master group\n"
        "Press q to quit"
    )

    while True:
        stdscr.addstr(
            12, 0, f"Channels playing: {system.channels_playing['channels']}\n"
        )

        # Listen to the user
        try:
            keypress = stdscr.getkey()
            if keypress == "a":
                group_a.mute = not group_a.mute
            elif keypress == "b":
                group_b.mute = not group_b.mute
            elif keypress == "m":
                group_master.mute = not group_master.mute
            elif keypress == "q":
                break
        except curses.error as cerr:
            if cerr.args[0] != "no input":
                raise cerr

        system.update()
        time.sleep(50 / 1000)

    # A little fade out
    if not (group_master.mute or group_a.mute and group_b.mute):
        pitch = 1.0
        volume = 1.0

        fadeout_sec = 3
        for _ in range(10 * fadeout_sec):
            group_master.pitch = pitch
            group_master.volume = volume

            volume -= 1 / (10 * fadeout_sec)
            pitch -= 0.25 / (10 * fadeout_sec)

            system.update()
            time.sleep(0.1)


curses.wrapper(main)

# Shut down
for sound in sounds:
    sound.release()

group_a.release()
group_b.release()

system.close()
system.release()
