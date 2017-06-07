from ctypes import c_float, byref
from .fmodobject import _dll
from .structures import VECTOR, REVERB_PROPERTIES
from .utils import ckresult

class ConeSettings(object):
    def __init__(self, sptr, class_name):
        self._sptr = sptr
        self._in = c_float()
        self._out = c_float()
        self._outvol = c_float()
        self._get_func = "FMOD_%s_Get3DConeSettings"%class_name
        self._set_func = "FMOD_%s_Set3DConeSettings"%class_name
        ckresult(getattr(_dll, self._get_func)(self._sptr, byref(self._in), byref(self._out), byref(self._outvol)))

    @property
    def inside_angle(self):
        return self._in.value
    @inside_angle.setter
    def inside_angle(self, angle):
        self._in = c_float(angle)
        self._commit()

    @property
    def outside_angle(self):
        return self._out.value
    @outside_angle.setter
    def outside_angle(self, angle):
        self._out = c_float(angle)
        self._commit()

    @property
    def outside_volume(self):
        return self._outvol.value
    @outside_volume.setter
    def outside_volume(self, vol):
        self._outvol = c_float(vol)
        self._commit()

    def _commit(self):
        ckresult(getattr(_dll, self._set_func)(self._sptr, self._in, self._out, self._outvol))
