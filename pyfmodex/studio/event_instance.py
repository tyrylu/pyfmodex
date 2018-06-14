from ctypes import c_bool, c_float, c_int, c_void_p, byref
from .studio_object import StudioObject
from .enums import PLAYBACK_STATE
from .parameter_instance import ParameterInstance
from ..utils import prepare_str


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

    def get_parameter(self, name):
        ptr = c_void_p()
        self._call("GetParameter", prepare_str(name), byref(ptr))
        return ParameterInstance(ptr)

    def get_parameter_by_index(self, index):
        ptr = c_void_p()
        self._call("GetParameterByIndex", index, byref(ptr))
        return ParameterInstance(ptr)

    def get_parameter_value(self, name):
        val = c_float()
        actual = c_float()
        self._call("GetParameterValue", prepare_str(name), byref(val), byref(actual))
        return (val.value, actual.value)

    def get_parameter_value_by_index(self, index):
        val = c_float()
        actual = c_float()
        self._call("GetParameterValueByIndex", index, byref(val), byref(actual))
        return (val.value, actual.value)

    def set_parameter_value(self, name, value):
        self._call("SetParameterValue", prepare_str(name), value)

    def set_parameter_value_by_index(self, index, value):
        self._call("SetParameterValueByIndex", index, value)

    def set_parameter_values_by_indices(self, indices, values):
        if len(indices) != len(values):
            raise ValueError("Indices and values must have same length.")
        self._call("SetParameterValuesByIndices", indices, values, len(indices))
