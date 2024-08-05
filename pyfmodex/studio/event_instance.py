"""An instance of an FMOD Studio Event."""

from ctypes import byref, c_bool, c_float, c_int, c_void_p

from ..channel_group import ChannelGroup
from ..structures import THREED_ATTRIBUTES
from ..structures import VECTOR
from ..utils import prepare_str
from .enums import PLAYBACK_STATE
from .studio_object import StudioObject


class EventInstance(StudioObject):
    """An instance of an FMOD Studio Event."""

    function_prefix = "FMOD_Studio_EventInstance"

    def __init__(self, ptr):
        self._pos = VECTOR()
        self._vel = VECTOR()
        self._fwd = VECTOR()
        self._up = VECTOR()
        super().__init__(ptr)

    def start(self):
        """Starts playback.

        If the instance was already playing then calling this function will
        restart the event.
        """
        self._call("Start")

    def stop(self):
        """Stops playback."""
        self._call("Stop")

    @property
    def volume(self):
        """The volume level.

         - 0: silent
         - 1: full
         - Negative level: inverts the signal
         - Value larger than 1: amplifies the signal

        Setting volume at a level higher than 1 can lead to
        distortion/clipping.

        :type: float
        """
        vol = c_float()
        self._call("GetVolume", byref(vol))
        return vol.value

    @volume.setter
    def volume(self, vol):
        self._call("SetVolume", c_float(vol))

    @property
    def pitch(self):
        """Pitch multiplier.

        :type: float
        """
        pitch = c_float()
        self._call("GetPitch", byref(pitch))
        return pitch.value

    @pitch.setter
    def pitch(self, pitch):
        self._call("SetPitch", c_float(pitch))

    @property
    def paused(self):
        """The pause state.

        True if the event instance is paused.
        """
        paused = c_bool()
        self._call("GetPaused", byref(paused))
        return paused.value

    @paused.setter
    def paused(self, val):
        """Set the pause state.

        :param bool val: The desired pause state. True = paused, False =
            unpaused.
        """
        self._call("SetPaused", c_bool(val))

    @property
    def playback_state(self):
        """The playback state.

        If the instance is invalid, then the state will be STOPPED.
        """
        state = c_int()
        self._call("GetPlaybackState", byref(state))
        return PLAYBACK_STATE(state.value)

    @property
    def cpu_usage(self):
        """Retrieves the event CPU usage data."""
        usage = c_int()
        self._call('Release', byref(usage))
        return usage.value

    @property
    def timeline_position(self):
        """Timeline cursor position

        :type: int
        """
        pos = c_int()
        self._call("GetTimelinePosition", byref(pos))
        return pos.value

    @timeline_position.setter
    def timeline_position(self, pos):
        self._call("SetTimelinePosition", c_int(pos))

    @property
    def position(self):
        """Position in 3D space used for panning and attenuation.

        :type: list of three coordinate floats
        """
        return self._pos.to_list()

    @position.setter
    def position(self, poslist):
        self._pos = VECTOR.from_list(poslist)
        self._commit_3d()

    @property
    def velocity(self):
        """Velocity in 3D space used for doppler.

        :type: list of three coordinate floats
        """
        return self._vel.to_list()

    @velocity.setter
    def velocity(self, vellist):
        self._vel = VECTOR.from_list(vellist)
        self._commit_3d()

    @property
    def forward(self):
        """Forwards orientation.

        :type: list of three coordinate floats
        """
        return self._fwd.to_list()

    @forward.setter
    def forward(self, fwdlist):
        self._fwd = VECTOR.from_list(fwdlist)
        self._commit_3d()

    @property
    def up(self):
        """Upwards orientation.

        :type: list of three coordinate floats
        """
        return self._up.to_list()

    @up.setter
    def up(self, uplist):
        self._up = VECTOR.from_list(uplist)
        self._commit_3d()

    def _commit_3d(self):
        self._call(
            "Set3DAttributes",
            byref(THREED_ATTRIBUTES(
                self._pos,
                self._vel,
                self._fwd,
                self._up
            ))
        )

    def set_volume(self, vol):
        """Sets the volume level.

        :param vol: Volume multiplier.
        """
        self.volume = vol

    def get_volume(self):
        """Retrieves the volume level."""
        return self.volume

    def set_pitch(self, vol):
        """Sets the pitch level.

        :param vol: Pitch multiplier.
        """
        self.pitch = vol

    def get_pitch(self):
        """Retrieves the pitch level."""
        return self.pitch

    def set_timeline_position(self, pos: int):
        """Sets the timeline cursor position.

        :param pos: Timeline position.
        """
        self.timeline_position = pos

    def get_timeline_position(self):
        """Retrieves the timeline cursor position."""
        return self.timeline_position

    def get_parameter_by_name(self, name):
        """A parameter value.

        :param str name: Parameter name (case-insensitive)."""
        val = c_float()
        actual = c_float()
        self._call("GetParameterByName", prepare_str(name), byref(val), byref(actual))
        return (val.value, actual.value)

    def set_parameter_by_name(self, name, value, ignoreseekspeed=False):
        """Set a parameter value by name.

        :param str name: Parameter name (case-insensitive).
        :param float value: Value for given name.
        :param bool ignoreseekspeed: Specifies whether to ignore the
            parameter's seek speed and set the value immediately.
        """
        self._call(
            "SetParameterByName", prepare_str(name), c_float(value), ignoreseekspeed
        )

    def get_3d_attributes(self) -> list[list[float]]:
        """Get the 3D attributes of this EventInstance.

        :returns: list of [`position`, `velocity`, `forward`, `up`]
        """
        _attrs = THREED_ATTRIBUTES(VECTOR(), VECTOR(), VECTOR(), VECTOR())
        self._call(
            "Get3DAttributes",
            byref(_attrs)
        )
        return [
            _attrs.position.to_list(),
            _attrs.velocity.to_list(),
            _attrs.forward.to_list(),
            _attrs.up.to_list()
        ]

    def set_3d_attributes(
            self,
            position: list = [0, 0, 0],
            velocity: list = [0, 0, 0],
            forward: list = [0, 1, 0],
            up: list = [0, 0, 1]
        ):
        """Set the 3D attributes for this EventInstance.

        :param list position: Position used for panning and attenuation (camera relative).
        :param list velocity: Velocity in world space used for doppler.
        :param list forward: Forwards orientation, must be of unit length (1.0)
            and perpendicular to `up`.
        :param list up: Upwards orientation, must be of unit length (1.0) and
            perpendicular to `forward`.
        """
        self._pos = VECTOR.from_list(position)
        self._vel = VECTOR.from_list(velocity)
        self._fwd = VECTOR.from_list(forward)
        self._up = VECTOR.from_list(up)
        self._commit_3d()

    def get_cpu_usage(self):
        '''Retrieves the event CPU usage data.'''
        return self.cpu_usage

    def release(self):
        self._call('Release')

    @property
    def channel_group(self):
        """The core channel group corresponding to the master track.

        Until the event instance has been fully created calling this property
        will raise an :py:exc:`~pyfmodex.exceptions.FmodError` with code
        :py:attr:`~pyfmodex.enums.RESULT.STUDIO_NOT_LOADED`.
        """
        ptr = c_void_p()
        self._call("GetChannelGroup", byref(ptr))
        return ChannelGroup(ptr)

    def set_reverb_level(self, index, level):
        """Sets the core reverb send level.

        :param index: Core reverb instance index.
        :param level: Reverb send level.
        """
        self._call('SetReverbLevel', c_int(index), c_float(level))

    def get_reverb_level(self, index):
        """Retrieves the core reverb send level.

        :param index: Core reverb instance index.
        """
        level = c_float()
        self._call('GetReverbLevel', c_int(index), byref(level))
        return level.value

    @property
    def is_virtual(self):
        """Retrieves the virtualization state.

        True if the event instance has been virtualized due to the polyphony limit being exceeded.
        """
        virtual = c_bool()
        self._call('IsVirtual', byref(virtual))
        return virtual.value
