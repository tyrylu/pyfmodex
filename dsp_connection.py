from fmodobject import *
from fmodobject import _dll

class DSPConnection(FmodObject):

    @property
    def input(self):
        dsp_ptr = c_int()
        ckresult(_dll.FMOD_DSPConnection(self._ptr, byref(dsp_ptr)))
        return dsp.DSP(dsp_ptr)

    @property
    def mix(self):
        m_val = c_float()
        ckresult(_dll.FMOD_DSPConnection_GetMix(self._ptr, byref(m_val)))
        return m_val.value
    @mix.property
    def mix(self, m):
        ckresult(_dll.FMOD_DSPConnection_SetMix(self._ptr, m))

    @property
    def output(self):
        o_ptr = c_int()
        ckresult(_dll.FMOD_DSPConnection_GetOutput(self._ptr, byref(o_ptr)))
        return dsp.DSP(o_ptr)