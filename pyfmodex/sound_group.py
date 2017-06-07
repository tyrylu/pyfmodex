from ctypes import *
from .globalvars import get_class
from .fmodobject import *
from .enums import SOUNDGROUP_BEHAVIOR

class SoundGroup(FmodObject):

    @property    
    def max_audible(self):
        val = c_int()
        self._call_fmod("FMOD_SoundGroup_GetMaxAudible", byref(val))
        return val.value
    @max_audible.setter
    def max_audible(self, val):
        self._call_fmod("FMOD_SoundGroup_SetMaxAudible", val)

    @property
    def max_audible_behavior(self):
        behavior = c_int()
        self._call_fmod("FMOD_SoundGroup_GetMaxAudibleBehavior", byref(behavior))
        return SOUNDGROUP_BEHAVIOR(behavior.value)
    @max_audible_behavior.setter
    def max_audible_behavior(self, behavior):
        self._call_fmod("FMOD_SoundGroup_SetMaxAudibleBehavior", behavior.value)

    @property
    def mute_fade_speed(self):
        speed = c_float()
        self._call_fmod("FMOD_SoundGroup_GetMuteFadeSpeed", byref(speed))
        return speed.value
    @mute_fade_speed.setter
    def mute_fade_speed(self, speed):
        self._call_fmod("FMOD_SoundGroup_SetMuteFadeSpeed", c_float(speed))

    @property
    def name(self):
        buf = create_string_buffer(512)
        self._call_fmod("FMOD_SoundGroup_GetName", buf, 512)
        return buf.value

    @property
    def num_playing(self):
        num = c_int()
        self._call_fmod("FMOD_SoundGroup_GetNumPlaying", byref(num))
        return num.value

    @property
    def num_sounds(self):
        num = c_int()
        self._call_fmod("FMOD_SoundGroup_GetNumSounds", byref(num))
        return num.value

    def get_sound(self, idx):
        sndptr = c_void_p()
        self._call_fmod("FMOD_SoundGroup_GetSound", idx, byref(sndptr))
        return get_class("Sound")(sndptr)

    @property
    def system_object(self):
        sysptr = c_void_p()
        self._call_fmod("FMOD_SoundGroup_GetSystemObject", byref(sysptr))
        return get_class("System")(sysptr, False)

    @property
    def volume(self):
        vol = c_float()
        self._call_fmod("FMOD_SoundGroup_GetVolume", byref(vol))
        return vol.value
    @volume.setter
    def volume(self, vol):
        self._call_fmod("FMOD_SoundGroup_SetVolume", c_float(vol))

    def release(self):
        self._call_fmod("FMOD_SoundGroup_Release")

    def stop(self):
        self._call_fmod("FMOD_SoundGroup_Stop")