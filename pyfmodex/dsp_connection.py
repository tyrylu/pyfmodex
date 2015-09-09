from .fmodobject import *
from .fmodobject import _dll
from .globalvars import get_class

class DSPConnection(FmodObject):

    @property
    def input(self):
        dsp_ptr = c_void_p()
        ckresult(_dll.FMOD_DSPConnection(self._ptr, byref(dsp_ptr)))
        return get_class("DSP")(dsp_ptr)

    @property
    def mix(self):
        m_val = c_float()
        ckresult(_dll.FMOD_DSPConnection_GetMix(self._ptr, byref(m_val)))
        return m_val.value
    @mix.setter
    def mix(self, m):
        ckresult(_dll.FMOD_DSPConnection_SetMix(self._ptr, m))

    @property
    def output(self):
        o_ptr = c_void_p()
        ckresult(_dll.FMOD_DSPConnection_GetOutput(self._ptr, byref(o_ptr)))
        return get_class("DSP")(o_ptr)