from ctypes import *
from .fmodobject import *
from .globalvars import get_class
from .enums import DSPCONNECTION_TYPE

class DSPConnection(FmodObject):

    @property
    def input(self):
        dsp_ptr = c_void_p()
        self._call_fmod("FMOD_DSPConnection_GetInput", byref(dsp_ptr))
        return get_class("DSP")(dsp_ptr)

    @property
    def mix(self):
        m_val = c_float()
        self._call_fmod("FMOD_DSPConnection_GetMix", byref(m_val))
        return m_val.value
    @mix.setter
    def mix(self, m):
        self._call_fmod("FMOD_DSPConnection_SetMix", c_float(m))

    def get_mix_matrix(self, hop=0):
        in_channels = c_int()
        out_channels = c_int()
        self._call_fmod("FMOD_DSPConnection_GetMixMatrix", None, byref(out_channels), byref(in_channels), hop)
        matrix = (c_float * (hop or in_channels.value * out_channels.value))()
        self._call_fmod("FMOD_DSPConnection_GetMixMatrix", matrix, byref(out_channels), byref(in_channels), hop)
        return  list(matrix)

    def set_mix_matrix(self, matrix, rows, cols):
        if not matrix:
            cols = 0
            rows = 0
        raw_matrix = (c_float * (cols * rows))(*matrix)
        self._call_fmod("FMOD_DSPConnection_SetMixMatrix", raw_matrix, rows, cols, 0)

    @property
    def output(self):
        o_ptr = c_void_p()
        self._call_fmod("FMOD_DSPConnection_GetOutput", byref(o_ptr))
        return get_class("DSP")(o_ptr)
    @property
    def type(self):
        typ = c_int()
        self._call_fmod("FMOD_DSPConnection_GetType", byref(typ))
        return DSPCONNECTION_TYPE(typ.value)