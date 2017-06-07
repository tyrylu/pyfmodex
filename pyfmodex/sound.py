from ctypes import *
from .fmodobject import *
from .fmodobject import _dll
from .structures import TAG, VECTOR
from .globalvars import get_class
from .utils import prepare_str, ckresult, check_type
from .structobject import Structobject as so
from .enums import SOUND_TYPE, SOUND_FORMAT, OPENSTATE
from .flags import MODE, TIMEUNIT

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
        self._call_fmod("FMOD_Sound_AddSyncPoint", offset, int(offset_type), name, byref(s_ptr))
        return s_ptr.value

    def delete_sync_point(self, point):
        self._call_fmod("FMOD_Sound_DeleteSyncPoint", c_void_p(point))

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
        print(num.value)
        curve = (VECTOR * num.value)()
        self._call_fmod("FMOD_Sound_Get3DCustomRolloff", byref(curve), None)
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
        self._call_fmod("FMOD_Sound_Get3DMinMaxDistance", byref(min), byref(max))
        return (min.value, max.value)
    @_min_max_distance.setter
    def _min_max_distance(self, dists):
        self._call_fmod("FMOD_Sound_Set3DMinMaxDistance", c_float(dists[0]), c_float(dists[1]))

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
        pri = c_int()
        self._call_fmod("FMOD_Sound_GetDefaults", byref(freq), byref(pri))
        return [freq.value, pri.value]
    @_defaults.setter
    def _defaults(self, vals):
        self._call_fmod("FMOD_Sound_SetDefaults", c_float(vals[0]), vals[1])

    @property
    def default_frequency(self):
        return self._defaults[0]
    @default_frequency.setter
    def default_frequency(self, freq):
        d = self._defaults
        d[0] = freq
        self._defaults = d

    @property
    def default_priority(self):
        return self._defaults[1]
    @default_priority.setter
    def default_priority(self, pri):
        d = self._defaults
        d[1] = pri
        self._defaults = d

    @property
    def format(self):
        type = c_int()
        format = c_int()
        channels = c_int()
        bits = c_int()
        self._call_fmod("FMOD_Sound_GetFormat", byref(type), byref(format), byref(channels), byref(bits))
        return so(type=SOUND_TYPE(type.value), format=SOUND_FORMAT(format.value), channels=channels.value, bits=bits.value)
        
    def get_length(self, ltype):
        len = c_uint()
        self._call_fmod("FMOD_Sound_GetLength", byref(len), int(ltype))
        return len.value

    @property
    def loop_count(self):
        c = c_int()
        self._call_fmod("FMOD_Sound_GetLoopCount", byref(c))
        return c.value
    @loop_count.setter
    def loop_count(self, count):
        self._call_fmod("FMOD_Sound_SetLoopCount", count)

    def get_loop_points(self, start_unit, end_unit):
        """Returns tuple (start, end)"""
        start = c_uint()
        end = c_uint()
        self._call_fmod("FMOD_Sound_GetLoopPoints", byref(start), int(start_unit), byref(end), int(end_unit))
        return start.value, end.value
    
    def set_loop_points(self, start, start_unit, end, end_unit):
        self._call_fmod("FMOD_Sound_SetLoopPoints", start, int(start_unit), end, int(end_unit))

    @property
    def mode(self):
        mode = c_int()
        self._call_fmod("FMOD_Sound_GetMode", byref(mode))
        return MODE(mode.value)
    @mode.setter
    def mode(self, m):
        self._call_fmod("FMOD_Sound_SetMode", int(m))

    def get_music_channel_volume(self, channel):
        v = c_float()
        self._call_fmod("FMOD_Sound_GetMusicChannelVolume", channel, byref(v))
        return v.value
    def set_music_channel_volume(self, id, vol):
        self._call_fmod("FMOD_Sound_SetMusicChannelVolume", id, c_float(vol))

    @property
    def num_music_channels(self):
        num = c_int()
        self._call_fmod("FMOD_Sound_GetMusicNumChannels", byref(num))
        return num.value

    @property
    def name(self):
        name = create_string_buffer(256)
        self._call_fmod("FMOD_Sound_GetName", byref(name), 256)
        return name.value

    @property
    def num_subsounds(self):
        num = c_int()
        self._call_fmod("FMOD_Sound_GetNumSubSounds", byref(num))
        return num.value

    @property
    def num_sync_points(self):
        num = c_int()
        self._call_fmod("FMOD_Sound_GetNumSyncPoints", byref(num))
        return num.value

    @property
    def num_tags(self):
        num = c_int()
        self._call_fmod("FMOD_Sound_GetNumTags", byref(num))
        return num.value

    @property
    def open_state(self):
        state = c_int()
        percentbuffered = c_uint()
        starving = c_bool()
        diskbusy = c_bool()
        self._call_fmod("FMOD_Sound_GetOpenState", byref(state), byref(percentbuffered), byref(starving), byref(diskbusy))
        return so(state=OPENSTATE(state.value), percent_buffered=percentbuffered.value, starving=starving.value, disk_busy=diskbusy.value)

    @property
    def sound_group(self):
        grp_ptr = c_void_p()
        self._call_fmod("FMOD_Sound_GetSoundGroup", byref(grp_ptr))
        return get_class("SoundGroup")(grp_ptr)
    @sound_group.setter
    def sound_group(self, group):
        check_type(group, get_class("SoundGroup"))
        self._call_fmod("FMOD_Sound_SetSoundGroup", group._ptr)

    def get_subsound(self, index):
        sh_ptr = c_void_p()
        self._call_fmod("FMOD_Sound_GetSubSound", index, byref(sh_ptr))
        return Sound(sh_ptr)
    @property
    def subsound_parent(self):
        sh_ptr = c_void_p()
        self._call_fmod("FMOD_Sound_GetSubSoundParent", byref(sh_ptr))
        return Sound(sh_ptr)

    def get_sync_point(self, index):
        sp = c_void_p()
        self._call_fmod("FMOD_Sound_GetSyncPoint", index, byref(sp))
        return sp.value

    def get_sync_point_info(self, point):
        name = create_string_buffer(256)
        offset = c_uint()
        offsettype = c_int()
        self._call_fmod("FMOD_Sound_GetSyncPointInfo", c_void_p(point), byref(name), 256, byref(offset), byref(offsettype))
        return so(name=name.value, offset=offset.value, offset_type=TIMEUNIT(offsettype.value))

    @property
    def system_object(self):
        sptr = c_void_p()
        self._call_fmod("FMOD_Sound_GetSystemObject", byref(sptr))
        return get_class("System")(sptr, False)

    def play(self, channel_group=None, paused=False):
        return self.system_object.play_sound(self, channel_group, paused)

    def get_tag(self, index, name=None):
        name = prepare_str(name, "ascii")
        tag = TAG()
        ckresult(_dll.FMOD_Sound_GetTag(self._ptr, name, index, byref(tag)))
        return tag

    def lock(self, offset, length):
        ptr1 = c_void_p()
        len1 = c_uint()
        ptr2 = c_void_p()
        len2 = c_uint()
        ckresult(_dll.FMOD_Sound_Lock(self._ptr, offset, length, byref(ptr1), byref(ptr2), byref(len1), byref(len2)))
        return ((ptr1, len1), (ptr2, len2))

    def release(self):
        self._call_fmod("FMOD_Sound_Release")

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

