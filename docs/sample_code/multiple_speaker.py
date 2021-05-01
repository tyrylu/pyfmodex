"""Example code to show how to play sounds on multiple speakers."""

import curses
import sys
import time

import pyfmodex
from pyfmodex.enums import RESULT, SPEAKERMODE
from pyfmodex.exceptions import FmodError
from pyfmodex.flags import MODE, TIMEUNIT

MIN_FMOD_VERSION = 0x00020108

CHOICES = (
    "Mono from front left speaker",
    "Mono from front right speaker",
    "Mono from center speaker",
    "Mono from surround left speaker",
    "Mono from surround right speaker",
    "Mono from rear left speaker",
    "Mono from rear right speaker",
    "Stereo from front speakers",
    "Stereo from front speakers (channels swapped)",
    "Stereo (right only) from center speaker",
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

system.init(maxchannels=len(CHOICES))

speaker_mode = SPEAKERMODE(system.software_format.speaker_mode)

sound_mono = system.create_sound("media/drumloop.wav", mode=MODE.TWOD | MODE.LOOP_OFF)
sound_stereo = system.create_sound("media/stereo.ogg", mode=MODE.TWOD | MODE.LOOP_OFF)


def is_choice_available(choice_idx):
    """Is the given cofiguration choice available in the current speakermode?"""
    if speaker_mode in (SPEAKERMODE.MONO, SPEAKERMODE.STEREO):
        return choice_idx not in (2, 3, 4, 5, 6, 9)
    if speaker_mode == SPEAKERMODE.QUAD:
        return choice_idx not in (2, 5, 6, 9)
    if speaker_mode in (SPEAKERMODE.SURROUND, SPEAKERMODE.FIVEPOINTONE):
        return choice_idx not in (5, 6)

    return True


def play_sound(choice_idx):
    """Play a sound in the given configuration choice.

    Returns the created channel.
    """
    channel = None
    if choice_idx == 0:  # Mono front left
        channel = system.play_sound(sound_mono, paused=True)
        channel.set_mix_levels_output(1, 0, 0, 0, 0, 0, 0, 0)
        channel.paused = False
    elif choice_idx == 1:  # Mono front right
        channel = system.play_sound(sound_mono, paused=True)
        channel.set_mix_levels_output(0, 1, 0, 0, 0, 0, 0, 0)
        channel.paused = False
    elif choice_idx == 2:  # Mono centre
        channel = system.play_sound(sound_mono, paused=True)
        channel.set_mix_levels_output(0, 0, 1, 0, 0, 0, 0, 0)
        channel.paused = False
    elif choice_idx == 3:  # Mono surround left
        channel = system.play_sound(sound_mono, paused=True)
        channel.set_mix_levels_output(0, 0, 0, 0, 1, 0, 0, 0)
        channel.paused = False
    elif choice_idx == 4:  # Mono surround right
        channel = system.play_sound(sound_mono, paused=True)
        channel.set_mix_levels_output(0, 0, 0, 0, 0, 1, 0, 0)
        channel.paused = False
    elif choice_idx == 5:  # Mono read left
        channel = system.play_sound(sound_mono, paused=True)
        channel.set_mix_levels_output(0, 0, 0, 0, 0, 0, 1, 0)
        channel.paused = False
    elif choice_idx == 6:  # Mono read right
        channel = system.play_sound(sound_mono, paused=True)
        channel.set_mix_levels_output(0, 0, 0, 0, 0, 0, 0, 1)
        channel.paused = False
    elif choice_idx == 7:  # Stereo format
        channel = system.play_sound(sound_stereo)
    elif choice_idx == 8:  # Stereo front channel swapped
        matrix = [0, 1,
                  1, 0]
        channel = system.play_sound(sound_stereo, paused=True)
        channel.set_mix_matrix(matrix, 2, 2)
        channel.paused = False
    elif choice_idx == 8:  # Stereo (right only) center
        matrix = [0, 0,
                  0, 0,
                  0, 1]
        channel = system.play_sound(sound_stereo, paused=True)
        channel.set_mix_matrix(matrix, 3, 2)
        channel.paused = False
    return channel


# Main loop
def main(stdscr):
    """Draw a simple TUI, grab keypresses and let the user play the sounds."""
    stdscr.clear()
    stdscr.nodelay(True)

    # Create small visual display
    all_opts = speaker_mode.value >= SPEAKERMODE.SEVENPOINTONE.value
    stdscr.addstr(
        "=========================\n"
        "Multiple Speaker Example.\n"
        "=========================\n"
        "\n"
        "Press j or k to select mode\n"
        "Press SPACE to play the sound\n"
        "Press q to quit\n"
        "\n"
        f"Speaker mode is set to {speaker_mode.name}"
        " causing some speaker options to be unavailale"
        if not all_opts
        else ""
    )

    channel = None
    currentsound = None
    choice_idx = 0
    while True:
        stdscr.move(10, 0)
        for idx, choice in enumerate(CHOICES):
            available = is_choice_available(idx)
            sel = "-" if not available else "X" if choice_idx == idx else " "
            stdscr.addstr(f"[{sel}] {choice}\n")

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

        stdscr.move(11 + len(CHOICES), 0)
        stdscr.clrtoeol()
        stdscr.addstr(
            "Time %02d:%02d:%02d/%02d:%02d:%02d : %s\n"
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
        stdscr.addstr(f"Channels playing: {system.channels_playing.channels:-2d}")

        # Listen to the user
        try:
            keypress = stdscr.getkey()
            if keypress == "k":
                old_idx = choice_idx
                while True:
                    choice_idx = max(choice_idx - 1, 0)
                    if is_choice_available(choice_idx):
                        break
                    if choice_idx == 0:
                        choice_idx = old_idx
                        break
            elif keypress == "j":
                old_idx = choice_idx
                while True:
                    choice_idx = min(choice_idx + 1, len(CHOICES) - 1)
                    if is_choice_available(choice_idx):
                        break
                    if choice_idx == len(CHOICES) - 1:
                        choice_idx = old_idx
                        break
            elif keypress == " ":
                channel = play_sound(choice_idx)
            elif keypress == "q":
                break
        except curses.error as cerr:
            if cerr.args[0] != "no input":
                raise cerr

        system.update()
        time.sleep(50 / 1000)


curses.wrapper(main)

# Shut down
sound_mono.release()
sound_stereo.release()
system.release()
