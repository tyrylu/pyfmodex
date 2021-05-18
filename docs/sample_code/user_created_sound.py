"""Example code to show how to create a sound with data filled by the user."""

import curses
import sys
import time
from ctypes import c_float, c_short, sizeof
from math import sin

import pyfmodex
from pyfmodex.callback_prototypes import (SOUND_PCMREADCALLBACK,
                                          SOUND_PCMSETPOSCALLBACK)
from pyfmodex.enums import RESULT, SOUND_FORMAT, TIMEUNIT
from pyfmodex.exceptions import FmodError
from pyfmodex.flags import MODE
from pyfmodex.structures import CREATESOUNDEXINFO

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

system.init()

# pylint: disable=invalid-name
# Using names common in mathematics
t1, t2 = c_float(0), c_float(0)  # time
v1, v2 = c_float(0), c_float(0)  # velocity


def pcmread_callback(sound_p, data_p, datalen_i):  # pylint: disable=unused-argument
    """Read callback used for user created sounds.

    Generates smooth noise.
    """

    # >>2 = 16bit stereo (4 bytes per sample)
    for _ in range(datalen_i >> 2):
        # left channel
        stereo16bitbuffer_left = int(sin(t1.value) * 32767)
        c_short.from_address(data_p).value = stereo16bitbuffer_left
        data_p += sizeof(c_short)

        # right channel
        stereo16bitbuffer_right = int(sin(t2.value) * 32767)
        c_short.from_address(data_p).value = stereo16bitbuffer_right
        data_p += sizeof(c_short)

        t1.value += 0.01 + v1.value
        t2.value += 0.0142 + v2.value
        v1.value += sin(t1.value) * 0.002
        v2.value += sin(t2.value) * 0.002

    return RESULT.OK.value


def pcmsetpos_callback(
    sound, subsound, position, timeunit
):  # pylint: disable=unused-argument
    """Set position callback for user created sounds or to intercept FMOD's
    decoder during an API setPositon call.

    This is useful if the user calls set_position on a channel and you want to
    seek your data accordingly.
    """
    return RESULT.OK.value


# Main loop
def main(stdscr):
    """Draw a simple TUI, grab keypresses and let the user select a sound
    generation method.
    """
    stdscr.clear()
    stdscr.nodelay(True)

    # Create small visual display
    stdscr.addstr(
        "===========================\n"
        "User Created Sound Example.\n"
        "==========================="
    )
    stdscr.refresh()

    subwin = stdscr.derwin(4, 0)
    subwin.nodelay(True)
    subwin.addstr(
        "Sound played here is generated in realtime. It will either play as a "
        "stream which means it is continually filled as it is playing, or it "
        "will play as a static sample, which means it is filled once as the "
        "sound is created, then, when played, it will just play that short "
        "loop of data.\n"
        "\n"
        "Press 1 to play an generated infinite stream\n"
        "Press 2 to play a static looping sample\n"
        "Press q to quit"
    )

    mode = MODE.OPENUSER | MODE.LOOP_NORMAL
    while True:
        # Listen to the user
        try:
            keypress = subwin.getkey()
            if keypress == "1":
                mode |= MODE.CREATESTREAM
                break
            if keypress == "2":
                break
            if keypress == "q":
                return
        except curses.error as cerr:
            if cerr.args[0] != "no input":
                raise cerr

        time.sleep(50 / 1000)

    # Create and play the sound
    numchannels = 2
    defaultfrequency = 44100
    exinfo = CREATESOUNDEXINFO(
        # Number of channels in the sound
        numchannels=numchannels,
        # Default playback rate of the sound
        defaultfrequency=defaultfrequency,
        # Chunk size of stream update in samples. This will be the amount of
        # data passed to the user callback.
        decodebuffersize=44100,
        # Length of PCM data in bytes of whole sound (for sound.get_length)
        length=defaultfrequency * numchannels * sizeof(c_short) * 5,
        # Data format of sound
        format=SOUND_FORMAT.PCM16.value,
        # User callback to reading
        pcmreadcallback=SOUND_PCMREADCALLBACK(pcmread_callback),
        # User callback to seeking
        pcmsetposcallback=SOUND_PCMSETPOSCALLBACK(pcmsetpos_callback),
    )
    sound = system.create_sound(0, mode=mode, exinfo=exinfo)
    channel = sound.play()

    subwin.clear()
    subwin.addstr("Press SPACE to toggle pause\n" "Press q to quit")
    row, _ = subwin.getyx()
    while True:
        is_playing = False
        paused = False
        position = 0
        length = 0
        if channel:
            try:
                is_playing = channel.is_playing
                paused = channel.paused
                position = channel.get_position(TIMEUNIT.MS)
                length = sound.get_length(TIMEUNIT.MS)

            except FmodError as fmoderror:
                if not fmoderror.result is RESULT.INVALID_HANDLE:
                    raise fmoderror

        subwin.move(row + 2, 0)
        subwin.clrtoeol()
        subwin.addstr(
            "Time %02d:%02d:%02d/%02d:%02d:%02d : %s"
            % (
                position / 1000 / 60,
                position / 1000 % 60,
                position / 10 % 100,
                length / 1000 / 60,
                length / 1000 % 60,
                length / 10 % 100,
                "Paused" if paused else "Playing" if is_playing else "Stopped",
            ),
        )

        # Listen to the user
        try:
            keypress = subwin.getkey()
            if keypress == " ":
                channel.paused = not channel.paused
            elif keypress == "q":
                break
        except curses.error as cerr:
            if cerr.args[0] != "no input":
                raise cerr

        system.update()
        time.sleep(50 / 1000)

    sound.release()


curses.wrapper(main)

# Shut down
system.release()
