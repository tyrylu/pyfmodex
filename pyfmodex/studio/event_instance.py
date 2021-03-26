from ctypes import c_bool, c_float, c_int, c_void_p, byref
from .studio_object import StudioObject
from .enums import PLAYBACK_STATE
from ..utils import prepare_str
from ..channel_group import ChannelGroup


class EventInstance(StudioObject):
    function_prefix = "FMOD_Studio_EventInstance"

    def start(self):
        self._call("Start")

    def stop(self):
        self._call("Stop")

    @property
    def paused(self):
        paused = c_bool()
        self._call("GetPaused", byref(paused))
        return paused.value

    @paused.setter
    def paused(self, val):
        self._call("SetPaused", c_bool(val))

    @property
    def playback_state(self):
        state = c_int()
        self._call("GetPlaybackState", byref(state))
        return PLAYBACK_STATE(state.value)

    def get_parameter_by_name(self, name):
        val = c_float()
        actual = c_float()
        self._call("GetParameterByName", prepare_str(name), byref(val), byref(actual))
        return (val.value, actual.value)

    def set_parameter_by_name(self, name, value, ignoreseekspeed=False):
        self._call(
            "SetParameterByName", prepare_str(name), c_float(value), ignoreseekspeed
        )

    @property
    def channel_group(self):
        ptr = c_void_p()
        self._call("GetChannelGroup", byref(ptr))
        return ChannelGroup(ptr)
