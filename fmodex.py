import constants
from ctypes import *
_dll = windll.fmodex
class cpuUsageInfo(object):
    def __init__(self, dsp, stream, update, total):
        self._dsp = dsp
        self._stream = stream
        self._update = update
        self._total = total

    @property
    def dsp(self):
        return self._dsp

    @property
    def stream(self):
        return self._stream

    @property
    def update(self):
        return self._update

    @property
    def total(self):
        return self._total
class CDROMDriveName(object):
    def __init__(self, drivename, scsiname, devicename):
        self._drivename = drivename
        self._scsiname = scsiname
        self._devicename = devicename

    @property
    def driveName(self):
        return self._drivename

    @property
    def scsiName(self):
        return self._scsiname

    @property
    def deviceName(self):
        return self._devicename
class system(object):
    def __init__(self, numchannels=32):
        self._ptr = c_int(0)
        res = _dll.FMOD_System_Create(byref(self._ptr))
        res2 = _dll.FMOD_System_Init(self._ptr, numchannels, constants.FMOD_INIT_NORMAL, 0)

    @property
    def num3DListeners(self):
        num = c_int()
        _dll.FMOD_System_Get3DNumListeners(self._ptr, byref(num))
        return num.value

    def getCDROMDriveName(self, index):
        n1 = c_char_p()
        n2 = c_char_p()
        n3 = c_char_p()
        _dll.FMOD_System_GetCDROMDriveName(self._ptr, byref(n1), sizeof(n1), byref(n2), sizeof(n2), byref(n3), sizeof(n3))
        return CDROMDriveName(n1.value, n2.value, n3.value)

    @property
    def cpuUsage(self):
        dsp = c_float()
        stream = c_float()
        update = c_float()
        total = c_float()
        _dll.FMOD_System_GetCPUUsage(self._ptr, byref(dsp), byref(stream), byref(update), byref(total))
        return cpuUsageInfo(dsp.value, stream.value, update.value, total.value)

    @property
    def channelsPlaying(self):
        channels = c_int()
        _dll.FMOD_System_GetChannelsPlaying(self._ptr, byref(channels))
        return channels.value