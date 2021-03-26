"""Playback state of various objects."""

from enum import Enum


class PLAYBACK_STATE(Enum):  # pylint: disable=invalid-name
    """Playback state of various objects.

    PLAYING: Playing
    SUSTAINING: The timeline cursor is paused on a sustain point
    STOPPED: Stopped
    STARTING: Preparing to start
    STOPPING: Preparing to stop
    """

    PLAYING = 0
    SUSTAINING = 1
    STOPPED = 2
    STARTING = 3
    STOPPING = 4
