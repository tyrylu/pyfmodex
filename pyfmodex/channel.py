from .fmodobject import *
from .fmodobject import _dll
from .structures import VECTOR, REVERB_CHANNELPROPERTIES
from .constants import FMOD_DELAYTYPE_END_MS
from .globalvars import get_class
from .callbackprototypes import CHANNEL_CALLBACK

class ConeSettings(object):
    def __init__(self, sptr):
        self._sptr = sptr
        self._in = c_float()
        self._out = c_float()
        self._outvol = c_float()
        ckresult(_dll.FMOD_Channel_Get3DConeSettings(self._sptr, byref(self._in), byref(self._out), byref(self._outvol)))

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
        ckresult(_dll.FMOD_Channel_Set3DConeSettings(self._sptr, self._in, self._out, self._outvol))

class Channel(FmodObject):
    def add_dsp(self, d):
        check_type(d, get_class("DSP"))
        c_ptr = c_void_p()
        ckresult(_dll.FMOD_Channel_AddDSP(self._ptr, d._ptr, byref(c_ptr)))
        return get_class("DSP_Connection")(c_ptr)
    @property
    def _threed_attrs(self):
        pos = VECTOR()
        vel = VECTOR()
        ckresult(_dll.FMOD_Channel_Get3DAttributes(self._ptr, byref(pos), byref(vel)))
        return [pos.to_list(), vel.to_list()]
    @_threed_attrs.setter
    def _threed_attrs(self, attrs):
        pos = VECTOR.from_list(attrs[0])
        vel = VECTOR.from_list(attrs[1])
        ckresult(_dll.FMOD_Channel_Set3DAttributes(self._ptr, byref(pos), byref(vel)))

    @property
    def position(self):
        return self._threed_attrs[0]
    @position.setter
    def position(self, pos):
        self._threed_attrs = (pos, self._threed_attrs[1])

    @property
    def velocity(self):
        return self._threed_attrs[1]
    @velocity.setter
    def velocity(self, vel):
        self._threed_attrs = (self._threed_attrs[0], vel)

    @property
    def cone_orientation(self):
        ori = VECTOR()
        ckresult(_dll.FMOD_Channel_Get3DConeOrientation(self._ptr, byref(ori)))
        return ori.to_list()
    @cone_orientation.setter
    def cone_orientation(self, ori):
        vec = VECTOR.from_list(ori)
        ckresult(_dll.FMOD_Channel_Set3DConeOrientation(self._ptr, vec))

    @property
    def cone_settings(self):
        return ConeSettings(self._ptr)
    
    @property
    def doppler_level(self):
        level = c_float()
        ckresult(_dll.FMOD_Channel_Get3DDopplerLevel(self._ptr, byref(level)))
        return level.value
    @doppler_level.setter
    def doppler_level(self, l):
        ckresult(_dll.FMOD_Channel_Set3DDopplerLevel(self._ptr, c_float(l)))

    @property
    def _min_max_distance(self):
        min = c_float()
        max = c_float()
        ckresult(_dll.FMOD_Channel_Get3DMinMaxDistance(self._ptr, byref(min), byref(max)))
        return (min.value, max.value)
    @_min_max_distance.setter
    def _min_max_distance(self, dists):
        ckresult(_dll.FMOD_Channel_Set3DMinMaxDistance(self._ptr, c_float(dists[0]), c_float(dists[1])))

    @property
    def min_distance(self):
        return self._min_max_distance[0]
    @min_distance.setter
    def min_distance(self, dist):
        self._min_max_distance = (dist, self._min_max_distance[1])

    @property
    def max_distance(self):
        return self._min_max_distance[1]
    @max_distance.setter
    def max_distance(self, dist):
        self._min_max_distance = (self._min_max_distance[0], dist)

    @property
    def _occlusion(self):
        direct = c_float()
        reverb = c_float()
        ckresult(_dll.FMOD_Channel_Get3DOcclusion(self._ptr, byref(direct), byref(reverb)))
        return (direct.value, reverb.value)
    @_occlusion.setter
    def _occlusion(self, occs):
        ckresult(_dll.FMOD_Channel_Set3DOcclusion(self._ptr, c_float(occs[0]), c_float(occs[1])))

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

    @property
    def pan_level(self):
        l = c_float()
        ckresult(_dll.FMOD_Channel_Get3DanLevel(self._ptr, byref(l)))
        return l.value
    @pan_level.setter
    def pan_level(self, l):
        ckresult(_dll.FMOD_Channel_Set3DPanLevel(self._ptr, c_float(l)))
    
    @property
    def threed_spread(self):
        a = c_float()
        ckresult(_dll.FMOD_Channel_Get3DSpread(self._ptr, byref(a)))
        return a.value
    @threed_spread.setter
    def threed_spread(self, a):
        ckresult(_dll.FMOD_Channel_Set3DSpread(self._ptr, c_float(a)))

    @property
    def audibility(self):
        aud = c_float()
        ckresult(_dll.FMOD_Channel_GetAudibility(self._ptr, byref(aud)))
        return aud.value

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
    def dsp_head(self):
        dsp_ptr = c_void_p()
        ckresult(_dll.FMOD_Channel_GetDSPHead(self._ptr, byref(dsp_ptr)))
        return get_class("DSP")(dsp_ptr)
    def get_delay(self, type):
        lo = c_uint()
        hi = c_uint()
        ckresult(_dll.FMOD_ChannelGetDelay(self._ptr, type, byref(hi), byref(lo)))
        return MAKELONG(lo.value, hi.value)

    def set_delay(self, type, val):
        if type == FMOD_DELAYTYPE_END_MS:
            hi = val
            lo = None
        else:
            hi = HIWORD(val)
            lo = LOWORD(val)
        ckresult(_dll.FMOD_Channel_SetDelay(self._ptr, type, hi, lo))

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
        idx = c_float()
        ckresult(_dll.FMOD_Channel_GetIndex(self._ptr, byref(idx)))
        return idx.value

    @property
    def loop_count(self):
        c = c_int()
        ckresult(_dll.FMOD_Channel_GetLoopCount(self._ptr, byref(c)))
        return c.value
    @loop_count.setter
    def loop_count(self, count):
        ckresult(_dll.FMOD_Channel_SetLoopCount(self._ptr, c_int(count)))

    @property
    def loop_points(self):
        "Returns tuple of two tuples ((start, startunit),(end, endunit))"""
        start = c_uint()
        startunit = c_int()    
        end = c_uint()
        endunit = c_int()
        ckresult(_dll.FMOD_Channel_GetLoopPoints(self._ptr, byref(start), byref(startunit), byref(end), byref(endunit)))
        return ((start.value, startunit.value), (end.value, endunit.value))
    @loop_points.setter
    def loop_points(self, p):
        """Same format as returned from this property is required to successfully call this setter."""
        ckresult(_dll.FMOD_Channel_SetLoopPoints(self._ptr, c_uint(p[0][0]), p[0][1], c_uint(p[1][0]), p[1][1]))

    @property
    def low_pass_gain(self):
        gain = c_float()
        ckresult(_dll.FMOD_Channel_GetLowPassGain(self._ptr, byref(gain)))
        return gain.value
    @low_pass_gain.setter
    def low_pass_gain(self, gain):
        ckresult(_dll.FFMOD_Channel_SetLowPassGain(self._ptr, c_float(gain)))

    @property
    def mode(self):
        mode = c_int()
        ckresult(_dll.FMOD_Channel_GetMode(self._ptr, byref(mode)))
        return mode.value
    @mode.setter
    def mode(self, m):
        ckresult(_dll.FMOD_Channel_SetMode(self._ptr, m))

    @property
    def mute(self):
        mute = c_bool()
        ckresult(_dll.FMOD_Channel_GetMute(self._ptr, byref(mute)))
        return mute.value
    @mute.setter
    def mute(self, m):
        ckresult(_dll.FMOD_Channel_SetMute(self._ptr, m))

    @property
    def pan(self):
        pan = c_float()
        ckresult(_dll.FMOD_Channel_GetPan(self._ptr, byref(pan)))
        return pan.value
    @pan.setter
    def pan(self, pan):
        ckresult(_dll.FMOD_Channel_SetPan(self._ptr, c_float(pan)))

    @property
    def paused(self):
        paused = c_bool()
        ckresult(_dll.FMOD_Channel_GetPaused(self._ptr, byref(paused)))
        return paused.value
    @paused.setter
    def paused(self, p):
        ckresult(_dll.FMOD_Channel_SetPaused(self._ptr, p))

    def get_position(self, unit):
        pos = c_uint()
        ckresult(_dll.FMOD_Channel_GetPosition(self._ptr, byref(pos), unit))
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
    def reverb_properties(self):
        props = REVERB_CHANNELPROPERTIES()
        ckresult(_dll.FMOD_Channel_GetReverbProperties(self._ptr, byref(props)))
        return props
    @reverb_properties.setter
    def reverb_properties(self, props):
        check_type(props, REVERB_CHANNELPROPERTIES)
        ckresult(_dll.FMOD_Channel_SetReverbProperties(self._ptr, byref(props)))

    def get_spectrum(self, numvalues, channeloffset, window):
        arr = c_float * numvalues
        arri = arr()
        ckresult(_dll.FMOD_Channel_GetSpectrum(self._ptr, byref(arri), numvalues, channeloffset, window))
        return list(arri)

    @property
    def system_object(self):
        sptr = c_void_p()
        ckresult(_dll.FMOD_Channel_GetSystemObject(self._ptr, byref(sptr)))
        return get_class("System")(sptr, False)

    @property
    def volume(self):
        vol = c_float()
        ckresult(_dll.FMOD_Channel_GetVolume(self._ptr, byref(vol)))
        return vol.value
    @volume.setter
    def volume(self, vol):
        ckresult(_dll.FMOD_Channel_SetVolume(self._ptr, c_float(vol)))

    def get_wave_data(self, numvalues, channeloffset):
        arr = c_float * numvalues
        arri = arr()
        ckresult(_dll.FMOD_Channel_GetWaveData(self._ptr, byref(arri), numvalues, channeloffset))
        return list(arri)

    @property
    def is_playing(self):
        pl = c_bool()
        ckresult(_dll.FMOD_Channel_IsPlaying(self._ptr, byref(pl)))
        return pl.value

    @property
    def is_virtual(self):
        vi = c_bool()
        ckresult(_dll.FMOD_Channel_IsVirtual(self._ptr, byref(vi)))
        return vi.value

    def set_callback(self, cb):
        cbi = CHANNEL_CALLBACK(cb)
        ckresult(_dll.FMOD_Channel_SetCallback(self._ptr, cbi))

    def stop(self):
        ckresult(_dll.FMOD_Channel_Stop(self._ptr))

    @property
    def threed_distance_filter(self):
        cu = c_bool()
        cl = c_float()
        ce = c_float()
        self._call_fmod("FMOD_CHANNEL_Get3DDistanceFilter", byref(cu), byref(cl), byref(cu))
        return so(custom=cu.value, custom_level=cl.value, center_frequency=ce.value)	
    @threed_distance_filter.setter
    def threed_distance_filter(self, cfg):
        "Sets the distance filter. Cfg must be an structobject, or anythink with attributes custom, custom_level and center_frequency."""
        self._call_fmod("FMOD_CHANNEL_Set3DDistanceFilter", cfg.custom, cfg.custom_level, cfg.center_frequency)
