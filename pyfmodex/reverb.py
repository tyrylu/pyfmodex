from ctypes import *
from .fmodobject import FmodObject
from .structures import VECTOR, REVERB_PROPERTIES
from .utils import check_type

class Reverb3D(FmodObject):

    @property
    def _threed_attrs(self):
        pos = VECTOR()
        mindist = c_float()
        maxdist = c_float()
        self._call_fmod("FMOD_Reverb3D_Get3DAttributes", byref(pos), byref(mindist), byref(maxdist))
        return [pos.to_list(), mindist.value, maxdist.value]
    @_threed_attrs.setter
    def _threed_attrs(self, attrs):
        self._call_fmod("FMOD_Reverb3D_Set3DAttributes", VECTOR.from_list(attrs[0]), c_float(attrs[1]), c_float(attrs[2]))

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
        self._call_fmod("FMOD_Reverb3D_GetActive", byref(active))
        return active.value
    @active.setter
    def active(self, a):
        self._call_fmod("FMOD_Reverb3D_SetActive", a)

    @property
    def properties(self):
        props = REVERB_PROPERTIES()
        self._call_fmod("FMOD_Reverb3D_GetProperties", byref(props))
        return props
    @properties.setter
    def properties(self, props):
        check_type(props, REVERB_PROPERTIES)
        self._call_fmod("FMOD_Reverb3D_SetProperties", props)

    def release(self):
        self._call_fmod("FMOD_Reverb3D_Release")