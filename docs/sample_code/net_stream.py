"""Example code to show how to play streaming audio from an Internet source."""

import ctypes
import curses
import sys
import time

import pyfmodex
from pyfmodex.enums import OPENSTATE, RESULT, TAGDATATYPE, TAGTYPE
from pyfmodex.exceptions import FmodError
from pyfmodex.flags import MODE, TIMEUNIT
from pyfmodex.structobject import Structobject
from pyfmodex.structures import CREATESOUNDEXINFO

URL = "https://focus.stream.publicradio.org/focus.mp3"

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

# Increase the file buffer size a little bit to account for Internet lag
system.stream_buffer_size = Structobject(size=64 * 1024, unit=TIMEUNIT.RAWBYTES)

# Increase the default file chunk size to handle seeking inside large playlist
# files that may be over 2kb.
exinfo = CREATESOUNDEXINFO(filebuffersize=1024 * 16)

tags = {}


def show_tags(stdscr, sound, channel):
    """Read and print any tags that have arrived. This could, for example,
    happen if a radio station switches to a new song.
    """
    stdscr.move(11, 0)
    stdscr.addstr("Tags:\n")
    while True:
        try:
            tag = sound.get_tag(-1)
        except FmodError:
            break

        if tag.datatype == TAGDATATYPE.STRING.value:
            tag_data = ctypes.string_at(tag.data).decode()
            tags[tag.name.decode()] = (tag_data, tag.datalen)
            if tag.type == TAGTYPE.PLAYLIST.value and not tag.name == "FILE":
                # data point to sound owned memory, copy it before the
                # sound is released
                sound.release()
                sound = system.create_sound(
                    tag.data,
                    mode=MODE.CREATESTREAM | MODE.NONBLOCKING,
                    exinfo=exinfo,
                )
        elif tag.type == TAGTYPE.FMOD.value:
            # When a song changes, the sample rate may also change, so
            # compensate here
            if tag.name.decode() == "Sample Rate Change" and channel:
                channel.frequency = float(ctypes.string_at(tag.data).decode())

        stdscr.move(12, 0)
        stdscr.clrtobot()
        for name, value in tags.items():
            stdscr.addstr(f"{name} = '{value[0]}' ({value[1]} bytes)\n")


# Main loop
def main(stdscr):
    """Draw a simple TUI, grab keypresses and let the user control playback."""
    stdscr.clear()
    stdscr.nodelay(True)

    # Create small visual display
    stdscr.addstr(
        "===================\n"
        "Net Stream Example.\n"
        "===================\n"
        "\n"
        "Press SPACE to toggle pause\n"
        "Press q to quit\n"
    )

    sound = system.create_sound(
        URL, mode=MODE.CREATESTREAM | MODE.NONBLOCKING, exinfo=exinfo
    )

    channel = None
    while True:
        open_state = sound.open_state

        is_playing = False
        position = 0
        paused = False
        if channel:
            try:
                is_playing = channel.is_playing
                position = channel.get_position(TIMEUNIT.MS)
                paused = channel.paused

                # Silence the stream until we have sufficient data for smooth
                # playback
                channel.mute = open_state.starving
            except FmodError as fmoderror:
                if fmoderror.result not in (
                    RESULT.INVALID_HANDLE,
                    RESULT.CHANNEL_STOLEN,
                ):
                    raise fmoderror
        else:
            try:
                channel = system.play_sound(sound)
            except FmodError:
                # This may fail if the stream isn't ready yet, so don't check
                # for errors
                pass

        state = ""
        if open_state.state == OPENSTATE.BUFFERING:
            state = "Buffering..."
        elif open_state.state == OPENSTATE.CONNECTING:
            state = "Connecting..."
        elif paused:
            state = "Paused"
        elif is_playing:
            state = "Playing"

        if open_state.starving:
            state += " (STARVING)"

        stdscr.move(7, 0)
        stdscr.clrtoeol()
        stdscr.addstr(
            "Time = %02d:%02d:%02d\n"
            % (
                position / 1000 / 60,
                position / 1000 % 60,
                position / 10 % 100,
            ),
        )
        stdscr.addstr(
            f"State = {state}\n"
            f"Buffer Percentage = {open_state.percent_buffered}%"
        )

        show_tags(stdscr, sound, channel)

        # Listen to the user
        try:
            keypress = stdscr.getkey()
            if keypress == " ":
                if channel:
                    channel.paused = not channel.paused
            elif keypress == "q":
                break
        except curses.error as cerr:
            if cerr.args[0] != "no input":
                raise cerr

        system.update()
        time.sleep(50 / 1000)

    if channel:
        channel.stop()

    stdscr.clear()
    stdscr.addstr("Waiting for sound to finish opening before trying to release it...")
    stdscr.refresh()
    while True:
        if sound.open_state.state == OPENSTATE.READY:
            break
        system.update()
        time.sleep(50 / 1000)

    sound.release()


curses.wrapper(main)

# Shut down
system.release()
