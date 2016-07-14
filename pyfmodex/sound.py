from .fmodobject import *
from .fmodobject import _dll
from .structures import TAG, VECTOR
from .globalvars import get_class
from .utils import prepare_str

class ConeSettings(object):
    def __init__(self, sptr):
        self._sptr = sptr
        self._in = c_float()
        self._out = c_float()
        self._outvol = c_float()
        ckresult(_dll.FMOD_Sound_Get3DConeSettings(self._sptr, byref(self._in), byref(self._out), byref(self._outvol)))

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
        ckresult(_dll.FMOD_Sound_Set3DConeSettings(self._sptr, self._in, self._out, self._outvol))

class Sound(FmodObject):
    def add_sync_point(self, offset, offset_type, name):
        name = prepare_str(name, "ascii")
        s_ptr = c_void_p()
        ckresult(_dll.FMOD_Sound_AddSyncPoint(self._ptr, offset, offset_type, name, byref(s_ptr)))
        return s_ptr

    def delete_sync_point(self, point):
        ckresult(_dll.FMOD_Sound_DeleteSyncPoint(self._ptr, point))

    @property
    def threed_cone_settings(self):
        return ConeSettings(self._ptr)

    @property
    def custom_rolloff(self):
        """Returns the custom rolloff curve.
        :rtype: List of [x, y, z] lists.
        """
        num = c_int()
        self._call_fmod("FMOD_Sound_Get3DCustomRolloff", None, byref(num))
        curve = (VECTOR * num.value)()
        self._call_fmod("FMOD_Sound_Get3DCustomRolloff", byref(curve), 0)
        return [p.to_list() for p in curve]
    @custom_rolloff.setter
    def custom_rolloff(self, curve):
        """Sets the custom rolloff curve.
        :param curve: The curve to set.
        :type curve: A list of something that can be treated as a list of [x, y, z] values e.g. implements indexing in some way.
        """
        native_curve = (VECTOR * len(curve))(*[VECTOR.from_list(lst) for lst in curve])
        self._call_fmod("FMOD_Sound_Set3DCustomRolloff", native_curve, len(native_curve))

    @property
    def _min_max_distance(self):
        min = c_float()
        max = c_float()
        ckresult(_dll.FMOD_Sound_Get3DMinMaxDistance(self._ptr, byref(min), byref(max)))
        return (min.value, max.value)
    @_min_max_distance.setter
    def _min_max_distance(self, dists):
        ckresult(_dll.FMOD_Sound_Set3DMinMaxDistance(self._ptr, c_float(dists[0]), c_float(dists[1])))

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
    def _defaults(self):
        freq = c_float()
        vol = c_float()
        pan = c_float()
        pri = c_int()
        ckresult(_dll.FMOD_Sound_GetDefaults(self._ptr, byref(freq), byref(vol), byref(pan), byref(pri)))
        return [freq.value, vol.value, pan.value, pri.value]
    @_defaults.setter
    def _defaults(self, vals):
        ckresult(_dll.FMOD_Sound_SetDefaults(self._ptr, c_float(vals[0]), c_float(vals[1]), c_float(vals[2]), vals[3]))

    @property
    def default_frequency(self):
        return self._defaults[0]
    @default_frequency.setter
    def default_frequency(self, freq):
        d = self._defaults
        d[0] = freq
        self._defaults = d

    @property
    def default_volume(self):
        return self._defaults[1]
    @default_volume.setter
    def default_volume(self, vol):
        d = self._defaults
        d[1] = vol
        self._defaults = d

    @property
    def default_pan(self):
        return self._defaults[2]
    @default_pan.setter
    def default_pan(self, pan):
        d = self._defaults
        d[2] = pan
        self._defaults = d

    @property
    def default_priority(self):
        return self._defaults[3]
    @default_priority.setter
    def default_priority(self, pri):
        d = self._defaults
        d[3] = pri
        self._defaults = d

    @property
    def format(self):
        type = c_int()
        format = c_int()
        bits = c_int()
        ckresult(_dll.FMOD_Sound_GetFormat(self._ptr, byref(type), byref(format), byref(bits)))
        return so(type=type.value, format=format.value, bits=bits.value)

    def get_length(self, ltype):
        len = c_uint()
        ckresult(_dll.FMOD_Sound_GetLength(self._ptr, byref(len), ltype))
        return len.value

    @property
    def loop_count(self):
        c = c_int()
        ckresult(_dll.FMOD_Sound_GetLoopCount(self._ptr, byref(c)))
        return c.value
    @loop_count.setter
    def loop_count(self, count):
        ckresult(_dll.FMOD_Sound_SetLoopCount(self._ptr, count))

    @property
    def loop_points(self):
        """Returns tuple of two tuples ((start, startunit),(end, endunit))"""
        start = c_uint()
        startunit = c_int()    
        end = c_uint()
        endunit = c_int()
        ckresult(_dll.FMOD_Sound_GetLoopPoints(self._ptr, byref(start), byref(startunit), byref(end), byref(endunit)))
        return ((start.value, startunit.value), (end.value, endunit.value))
    @loop_points.setter
    def loop_points(self, p):
        """Same format as returned from this property is required to successfully call this setter."""
        ckresult(_dll.FMOD_Sound_SetLoopPoints(self._ptr, p[0][0], p[0][1], p[1][0], p[1][1]))

    @property
    def mode(self):
        mode = c_int()
        ckresult(_dll.FMOD_Sound_GetMode(self._ptr, byref(mode)))
        return mode.value
    @mode.setter
    def mode(self, m):
        ckresult(_dll.FMOD_Sound_SetMode(self._ptr, m))

    def get_music_channel_volume(self, channel):
        v = c_float()
        ckresult(_dll.FMOD_Sound_GetMusicChannelVolume(self._ptr, channel, byref(v)))
        return v.value
    def set_music_channel_volume(self, id, vol):
        ckresult(_dll.FMOD_Sound_SetMusicChannelVolume(self._ptr, id, c_float(vol)))

    @property
    def num_music_channels(self):
        num = c_int()
        ckresult(_dll.FMOD_Sound_GetMusicNumChannels(self._ptr, byref(num)))
        return num.value

    @property
    def name(self):
        name = create_string_buffer(256)
        ckresult(_dll.FMOD_Sound_GetName(self._ptr, byref(name), 256))
        return name.value

    @property
    def num_subsounds(self):
        num = c_int()
        ckresult(_dll.FMOD_Sound_GetNumSubSounds(self._ptr, byref(num)))
        return num.value

    @property
    def num_sync_points(self):
        num = c_int()
        ckresult(_dll.FMOD_Sound_GetNumSyncPoints(self._ptr, byref(num)))
        return num.value

    @property
    def num_tags(self):
        num = c_int()
        ckresult(_dll.FMOD_Sound_GetNumTags(self._ptr, byref(num)))
        return num.value

    @property
    def open_state(self):
        state = c_int()
        percentbuffered = c_uint()
        starving = c_bool()
        diskbusy = c_bool()
        ckresult(_dll.FMOD_Sound_GetOpenState(self._ptr, byref(state), byref(percentbuffered), byref(starving), byref(diskbusy)))
        return so(state=state.value, percent_buffered=percentbuffered.value, starving=starving.value, disk_busy=diskbusy.value)

    @property
    def sound_group(self):
        grp_ptr = c_void_p()
        ckresult(_dll.FMOD_Sound_GetSoundGroup(self._ptr, byref(grp_ptr)))
        return get_class("SoundGroup")(grp_ptr)
    @sound_group.setter
    def sound_group(self, group):
        check_type(group, get_class("SoundGroup"))
        ckresult(_dll.FMOD_Sound_SetSoundGroup(self._ptr, group._ptr))

    def get_subsound(self, index):
        sh_ptr = c_void_p()
        ckresult(_dll.FMOD_Sound_GetSubSound(self._ptr, index, byref(sh_ptr)))
        return Sound(sh_ptr)

    def get_sync_point(self, index):
        sp = c_int()
        ckresult(_dll.FMOD_Sound_GetSyncPoint(self._ptr, index, byref(sp)))
        return sp.value

    def get_sync_point_info(self, point):
        name = c_char_p()
        offset = c_uint()
        offsettype = c_int()
        ckresult(_dll.FMOD_Sound_GetSyncPointInfo(self._ptr, point, byref(name), 256, byref(offset), byref(offsettype)))
        return so(name=name.value, offset=offset.value, offset_type=offsettype.value)

    @property
    def system_object(self):
        sptr = c_void_p()
        ckresult(_dll.FMOD_Sound_GetSystemObject(self._ptr, byref(sptr)))
        return get_class("System")(sptr, False)

    def play(self, paused=False):
        return self.system_object.play_sound(self, paused)

    def get_tag(self, index, name=None):
        name = prepare_str(name, "ascii")
        tag = TAG()
        ckresult(_dll.FMOD_Sound_GetTag(self._ptr, name, index, byref(tag)))
        return tag

    @property
    def _variations(self):
        freq = c_float()
        vol = c_float()
        pan = c_float()
        ckresult(_dll.FMOD_Sound_GetVariations(self._ptr, byref(freq), byref(vol), byref(pan)))
        return [freq.value, vol.value, pan.value]
    @_variations.setter
    def _variations(self, vars):
        ckresult(_dll.FMOD_Sound_SetVariations(self._ptr, c_float(vars[0]), c_float(vars[1]), c_float(vars[2])))

    @property
    def frequency_variation(self):
        return self._variations[0]
    @frequency_variation.setter
    def frequency_variation(self, var):
        v = self._variations
        v[0] = var
        self._variations = var

    @property
    def volume_variation(self):
        return self._variations[1]
    @volume_variation.setter
    def volume_variation(self, var):
        v = self._variations
        v[1] = var
        self._variations = var

    @property
    def pan_variation(self):
        return self._variations[2]
    @pan_variation.setter
    def pan_variation(self, var):
        v = self._variations
        v[2] = var
        self._variations = var

    def lock(self, offset, length):
        ptr1 = c_void_p()
        len1 = c_uint()
        ptr2 = c_void_p()
        len2 = c_uint()
        ckresult(_dll.FMOD_Sound_Lock(self._ptr, offset, length, byref(ptr1), byref(ptr2), byref(len1), byref(len2)))
        return ((ptr1, len1), (ptr2, len2))

    def release(self):
        ckresult(_dll.FMOD_Sound_Release(self._ptr))

    def set_subsound(self, index, snd):
        check_type(snd, Sound)
        ckresult(_dll.FMOD_Sound_SetSubSound(self._ptr, index, snd._ptr))

    def set_subsound_sentence(self, sounds):
        a = c_int * len(sounds)
        ptrs = [o._ptr for o in sounds]
        ai = a(*ptrs)
        ckresult(_dll.FMOD_Sound_SetSubSoundSentence(self._ptr, ai, len(ai)))

    def unlock(self, i1, i2):
        """I1 and I2 are tuples of form (ptr, len)."""
        ckresult(_dll.FMOD_Sound_Unlock(self._ptr, i1[0], i2[0], i1[1], i2[1]))

    @property
    def music_speed(self):
        speed = c_float()
        self._call_fmod("FMOD_Sound_GetMusicSpeed", byref(speed))
        return speed.value
    @music_speed.setter
    def music_speed(self, speed):
        self._call_fmod("FMOD_Sound_SetMusicSpeed", c_float(speed))

    def read_data(self, length):
        """Read a fragment of the sound's decoded data.
        :param length: The requested length.
        :returns: The data and the actual length.
        :rtype: Tuple of the form (data, actual)."""
        buf = create_string_buffer(length)
        actual = c_uint()
        self._call_fmod("FMOD_Sound_ReadData", buf, length, byref(actual))
        return buf.value, actual.value

    def seek_data(self, offset):
        """Seeks for data reading purposes.
        :param offset: The offset to seek to in PCM samples.
        :type offset: Int or long, but must be in range of an unsigned long, not python's arbitrary long."""
        self._call_fmod("FMOD_Sound_SeekData", offset)