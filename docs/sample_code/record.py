"""Example code to show how to record continuously and play back the same data
while keeping a specified latency between the two.
"""

import curses
import sys
import time
from ctypes import c_short, sizeof

import pyfmodex
from pyfmodex.enums import RESULT, SOUND_FORMAT
from pyfmodex.exceptions import FmodError
from pyfmodex.flags import MODE, TIMEUNIT
from pyfmodex.reverb_presets import REVERB_PRESET
from pyfmodex.structure_declarations import CREATESOUNDEXINFO
from pyfmodex.structures import REVERB_PROPERTIES

MIN_FMOD_VERSION = 0x00020108

# Some devices will require higher latency to avoid glitches
LATENCY_MS = 50
DRIFT_MS = 1
RECORD_DEVICE_INDEX = 0

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

if not system.record_num_drivers:
    print("No recording devices found/plugged in! Aborting.")
    sys.exit(1)

# Determine latency in samples
record_driver_info = system.get_record_driver_info(RECORD_DEVICE_INDEX)

# The point where we start compensating for drift
drift_threshold = record_driver_info.system_rate * DRIFT_MS / 1000
# User specified latency
desired_latency = record_driver_info.system_rate * LATENCY_MS / 1000

# Create user sound to record into, then start recording
exinfo = CREATESOUNDEXINFO(
    numchannels=record_driver_info.speaker_mode_channels,
    format=SOUND_FORMAT.PCM16.value,
    defaultfrequency=record_driver_info.system_rate,
    length=record_driver_info.system_rate  # one second buffer; size here does
    * sizeof(c_short)  # not change the latency
    * record_driver_info.speaker_mode_channels,
)
sound = system.create_sound(0, mode=MODE.LOOP_NORMAL | MODE.OPENUSER, exinfo=exinfo)
system.record_start(RECORD_DEVICE_INDEX, sound, loop=True)
sound_len = sound.get_length(TIMEUNIT.PCM)

# Main loop
def main(stdscr):
    """Draw a simple TUI, grab keypresses and let the user control playback."""
    stdscr.clear()
    stdscr.nodelay(True)

    dsp_enabled = False

    # Create small visual display
    stdscr.addstr(
        "===============\n"
        "Record Example.\n"
        "===============\n"
        "\n"
        "(Adjust LATENCY_MS in the source to compensate for stuttering)\n"
        f"(Current value is {LATENCY_MS}ms)"
    )

    reverb_on = REVERB_PROPERTIES(*REVERB_PRESET.CONCERTHALL.value)
    reverb_off = REVERB_PROPERTIES(*REVERB_PRESET.OFF.value)

    # User specified latency adjusted for driver update granularity
    adjusted_latency = desired_latency
    # Latency measured once playback begins (smoothened for jitter)
    actual_latency = desired_latency

    last_record_pos = 0
    last_play_pos = 0
    samples_recorded = 0
    samples_played = 0
    min_record_delta = sound_len
    channel = None
    while True:
        stdscr.move(7, 0)
        stdscr.clrtoeol()
        stdscr.addstr(
            f"Press SPACE to {'disable' if dsp_enabled else 'enable'} DSP effect\n"
            "Press q to quit"
        )

        # Determine how much has been recorded since we last checked
        record_pos = 0
        try:
            record_pos = system.get_record_position(RECORD_DEVICE_INDEX)
        except FmodError as fmoderror:
            if fmoderror.result != RESULT.RECORD_DISCONNECTED:
                raise fmoderror

        record_delta = (
            record_pos - last_record_pos
            if record_pos >= last_record_pos
            else record_pos + sound_len - last_record_pos
        )
        last_record_pos = record_pos
        samples_recorded += record_delta

        if record_delta and record_delta < min_record_delta:
            # Smallest driver granularity seen so far
            min_record_delta = record_delta
            # Adjust our latency if driver granularity is high
            adjusted_latency = max(desired_latency, record_delta)

        # Delay playback until our desired latency is reached
        if not channel and samples_recorded >= adjusted_latency:
            channel = sound.play()

        if channel:
            # Stop playback if recording stops
            if not system.is_recording(RECORD_DEVICE_INDEX):
                channel.paused = True

            # Determine how much has been played since we last checked
            play_pos = channel.get_position(TIMEUNIT.PCM)
            play_delta = (
                play_pos - last_play_pos
                if play_pos >= last_play_pos
                else play_pos + sound_len - last_play_pos
            )
            last_play_pos = play_pos
            samples_played += play_delta

            # Compensate for any drift
            latency = samples_recorded - samples_played
            actual_latency = 0.97 * actual_latency + 0.03 * latency

            playbackrate = record_driver_info.system_rate
            if actual_latency < adjusted_latency - drift_threshold:
                # Play position is catching up to the record position, slow
                # playback down by 2%
                playbackrate -= playbackrate / 50
            elif actual_latency > adjusted_latency + drift_threshold:
                # Play position is falling behind the record position, speed
                # playback up by 2%
                playbackrate += playbackrate / 50
            channel.frequency = playbackrate

        adjusted_latency_ms = int(
            adjusted_latency * 1000 / record_driver_info.system_rate
        )
        actual_latency_ms = int(actual_latency * 1000 / record_driver_info.system_rate)
        samples_recorded_s = int(samples_recorded / record_driver_info.system_rate)
        samples_played_s = int(samples_played / record_driver_info.system_rate)

        stdscr.move(10, 0)
        stdscr.clrtobot()
        stdscr.addstr(
            f"Adjusted latency: {adjusted_latency:4.0f} ({adjusted_latency_ms}ms)\n"
            f"Actual latency:   {actual_latency:4.0f} ({actual_latency_ms}ms)\n"
            "\n"
            f"Recorded: {samples_recorded:5d} ({samples_recorded_s}s)\n"
            f"Played: {samples_played:5d} ({samples_played_s}s)"
        )

        # Listen to the user
        try:
            keypress = stdscr.getkey()
            if keypress == " ":
                # Add a DSP effect -- just for fun
                dsp_enabled = not dsp_enabled
                system.set_reverb_properties(
                    0, reverb_on if dsp_enabled else reverb_off
                )
            elif keypress == "q":
                break
        except curses.error as cerr:
            if cerr.args[0] != "no input":
                raise cerr

        system.update()
        time.sleep(10 / 1000)


curses.wrapper(main)

# Shut down
sound.release()
system.release()
