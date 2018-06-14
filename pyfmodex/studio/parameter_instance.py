from ctypes import c_float, byref
from .studio_object import StudioObject
from .structures import PARAMETER_DESCRIPTION

class ParameterInstance(StudioObject):
    function_prefix = "FMOD_Studio_ParameterInstance"

    @property
    def value(self):
        val = c_float()
        self._call("GetValue", byref(val))
        return val.value

    @value.setter
    def value(self, val):
        self._call("SetValue", val)

    @property
    def description(self):
        desc = PARAMETER_DESCRIPTION()
        self._call("GetDescription", byref(desc))
        return desc