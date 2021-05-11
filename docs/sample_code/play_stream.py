"""Example code to show how to simply play a stream such as an MP3 or WAV."""

import curses
import sys
import time
from pathlib import Path

import pyfmodex
from pyfmodex.enums import RESULT, TIMEUNIT
from pyfmodex.exceptions import FmodError
from pyfmodex.flags import MODE

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

# This example uses an FSB file, which is a preferred pack format for fmod
# containing multiple sounds. This could just as easily be exchanged with a
# wav/mp3/ogg file for example, but in that case you wouldn't need to check for
# subsounds. Because of the check below, this example would work with both
# types of sound file (packed vs single).
sound = system.create_stream("media/wave_vorbis.fsb", mode=MODE.LOOP_NORMAL)

sound_to_play = sound
if sound.num_subsounds:
    sound_to_play = sound.get_subsound(0)

# Main loop
def main(stdscr):
    """Draw a simple TUI, grab keypresses and let the user control playback."""
    stdscr.clear()
    stdscr.nodelay(True)

    # Create small visual display
    stdscr.addstr(
        "====================\n"
        "Play Stream Example.\n"
        "====================\n"
        "\n"
        "Press SPACE to toggle pause\n"
        "Press q to quit"
    )

    # Play the sound
    channel = sound_to_play.play()

    while True:
        is_playing = False
        position = 0
        length = 0
        try:
            is_playing = channel.is_playing
            position = channel.get_position(TIMEUNIT.MS)
            length = sound_to_play.get_length(TIMEUNIT.MS)
        except FmodError as fmoderror:
            if not fmoderror.result is RESULT.INVALID_HANDLE:
                raise fmoderror

        stdscr.move(7, 0)
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
                "Paused" if channel.paused else "Playing" if is_playing else "Stopped",
            ),
        )

        # Listen to the user
        try:
            keypress = stdscr.getkey()
            if keypress == " ":
                channel.paused = not channel.paused
            elif keypress == "q":
                break
        except curses.error as cerr:
            if cerr.args[0] != "no input":
                raise cerr

        system.update()
        time.sleep(50 / 1000)


curses.wrapper(main)

# Shut down
sound_to_play.release()
system.release()
