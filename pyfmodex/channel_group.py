from .fmodobject import *
from .globalvars import dll as _dll
from .globalvars import get_class

class ChannelGroup(FmodObject):

    def add_dsp(self, dsp):
        check_type(dsp, get_class("DSP"))
        c_ptr = c_void_p()
        self._call_fmod("FMOD_ChannelGroup_AddDSP", d._ptr, byref(c_ptr))
        return get_class("DSPConnection")(c_ptr)

    def add_group(self, group):
        check_type(group, ChannelGroup)
        self._call_fmod("FMOD_ChannelGroup_AddGroup", group._ptr)

    @property
    def _occlusion(self):
        direct = c_float()
        reverb = c_float()
        self._call_fmod("FMOD_ChannelGroup_Get3DOcclusion", byref(direct), byref(reverb))
        return (direct.value, reverb.value)
    @_occlusion.setter
    def _occlusion(self, occs):
        self._call_fmod("FMOD_ChannelGroup_Set3DOcclusion", c_float(occs[0]), c_float(occs[1]))

    @property
    def direct_occlusion(self):
        return self._occlusion[0]
    @direct_occlusion.setter
    def direct_occlusion(self, occ):
        self._occlusion = (occ, self._occlusion[1])

    @property
    def reverb_occlusion(self):
        return self._occlusion[1]
    @reverb_occlusion.setter
    def reverb_occlusion(self, occ):
        self._occlusion = (self._occlusion[0], occ)

    def get_channel(self, idx):
        c_ptr = c_void_p()
        self._call_fmod("FMOD_ChannelGroup_GetChannel", idx, byref(c_ptr))
        return channel.Channel(c_ptr)

    @property
    def dsp_head(self):
        dsp_ptr = c_void_p()
        self._call_fmod("FMOD_ChannelGroup_GetDSPHead", byref(dsp_ptr))
        return get_class("DSP")(dsp_ptr)

    def get_group(self, idx):
        grp_ptr = c_void_p()
        self._call_fmod("FMOD_ChannelGroup_GetGroup", idx)
        return ChannelGroup(grp_ptr)

    @property
    def mute(self):
        mute = c_bool()
        self._call_fmod("FMOD_ChannelGroup_GetMute", byref(mute))
        return mute.value
    @mute.setter
    def mute(self, m):
        self._call_fmod("FMOD_Channel_SetMute", m)

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
        return ChannelGroup(grp_ptr)

    @property
    def paused(self):
        paused = c_bool()
        self._call_fmod("FMOD_ChannelGroup_GetPaused", byref(paused))
        return paused.value
    @paused.setter
    def paused(self, p):
        self._call_fmod("FMOD_ChannelGroup_SetPaused", p)

    @property
    def pitch(self):
        pitch = c_float()
        self._call_fmod("FMOD_ChannelGroup_GetPitch", byref(pitch))
        return pitch.value
    @property
    def pitch(self, p):
        self._call_fmod("FMOD_ChannelGroup_SetPitch", p)

    def get_spectrum(self, numvalues, channeloffset, window):
        arr = c_float * numvalues
        arri = arr()
        self._call_fmod("FMOD_ChannelGroup_GetSpectrum", byref(arri), numvalues,  channeloffset, window)
        return list(arri)

    @property
    def system_object(self):
        sptr = c_void_p()
        self._call_fmod("FMOD_channelGroup_GetSystemObject", byref(sptr))
        return get_class("System")(sptr, False)

    @property
    def volume(self):
        vol = c_float()
        self._call_fmod("FMOD_ChannelGroup_GetVolume", byref(vol))
        return vol.value
    @volume.setter
    def volume(self, vol):
        self._call_fmod("FMOD_ChannelGroup_SetVolume", c_float(vol))

    def get_wave_data(self, numvalues, channeloffset):
        arr = c_float * numvalues
        arri = arr()
        self._call_fmod("FMOD_ChannelGroup_GetWaveData", byref(arri), numvalues,  channeloffset)
        return list(arri)

    def override_3d_attributes(self, pos=0, vel=0):
        self._call_fmod("FMOD_ChannelGroup_Override3DAttributes", pos, vel)

    def override_frequency(self, freq):
        self._call_fmod("FMOD_ChannelGroup_OverrideFrequency", c_float(freq))

    def override_pan(self, pan):
        self._call_fmod("FMOD_ChannelGroup_OverridePan", c_float(pan))

    def override_reverb_properties(self, props):
        check_type(props, REVERB_CHANNELPROPERTIES)
        self._call_fmod("FMOD_ChannelGroup_OverrideReverbProperties", props)

    def override_speaker_mix(self, frontleft, frontright, center, lfe, backleft, backright, sideleft, sideright):
        self._call_fmod("FMOD_ChannelGroup_OverrideSpeakerMix", frontleft, frontright, center, lfe, backleft, backright, sideleft, sideright)

    def override_volume(self, vol):
        self._call_fmod("FMOD_ChannelGroup_OverrideVolume", c_float(vol))

    def release(self):
        self._call_fmod("FMOD_ChannelGroup_Release")
    def stop(self):
        self._call_fmod("FMOD_ChannelGroup_Stop")

    @property
    def reverb_properties(self):
        props = REVERB_CHANNELPROPERTIES()
        ckresult(_dll.FMOD_ChannelGroup_GetReverbProperties(self._ptr, byref(props)))
        return props
    @reverb_properties.setter
    def reverb_properties(self, props):
        check_type(props, REVERB_CHANNELPROPERTIES)
        ckresult(_dll.FMOD_ChannelGroup_SetReverbProperties(self._ptr, byref(props)))
