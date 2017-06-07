from ctypes import *
from .fmodobject import *
from .globalvars import dll as _dll
from .globalvars import get_class
from .channel_control import ChannelControl
from .utils import check_type


class ChannelGroup(ChannelControl):

    def add_group(self, group, propagate_dsp_clock):
        check_type(group, ChannelGroup)
        conn_ptr = c_void_p()
        self._call_fmod("FMOD_ChannelGroup_AddGroup", group._ptr, propagate_dsp_clock, byref(conn_ptr))
        return get_class("DSP_Connection")(conn_ptr)
    
    def get_channel(self, idx):
        c_ptr = c_void_p()
        self._call_fmod("FMOD_ChannelGroup_GetChannel", idx, byref(c_ptr))
        return get_class("Channel")(c_ptr)

    def get_group(self, idx):
        grp_ptr = c_void_p()
        self._call_fmod("FMOD_ChannelGroup_GetGroup", idx)
        return ChannelGroup(grp_ptr)

    @property
    def name(self):
        buf = create_string_buffer(512)
        self._call_fmod("FMOD_ChannelGroup_GetName", buf, 512)
        return buf.value

    @property
    def num_channels(self):
        num = c_int()
        self._call_fmod("FMOD_ChannelGroup_GetNumChannels", byref(num))
        return num.value

    @property
    def num_groups(self):
        num = c_int()
        self._call_fmod("FMOD_ChannelGroup_GetNumGroups", byref(num))
        return num.value

    @property
    def parent_group(self):
        grp_ptr = c_void_p()
        self._call_fmod("FMOD_ChannelGroup_GetParentGroup", byref(grp_ptr))
        return ChannelGroup(grp_ptr) if grp_ptr.value else None

    def release(self):
        self._call_fmod("FMOD_ChannelGroup_Release")

