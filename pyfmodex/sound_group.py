from .globalvars import get_class
from .fmodobject import *
from .globalvars import dll as _dll
from ctypes import create_string_buffer

class SoundGroup(FmodObject):

    @property    
    def max_audible(self):
        val = c_int()
        ckresult(_dll.FMOD_SoundGroup_GetMaxAudible(self._ptr, byref(val)))
        return val.value
    @max_audible.setter
    def max_audible(self, val):
        ckresult(_dll.FMOD_SoundGroup_SetMaxAudible(self._ptr, val))

    @property
    def max_audible_behavior(self):
        behavior = c_int()
        ckresult(_dll.FMOD_SoundGroup_GetMaxAudibleBehavior(self._ptr, byref(behavior)))
        return behavior.value
    @max_audible_behavior.setter
    def max_audible_behavior(self, behavior):
        ckresult(_dll.FMOD_SoundGroup_SetMaxAudibleBehavior(self._ptr, behavior))

    @property
    def mute_fade_speed(self):
        speed = c_float()
        ckresult(_dll.FMOD_SoundGroup_GetMuteFadeSpeed(self._ptr, byref(speed)))
        return speed.value
    @mute_fade_speed.setter
    def mute_fade_speed(self, speed):
        ckresult(_dll.FMOD_SoundGroup_SetMuteFadeSpeed(self._ptr, speed))

    @property
    def name(self):
        buf = create_string_buffer(512)
        ckresult(_dll.FMOD_SoundGroup_GetName(self._ptr, buf, 512))
        return buf.value

    @property
    def num_playing(self):
        num = c_int()
        ckresult(_dll.FMOD_SoundGroup_GetNumPlaying(self._ptr, byref(num)))
        return num.value

    @property
    def num_sounds(self):
        num = c_int()
        ckresult(_dll.FMOD_SoundGroup_GetNumSounds(self._ptr, byref(num)))
        return num.value

    def get_sound(self, idx):
        sndptr = c_void_p()
        ckresult(_dll.FMOD_SoundGroup_GetSound(self._ptr, idx, byref(sndptr)))
        return get_class("Sound")(sndptr)

    @property
    def system_object(self):
        sysptr = c_void_p()
        ckresult(_dll.FMOD_SoundGroup_GetSystemObject(self._ptr, byref(sysptr)))
        return get_class("System")(sysptr, False)

    @property
    def volume(self):
        vol = c_float()
        ckresult(_dll.FMOD_SoundGroup_GetVolume(self._ptr, byref(vol)))
        return vol.value
    @volume.setter
    def volume(self, vol):
        ckresult(_dll.FMOD_SoundGroup_SetVolume(self._ptr, c_float(vol)))

    def release(self):
        ckresult(_dll.FMOD_SoundGroup_Release(self._ptr))

    def stop(self):
        ckresult(_dll.FMOD_SoundGroup_Stop(self._ptr))