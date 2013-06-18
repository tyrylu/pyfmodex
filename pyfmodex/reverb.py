from .fmodobject import *
from .globalvars import dll as _dll
from .structures import VECTOR, REVERBPROPERTIES

class Reverb(FmodObject):

    @property
    def _threed_attrs(self):
        pos = VECTOR()
        mindist = c_float()
        maxdist = c_float()
        self._call_fmod("FMOD_Reverb_Get3DAttributes", byref(pos), byref(mindist), byref(maxdist))
        return [pos.to_list(), mindist.value, maxdist.value]
    @_threed_attrs.setter
    def _threed_attrs(self, attrs):
        self._call_fmod("FMOD_Reverb_Set3DAttributes", *attrs)

    @property
    def position(self):
        return self._threed_attrs[0]
    @position.setter
    def position(self, pos):
        attrs = self._threed_attrs
        attrs[0] = pos
        self._threed_attrs = attrs

    @property
    def min_distance(self):
        return self._threed_attrs[1]
    @min_distance.setter
    def min_distance(self, mindist):
        attrs = self._threed_attrs
        attrs[1] = mindist
        self._threed_attrs = attrs

    @property
    def max_distance(self):
        return self._threed_attrs[2]
    @max_distance.setter
    def max_distance(self, maxdist):
        attrs = self._threed_attrs
        attrs[2] = maxdist
        self._threed_attrs = attrs

    @property
    def active(self):
        active = c_bool()
        self._call_fmod("FMOD_Reverb_GetActive", byref(active))
        return active.value
    @active.setter
    def active(self, a):
        self._call_fmod("FMOD_Reverb_SetActive", a)

    @property
    def properties(self):
        props = REVERBPROPERTIES()
        self._call_fmod("FMOD_Reverb_GetProperties", byref(props))
        return props
    @properties.setter
    def properties(self):
        check_type(props, REVERBPROPERTIES)
        self._call_fmod("FMOD_Reverb_SetProperties", props)

    def release(self):
        self._call_fmod("FMOD_Reverb_Release")