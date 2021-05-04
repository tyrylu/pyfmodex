"""Example code to show how to load data into memory and read it from there."""

import curses
import mmap
import sys
import time
from pathlib import Path

import pyfmodex
from pyfmodex.enums import RESULT
from pyfmodex.exceptions import FmodError
from pyfmodex.flags import MODE, TIMEUNIT
from pyfmodex.structures import CREATESOUNDEXINFO

MIN_FMOD_VERSION = 0x00020108

mediadir = Path("media")
soundnames = (
    mediadir / "drumloop.wav",
    mediadir / "jaguar.wav",
    mediadir / "swish.wav",
)

# Create a System object and initialize
system = pyfmodex.System()
VERSION = system.version
if VERSION < MIN_FMOD_VERSION:
    print(
        f"FMOD lib version {VERSION:#08x} doesn't meet "
        f"minimum requirement of version {MIN_FMOD_VERSION:#08x}"
    )
    sys.exit(1)

system.init()

sounds = []
for filename in soundnames:
    with open(filename, mode="rb") as file_obj:
        with mmap.mmap(
            file_obj.fileno(), length=0, access=mmap.ACCESS_READ
        ) as mmap_obj:
            sounds.append(
                system.create_sound(
                    mmap_obj.read(),
                    mode=MODE.OPENMEMORY | MODE.LOOP_OFF,
                    exinfo=CREATESOUNDEXINFO(length=mmap_obj.size()),
                )
            )

# Main loop
def main(stdscr):
    """Draw a simple TUI, grab keypresses and let the user play the sounds."""
    stdscr.clear()
    stdscr.nodelay(True)

    # Create small visual display
    stdscr.addstr(
        "=========================\n"
        "Load From Memory Example.\n"
        "=========================\n"
        "\n"
        f"Press 1 to play a mono sound ({soundnames[0].stem})\n"
        f"Press 2 to play a mono sound ({soundnames[1].stem})\n"
        f"Press 3 to play a stero sound ({soundnames[2].stem})\n"
        "Press q to quit"
    )

    channel = None
    currentsound = None
    while True:
        is_playing = False
        position = 0
        length = 0
        if channel:
            try:
                is_playing = channel.is_playing
                position = channel.get_position(TIMEUNIT.MS)
                currentsound = channel.current_sound
                if currentsound:
                    length = currentsound.get_length(TIMEUNIT.MS)

            except FmodError as fmoderror:
                if fmoderror.result not in (
                    RESULT.INVALID_HANDLE,
                    RESULT.CHANNEL_STOLEN,
                ):
                    raise fmoderror

        stdscr.move(9, 0)
        stdscr.clrtoeol()
        stdscr.addstr(
            "Time %02d:%02d:%02d/%02d:%02d:%02d : %s"
            % (
                position / 1000 / 60,
                position / 1000 % 60,
                position / 10 % 100,
                length / 1000 / 60,
                length / 1000 % 60,
                length / 10 % 100,
                "Playing" if is_playing else "Stopped",
            ),
        )
        stdscr.addstr(10, 0, f"Channel Playing {system.channels_playing.channels:-2d}")

        # Listen to the user
        try:
            keypress = stdscr.getkey()
            if keypress in "123":
                channel = system.play_sound(sounds[int(keypress) - 1])
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
