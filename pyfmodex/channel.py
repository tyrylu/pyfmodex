from ctypes import *
from .fmodobject import _dll
from .structures import VECTOR, REVERB_PROPERTIES
from .globalvars import get_class
from .callback_prototypes import CHANNELCONTROL_CALLBACK
from .utils import ckresult, check_type
from .structobject import Structobject as so
from .flags import MODE

from .channel_control import ChannelControl

class Channel(ChannelControl):

    @property
    def pan_level(self):
        l = c_float()
        ckresult(_dll.FMOD_Channel_Get3DPanLevel(self._ptr, byref(l)))
        return l.value
    @pan_level.setter
    def pan_level(self, l):
        ckresult(_dll.FMOD_Channel_Set3DPanLevel(self._ptr, c_float(l)))
    
    
    @property
    def channel_group(self):
        grp_ptr = c_void_p()
        ckresult(_dll.FMOD_Channel_GetChannelGroup(self._ptr, byref(grp_ptr)))
        return get_class("ChannelGroup")(grp_ptr)
    @channel_group.setter
    def channel_group(self, group):
        check_type(group, get_class("ChannelGroup"))
        ckresult(_dll.FMOD_Channel_SetChannelGroup(self._ptr, group._ptr))

    @property
    def current_sound(self):
        snd_ptr = c_void_p()
        ckresult(_dll.FMOD_Channel_GetCurrentSound(self._ptr, byref(snd_ptr)))
        return get_class("Sound")(snd_ptr)
    
    @property
    def frequency(self):
        freq = c_float()
        ckresult(_dll.FMOD_Channel_GetFrequency(self._ptr, byref(freq)))
        return freq.value
    @frequency.setter
    def frequency(self, freq):
        ckresult(_dll.FMOD_Channel_SetFrequency(self._ptr, c_float(freq)))

    @property
    def index(self):
        idx = c_int()
        self._call_fmod("FMOD_Channel_GetIndex", byref(idx))
        return idx.value

    @property
    def loop_count(self):
        c = c_int()
        ckresult(_dll.FMOD_Channel_GetLoopCount(self._ptr, byref(c)))
        return c.value
    @loop_count.setter
    def loop_count(self, count):
        ckresult(_dll.FMOD_Channel_SetLoopCount(self._ptr, c_int(count)))

    def get_loop_points(self, startunit, endunit):
        "Returns tuple(start, end)"""
        start = c_uint()
        end = c_uint()
        ckresult(_dll.FMOD_Channel_GetLoopPoints(self._ptr, byref(start), int(startunit), byref(end), int(endunit)))
        return start.value, end.value

    def set_loop_points(self, start, startunit, end, endunit):
        ckresult(_dll.FMOD_Channel_SetLoopPoints(self._ptr, c_uint(start), int(startunit), c_uint(end), int(endunit)))

    def get_position(self, unit):
        pos = c_uint()
        ckresult(_dll.FMOD_Channel_GetPosition(self._ptr, byref(pos), int(unit)))
        return pos.value

    def set_position(self, pos, unit):
        ckresult(_dll.FMOD_Channel_SetPosition(self._ptr, pos, unit))

    @property
    def priority(self):
        pri = c_int()
        ckresult(_dll.FMOD_Channel_GetPriority(self._ptr, byref(pri)))
        return pri.value
    @priority.setter
    def priority(self, pri):
        ckresult(_dll.FMOD_Channel_SetPriority(self._ptr, pri))    

    @property
    def is_virtual(self):
        vi = c_bool()
        ckresult(_dll.FMOD_Channel_IsVirtual(self._ptr, byref(vi)))
        return vi.value
