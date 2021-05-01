"""Example code to show how to play sounds on two diferent output devices from
the same application.
"""

import curses
import sys
import time

import pyfmodex
from pyfmodex.enums import OUTPUTTYPE
from pyfmodex.flags import MODE

MIN_FMOD_VERSION = 0x00020108


def fetch_driver(stdscr, system, name=""):
    """Draw a simple TUI, grab keypresses and let the user select a driver."""
    num_drivers = system.num_drivers
    if not num_drivers:
        system.output = OUTPUTTYPE.NOSOUND
        return 0

    selected_idx = 0
    drivers = [system.get_driver_info(idx).name.decode() for idx in range(num_drivers)]
    while True:
        stdscr.addstr(4, 0, "Choose a device for system ")
        stdscr.addstr(name, curses.A_BOLD)
        stdscr.addstr(
            "\n"
            "\n"
            "Use j and k to select\n"
            "Press SPACE to confirm\n"
            "\n"
        )

        for idx in range(num_drivers):
            sel = "X" if selected_idx == idx else " "
            stdscr.addstr(f"[{sel}] - {idx}. {drivers[idx]}\n")

        # Listen to the user
        try:
            keypress = stdscr.getkey()
            if keypress == "k":
                selected_idx = max(selected_idx - 1, 0)
            elif keypress == "j":
                selected_idx = min(selected_idx + 1, num_drivers - 1)
            elif keypress == " ":
                return selected_idx
        except curses.error as cerr:
            if cerr.args[0] != "no input":
                raise cerr

        time.sleep(50 / 1000)


# Main loop
def main(stdscr):
    """Draw a simple TUI, grab keypresses and let the user play some sounds."""
    stdscr.clear()
    stdscr.nodelay(True)

    # Create small visual display
    stdscr.addstr(
        "========================\n"
        "Multiple System Example.\n"
        "========================"
    )

    # Create Sound Card A
    system_a = pyfmodex.System()
    version = system_a.version
    if version < MIN_FMOD_VERSION:
        print(
            f"FMOD lib version {version:#08x} doesn't meet "
            f"minimum requirement of version {MIN_FMOD_VERSION:#08x}"
        )
        sys.exit(1)

    system_a.driver = fetch_driver(stdscr, system_a, "System A")
    system_a.init()

    # Create Sound Card B
    system_b = pyfmodex.System()
    system_b.driver = fetch_driver(stdscr, system_b, "System B")
    system_b.init()

    # Load one sample into each sound card
    sound_a = system_a.create_sound("media/drumloop.wav", mode=MODE.LOOP_OFF)
    sound_b = system_b.create_sound("media/jaguar.wav")

    stdscr.move(4, 0)
    stdscr.clrtobot()
    stdscr.addstr(
        "Press 1 to play a sound on device A\n"
        "Press 2 to play a sound on device B\n"
        "Press q to quit"
    )
    while True:
        stdscr.move(8, 0)
        stdscr.clrtobot()
        stdscr.addstr(
            f"Channels playing on A: {system_a.channels_playing.channels}\n"
            f"Channels playing on B: {system_b.channels_playing.channels}"
        )

        # Listen to the user
        try:
            keypress = stdscr.getkey()
            if keypress == "1":
                system_a.play_sound(sound_a)
            elif keypress == "2":
                system_b.play_sound(sound_b)
            elif keypress == "q":
                break
        except curses.error as cerr:
            if cerr.args[0] != "no input":
                raise cerr

        system_a.update()
        system_b.update()
        time.sleep(50 / 1000)

    # Shut down
    sound_a.release()
    system_a.release()

    sound_b.release()
    system_b.release()


curses.wrapper(main)
