from ctypes import c_bool, c_int, byref
from .studio_object import StudioObject
from .enums import PLAYBACK_STATE

class EventInstance(StudioObject):
    function_prefix = "FMOD_Studio_EventInstance"
    
    def start(self):
        self._call("Start")
    @property
    def paused(self):
        paused = c_bool()
        self._call("GetPaused", byref(paused))
        return paused.value

    @property
    def playback_state(self):
        state = c_int()
        self._call("GetPlaybackState", byref(state))
        return PLAYBACK_STATE(state.value)