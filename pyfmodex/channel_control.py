from ctypes import *
from .fmodobject import FmodObject
from .cone_settings import ConeSettings
from .utils import check_type
from .globalvars import get_class
from .structures import VECTOR
from .structobject import Structobject as so
from .flags  import MODE
from .callback_prototypes import CHANNELCONTROL_CALLBACK


class ChannelControl(FmodObject):
    def _call_specific(self, specific_function_suffix, *args):
        return self._call_fmod("FMOD_%s_%s"%(self.__class__.__name__, specific_function_suffix), *args)
    
    def add_dsp(self, index, dsp):
        check_type(dsp, get_class("DSP"))
        c_ptr = c_void_p()
        self._call_specific("AddDSP", int(index), dsp._ptr, byref(c_ptr))
        return get_class("DSP_Connection")(c_ptr)
    
    def add_fade_point(self, dsp_clock, volume):
        self._call_specific("AddFadePoint", c_ulonglong(dsp_clock), c_float(volume))
    
    @property
    def _threed_attrs(self):
        pos = VECTOR()
        vel = VECTOR()
        self._call_specific("Get3DAttributes", byref(pos), byref(vel))
        return [pos.to_list(), vel.to_list()]
    @_threed_attrs.setter
    def _threed_attrs(self, attrs):
        pos = VECTOR.from_list(attrs[0])
        vel = VECTOR.from_list(attrs[1])
        self._call_specific("Set3DAttributes", byref(pos), byref(vel))

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
        self._call_specific("Get3DConeOrientation", byref(ori))
        return ori.to_list()
    @cone_orientation.setter
    def cone_orientation(self, ori):
        vec = VECTOR.from_list(ori)
        self._call_specific("Set3DConeOrientation", vec)

    @property
    def cone_settings(self):
        return ConeSettings(self._ptr, self.__class__.__name__)

    @property
    def custom_rolloff(self):
        """Returns the custom rolloff curve.
        :rtype: List of [x, y, z] lists.
        """
        num = c_int()
        self._call_specific("Get3DCustomRolloff", None, byref(num))
        curve = (VECTOR * num.value)()
        self._call_specific("Get3DCustomRolloff", byref(curve), None)
        return [p.to_list() for p in curve]
    @custom_rolloff.setter
    def custom_rolloff(self, curve):
        """Sets the custom rolloff curve.
        :param curve: The curve to set.
        :type curve: A list of something that can be treated as a list of [x, y, z] values e.g. implements indexing in some way.
        """
        native_curve = (VECTOR * len(curve))(*[VECTOR.from_list(lst) for lst in curve])
        self._call_specific("Set3DCustomRolloff", native_curve, len(native_curve))
    @property
    def threed_distance_filter(self):
        cu = c_bool()
        cl = c_float()
        ce = c_float()
        self._call_specific("Get3DDistanceFilter", byref(cu), byref(cl), byref(cu))
        return so(custom=cu.value, custom_level=cl.value, center_frequency=ce.value)	
    @threed_distance_filter.setter
    def threed_distance_filter(self, cfg):
        "Sets the distance filter. Cfg must be an structobject, or anythink with attributes custom, custom_level and center_frequency."""
        self._call_specific("Set3DDistanceFilter", cfg.custom, c_float(cfg.custom_level), c_float(cfg.center_frequency))

    @property
    def doppler_level(self):
        level = c_float()
        self._call_specific("Get3DDopplerLevel", byref(level))
        return level.value
    @doppler_level.setter
    def doppler_level(self, l):
        self._call_specific("Set3DDopplerLevel", c_float(l))

    @property
    def level(self):
        level = c_float()
        self._call_specific("Get3DLevel", byref(level))
        return level.value
    @level.setter
    def level(self, level):
        self._call_specific("Set3DLevel", c_float(level))
        
    @property
    def _min_max_distance(self):
        min = c_float()
        max = c_float()
        self._call_specific("Get3DMinMaxDistance", byref(min), byref(max))
        return (min.value, max.value)
    @_min_max_distance.setter
    def _min_max_distance(self, dists):
        self._call_specific("Set3DMinMaxDistance", c_float(dists[0]), c_float(dists[1]))

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
        self._call_specific("Get3DOcclusion", byref(direct), byref(reverb))
        return (direct.value, reverb.value)
    @_occlusion.setter
    def _occlusion(self, occs):
        self._call_specific("Set3DOcclusion", c_float(occs[0]), c_float(occs[1]))

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
    def threed_spread(self):
        spread = c_float()
        self._call_specific("Get3DSpread", byref(spread))
        return spread.value
    @threed_spread.setter
    def threed_spread(self, spread):
        self._call_specific("Set3DSpread", c_float(spread))

    @property
    def audibility(self):
        aud = c_float()
        self._call_specific("GetAudibility", byref(aud))
        return aud.value

    def get_dsp(self, index):
        dsp = c_void_p()
        self._call_specific("GetDSP", index, byref(dsp))
        return get_class("DSP")(dsp)

    @property
    def dsp_clock(self):
        clock = c_ulonglong()
        parent = c_ulonglong()
        self._call_specific("GetDSPClock", byref(clock), byref(parent))
        return so(dsp_clock=clock.value, parent_clock=parent.value)

    def get_dsp_index(self, dsp):
        index = c_int()
        self._call_specific("GetDSPIndex", dsp._ptr, byref(index))
        return index.value

    def set_dsp_index(self, dsp, index):
        self._call_specific("SetDSPIndex", dsp._ptr, index)

    @property
    def delay(self):
        dsp_start = c_ulonglong()
        dsp_end = c_ulonglong()
        stop_channels = c_bool()
        self._call_specific("GetDelay", byref(dsp_start), byref(dsp_end), byref(stop_channels))
        return so(dsp_start=dsp_start.value, dsp_end=dsp_end.value, stop_channels=stop_channels.value)
    @delay.setter
    def delay(self, delay):
        self._call_specific("SetDelay", c_ulonglong(delay.dsp_start), c_ulonglong(delay.dsp_end), delay.stop_channels)

    @property
    def fade_points(self):
        num = c_uint()
        self._call_specific("GetFadePoints", byref(num), None, None)
        clocks = (c_ulonglong * num.value)()
        volumes = (c_float * num.value)()
        self._call_specific("GetFadePoints", byref(num), clocks, volumes)
        return list(clocks), list(volumes)
    
    @property
    def low_pass_gain(self):
        gain = c_float()
        self._call_specific("GetLowPassGain", byref(gain))
        return gain.value
    @low_pass_gain.setter
    def low_pass_gain(self, gain):
        self._call_specific("SetLowPassGain", c_float(gain))

    def get_mix_matrix(self, hop=0):
        in_channels = c_int()
        out_channels = c_int()
        self._call_fmod("FMOD_Channel_GetMixMatrix", None, byref(out_channels), byref(in_channels), hop)
        matrix = (c_float * (hop or in_channels.value * out_channels.value))()
        self._call_specific("GetMixMatrix", matrix, byref(out_channels), byref(in_channels), hop)
        return  list(matrix)

    def set_mix_matrix(self, matrix, rows, cols):
        if not matrix:
            cols = 0
            rows = 0
        raw_matrix = (c_float * (cols * rows))(*matrix)
        self._call_specific("SetMixMatrix", raw_matrix, rows, cols, 0)

    @property
    def mode(self):
        mode = c_int()
        self._call_specific("GetMode", byref(mode))
        return MODE(mode.value)
    @mode.setter
    def mode(self, m):
        self._call_specific("SetMode", int(m))

    @property
    def mute(self):
        mute = c_bool()
        self._call_specific("GetMute", byref(mute))
        return mute.value
    @mute.setter
    def mute(self, m):
        self._call_specific("SetMute", m)

    @property
    def num_dsps(self):
        num = c_int()
        self._call_specific("GetNumDSPs", byref(num))
        return num.value

    @property
    def paused(self):
        paused = c_bool()
        self._call_specific("GetPaused", byref(paused))
        return paused.value
    @paused.setter
    def paused(self, p):
        self._call_specific("SetPaused", p)

    @property
    def pitch(self):
        val = c_float()
        self._call_specific("GetPitch", byref(val))
        return val.value
    @pitch.setter
    def pitch(self, val):
        self._call_specific("SetPitch", c_float(val))
        
    def get_reverb_wet(self, instance):
        wet = c_float()
        self._call_specific("GetReverbProperties", instance, byref(wet))
        return wet.value

    def set_reverb_wet(self, instance, wet):
        self._call_specific("SetReverbProperties", instance, c_float(wet))

    @property
    def system_object(self):
        sptr = c_void_p()
        self._call_specific("GetSystemObject", byref(sptr))
        return get_class("System")(sptr)

    @property
    def volume(self):
        vol = c_float()
        self._call_specific("GetVolume", byref(vol))
        return vol.value
    @volume.setter
    def volume(self, vol):
        self._call_specific("SetVolume", c_float(vol))

    @property
    def volume_ramp(self):
        ramp = c_bool()
        self._call_specific("GetVolumeRamp", byref(ramp))
        return ramp.value
    @volume_ramp.setter
    def volume_ramp(self,ramp):
        self._call_specific("SetVolumeRamp", ramp)

    @property
    def is_playing(self):
        pl = c_bool()
        self._call_specific("IsPlaying", byref(pl))
        self._call_specific("IsPlaying", byref(pl))
        return pl.value

    def remove_dsp(self,  dsp):
        self._call_specific("RemoveDSP", dsp._ptr)

    def remove_fade_points(self, dsp_clock_start, dsp_clock_end):
        self._call_specific("RemoveFadePoints", c_ulonglong(dsp_clock_start), c_ulonglong(dsp_clock_end))
        
    def set_callback(self, cb):
        cbi = CHANNELCONTROL_CALLBACK(cb)
        self._cb = cb
        self._call_specific("SetCallback", cbi)

    def set_fade_point_ramp(self, dsp_clock, volume):
        self._call_specific("SetFadePointRamp", c_ulonglong(dsp_clock), c_float(volume))

    def set_mix_levels_input(self, *levels):
        level_array = (c_float * len(levels))(*levels)
        self._call_specific("SetMixLevelsInput", level_array, len(level_array))

    def set_mix_levels_output(self, frontleft, frontright, center, lfe, surroundleft, surroundright, backleft, backright):
        self._call_specific("SetMixLevelsOutput", c_float(frontleft), c_float(frontright), c_float(center), c_float(lfe), c_float(surroundleft), c_float(surroundright), c_float(backleft), c_float(backright))

    def set_pan(self, pan):
        self._call_specific("SetPan", c_float(pan))
    def stop(self):
        self._call_specific("Stop")

    