"""Example code to show how to enumerate the available recording drivers on
this device and work with them.
"""

import curses
import sys
import time
from collections import defaultdict
from ctypes import c_int, c_short, sizeof

import pyfmodex
from pyfmodex.enums import RESULT, SOUND_FORMAT
from pyfmodex.exceptions import FmodError
from pyfmodex.flags import DRIVER_STATE, MODE, SYSTEM_CALLBACK_TYPE
from pyfmodex.structures import CREATESOUNDEXINFO

MIN_FMOD_VERSION = 0x00020108
MAX_DRIVERS_IN_VIEW = 3
MAX_DRIVERS = 16

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

# Setup a callback so we can be notified if the record list has changed
def record_list_changed_callback(  # pylint: disable=unused-argument
    mysystem, callback_type, commanddata1, comanddata2, userdata
):
    """Increase a counter referenced by userdata."""
    _record_list_changed_count = c_int.from_address(userdata)
    _record_list_changed_count.value += 1

    return RESULT.OK.value


record_list_changed_count = c_int(0)
system.user_data = record_list_changed_count
system.set_callback(
    record_list_changed_callback, SYSTEM_CALLBACK_TYPE.RECORDLISTCHANGED
)


recordings = [defaultdict(bool) for _ in range(MAX_DRIVERS)]


def show_record_drivers(stdscr, selected_driver_idx, num_drivers):
    """Show an overview of detected record drivers."""
    row, _ = stdscr.getyx()
    for i in range(min(MAX_DRIVERS_IN_VIEW, num_drivers)):
        idx = (selected_driver_idx - MAX_DRIVERS_IN_VIEW // 2 + i) % num_drivers
        row += 2
        if idx == selected_driver_idx:
            stdscr.addstr(row, 0, ">")
        driver_info = system.get_record_driver_info(idx)
        statechar = "(*) " if driver_info.state & int(DRIVER_STATE.DEFAULT) else ""
        stdscr.addstr(row, 2, f"{idx}. {statechar}{driver_info.name.decode():41s}")
        row += 1
        stdscr.addstr(row, 2, f"{driver_info.system_rate/1000:2.1f}KHz")
        stdscr.addstr(row, 10, f"{driver_info.speaker_mode_channels}ch")
        data4 = driver_info.guid.data4.zfill(8).decode()
        stdscr.addstr(
            row,
            13,
            "{%08X-%04X-%04X-%04X-%02X%02X%02X%02X%02X%02X}"
            % (
                driver_info.guid.data1,
                driver_info.guid.data2,
                driver_info.guid.data3,
                int(data4[0]) << 8 | int(data4[1]),
                int(data4[2]),
                int(data4[3]),
                int(data4[4]),
                int(data4[5]),
                int(data4[6]),
                int(data4[7]),
            ),
        )
        row += 1
        stdscr.addstr(
            row,
            2,
            "(%s) (%s) (%s)"
            % (
                "Connected"
                if (driver_info.state & int(DRIVER_STATE.CONNECTED))
                else "Unplugged",
                "Recording" if system.is_recording(idx) else "Not recoding",
                "Playing"
                if recordings[idx]["channel"] and recordings[idx]["channel"].is_playing
                else "Not playing",
            ),
        )


# Main loop
def main(stdscr):
    """Draw a simple TUI, grab keypresses and let the user control recording
    and playback.
    """
    stdscr.clear()
    stdscr.nodelay(True)

    # Create small visual display
    stdscr.addstr(
        "===========================\n"
        "Record Enumeration Example.\n"
        "==========================="
    )

    selected_driver_idx = 0
    cur_y, _ = stdscr.getyx()
    while True:
        stdscr.move(cur_y + 2, 0)
        stdscr.clrtobot()
        stdscr.addstr(
            f"Record list has updated {record_list_changed_count.value} time(s)\n"
            f"Currently, {system.record_num_drivers.connected} recording device(s) are plugged in\n"
            "\n"
            "Press j and k to scroll list\n"
            "Press q to quit\n"
            "\n"
            "Press 1 to start/stop recording\n"
            "Press 2 to start/stop playback"
        )

        # Clamp the reported number of drivers to simplify this example
        num_drivers = min(system.record_num_drivers.drivers, MAX_DRIVERS)

        subwin = stdscr.subwin(cur_y + 9, 0)
        show_record_drivers(subwin, selected_driver_idx, num_drivers)

        # Listen to the user
        try:
            keypress = stdscr.getkey()
            if keypress == "j":
                selected_driver_idx = (selected_driver_idx + 1) % num_drivers
            elif keypress == "k":
                selected_driver_idx = (selected_driver_idx - 1) % num_drivers
            elif keypress == "q":
                break
            elif keypress == "1":
                if system.is_recording(selected_driver_idx):
                    system.record_stop(selected_driver_idx)
                else:
                    # Clean up previous record sound
                    if recordings[selected_driver_idx]["sound"]:
                        recordings[selected_driver_idx]["sound"].release()

                    # Query device native settings and start a recording
                    record_driver_info = system.get_record_driver_info(
                        selected_driver_idx
                    )
                    exinfo = CREATESOUNDEXINFO(
                        numchannels=record_driver_info.speaker_mode_channels,
                        format=SOUND_FORMAT.PCM16.value,
                        defaultfrequency=record_driver_info.system_rate,
                        # one second buffer; size here does not change the latency
                        length=record_driver_info.system_rate
                        * sizeof(c_short)
                        * record_driver_info.speaker_mode_channels,
                    )
                    sound = system.create_sound(
                        0, mode=MODE.LOOP_NORMAL | MODE.OPENUSER, exinfo=exinfo
                    )
                    recordings[selected_driver_idx]["sound"] = sound
                    try:
                        system.record_start(selected_driver_idx, sound, loop=True)
                    except FmodError as fmoderror:
                        if fmoderror.result != RESULT.RECORD_DISCONNECTED:
                            raise fmoderror
            elif keypress == "2":
                channel = recordings[selected_driver_idx]["channel"]
                sound = recordings[selected_driver_idx]["sound"]
                if channel and channel.is_playing:
                    channel.stop()
                    recordings[selected_driver_idx]["channel"] = False
                elif sound:
                    recordings[selected_driver_idx]["channel"] = sound.play()

        except curses.error as cerr:
            if cerr.args[0] != "no input":
                raise cerr

        system.update()
        time.sleep(50 / 1000)


curses.wrapper(main)

# Shut down
for recorder in recordings:
    if recorder["sound"]:
        recorder["sound"].release()
system.release()
