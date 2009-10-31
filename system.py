from ctypes import *
from utils import ckresult
from structures import *
from globalvars import dll as _dll
class HardwareChannelsInfo(object):
    def __init__(self, num2d, num3d, total):
        self._num2d = num2d
        self._num3d = num3d
        self._total = total

    @property
    def num2d(self):
        return self._num2d

    @property
    def num3d(self):
        return self._num3d

    @property
    def total(self):
        return self._total


class DriverCapsInfo(object):
    def __init__(self, caps, minfreq, maxfreq, speakermode):
        self._caps = caps
        self._minfreq = minfreq
        self._maxfreq = maxfreq
        self._speakermode = speakermode

    @property
    def caps(self):
        return self._caps

    @property
    def minfrequency(self):
        return self._minfreq

    @property
    def maxfrequency(self):
        return self._maxfreq

    @property
    def control_panel_speaker_mode(self):
        return self._speakermode

class DSPBufferSizeInfo(object):
    def __init__(self, sptr, size, count):
        self._sysptr = sptr
        self._size = size
        self._count = count

    @property
    def size(self):
        return self._size
    @size.setter
    def size(self, size):
        ckresult(_dll.FMOD_System_SetDSPBufferSize(self._sysptr, size, self._count))
    @property
    def count(self):
        return self._count
    @count.setter
    def count(self, count):
        ckresult(_dll.FMOD_System_SetDSPBufferSize(self._sysptr, self._size, count))

class ThreedSettings(object):
    def __init__(self, sptr, dopplerscale, distancefactor, rolloffscale):
        self._sysptr = sptr
        self._distancefactor = distancefactor
        self._dopplerscale = dopplerscale
        self._rolloffscale = rolloffscale

    @property
    def distancefactor(self):
        return self._distancefactor

    @distancefactor.setter
    def distancefactor(self, factor):
        ckresult(_dll.FMOD_System_Set3DSettings(self._sysptr, self._dopplerscale, factor, self._rolloffscale))

    @property
    def dopplerscale(self):
        return self._dopplerscale

    @dopplerscale.setter
    def dopplerscale(self, scale):
        ckresult(_dll.FMOD_System_Set3DSettings(self._sysptr, scale, self._distancefactor, self._rolloffscale))
    @property
    def rolloffscale(self):
        return self._rolloffscale

    @rolloffscale.setter
    def rolloffscale(self, rscale):
        ckresult(_dll.FMOD_System_Set3DSettings(self._sysptr, self._distancefactor, self._dopplerscale, rscale))
class CPUUsageInfo(object):
    def __init__(self, dsp, stream, geometry, update, total):
        self._dsp = dsp
        self._stream = stream
        self._geometry = geometry
        self._update = update
        self._total = total

    @property
    def dsp(self):
        return self._dsp

    @property
    def stream(self):
        return self._stream

    @property
    def geometry(self):
        return self._geometry

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
class System(object):
    def __init__(self):
        self._ptr = c_int()
        ckresult(_dll.FMOD_System_Create(byref(self._ptr)))
    def close(self):
        ckresult(_dll.FMOD_System_Close(self._ptr))

    @property
    def num3DListeners(self):
        num = c_int()
        ckresult(_dll.FMOD_System_Get3DNumListeners(self._ptr, byref(num)))
        return num.value

    def getCDROMDriveName(self, index):
        n1 = c_char_p()
        n2 = c_char_p()
        n3 = c_char_p()
        ckresult(_dll.FMOD_System_GetCDROMDriveName(self._ptr, byref(n1), sizeof(n1), byref(n2), sizeof(n2), byref(n3), sizeof(n3)))
        return CDROMDriveName(n1.value, n2.value, n3.value)

    @property
    def cpuUsage(self):
        dsp = c_float()
        stream = c_float()
        geometry = c_float()
        update = c_float()
        total = c_float()
        ckresult(_dll.FMOD_System_GetCPUUsage(self._ptr, byref(dsp), byref(stream), byref(geometry), byref(update), byref(total)))
        return CPUUsageInfo(dsp.value, stream.value, geometry.value, update.value, total.value)

    @property
    def channelsPlaying(self):
        channels = c_int()
        ckresult(_dll.FMOD_System_GetChannelsPlaying(self._ptr, byref(channels)))
        return channels.value

    @property
    def threed_settings(self):
        dscale = c_float()

        distancefactor = c_float()
        rscale = c_float()
        ckresult(_dll.FMOD_System_Get3DSettings(self._ptr, byref(dscale), byref(distancefactor), byref(rscale)))
        return ThreedSettings(self._ptr, distancefactor.value, dscale.value, rscale.value)

    def get_3d_speaker_position(self, speaker):
        x = c_float()
        y = c_float()
        active = c_int()
        ckresult(_dll.FMOD_System_Get3DSpeakerPosition(self._ptr, speaker, byref(x), byref(y), byref(active)))
        return (x.value, y.value, active.value)

    def set_3d_speaker_position(self, speaker, x, y, active):
        ckresult(_dll.FMOD_System_Set3DSpeakerPosition(self._ptr, speaker, x, y, active))

    @property
    def advanced_settings(self):
        settings = ADVANCEDSETTINGS()
        ckresult(_dll.FMOD_System_GetAdvancedSettings(self._ptr, byref(settings)))
        return settings

    @advanced_settings.setter
    def advanced_settings(self, settings):
        ckresult(_dll.FMOD_System_SetAdvancedSettings(self._ptr, byref(settings)))

    @property
    def DSP_buffer_size(self):
        size = c_uint()
        count = c_int()
        ckresult(_dll.FMOD_System_GetDSPBufferSize(self._ptr, byref(size), byref(count)))
        return DSPBufferSizeInfo(self._ptr, size.value, count.value)

    @property
    def DSP_clock(self):
        hi = c_uint()
        lo = c_uint()
        ckresult(_dll.FMOD_System_GetDSPClock(self._ptr, byref(hi), byref(lo)))
        return (hi.value, lo.value)

    @property
    def driver(self):
        driver = c_int()
        ckresult(_dll.FMOD_System_GetDriver(self._ptr, byref(driver)))
        return driver.value

    @driver.setter
    def driver(self, driver):
        ckresult(_dll.FMOD_System_SetDriver(self._ptr, driver))

    def get_driver_caps(self, id):
        caps = c_uint()
        minfreq = c_int()
        maxfreq = c_int()
        mode = c_uint()
        ckresult(_dll.FMOD_System_GetDriverCaps(self._ptr, id, byref(caps), byref(minfreq), byref(maxfreq), byref(mode)))
        return DriverCapsInfo(caps.value, minfreq.value, maxfreq.value, mode.value)

    def get_driver_info(self, id):
        name = c_char_p()
        guid = GUID()
        ckresult(_dll.FMOD_System_GetDriverInfo(self._ptr, id, byref(name), sizeof(name), byref(guid)))
        return (name, guid)

    def get_geometry_occlusion(self, listener, source):
        listener = VECTOR.from_list(listener)
        source = VECTOR.from_list(source)
        direct = c_float()
        reverb = c_float()
        ckresult(_dll.FMOD_System_GetGeometryOcclusion(self._ptr, byref(listener), byref(source), byref(direct), byref(reverb)))
        return (direct.value, reverb.value)

    @property
    def geometry_max_world_size(self):
        wsize = c_float()
        ckresult(_dll.FMOD_System_GetGeometrySettings(self._ptr, byref(wsize)))
        return wsize.value
    @geometry_max_world_size.setter
    def geometry_max_world_size(self, size):
        ckresult(_dll.FMOD_System_SetGeometrySettings(self._ptr, size))

    @property
    def hardware_chanels(self):
        num2d = c_int()
        num3d = c_int()
        total = c_int()
        ckresult(_dll.FMOD_System_GetHardwareChannels(self._ptr, byref(num2d), byref(num3d), byref(total)))
        return HardwareChannelsInfo(num2d.value, num3d.value, total.value)

    def get_memory_info(membits, event_membits):
        # Which can be done with fourth argument...?
        usage = c_uint()
        ckresult(_dll.FMOD_System_GetMemoryInfo(self._ptr, membits, event_membits, byref(usage), None))
        return usage.value

    @property
    def network_proxy(self):
        server = c_char_p()
        ckresult(_dll.FMOD_System_GetNetworkProxy(self._ptr, byref(server), sizeof(server)))
    @network_proxy.setter
    def network_proxy(self, proxy):
        ckresult(_dll.FMOD_System_SetNetworkProxy(self._ptr, proxy))

    @property
    def network_timeout(self):
        timeout = c_int()
        ckresult(_dll.FMOD_System_GetNetworkTimeout(self._ptr, byref(timeout)))
        return timeout.value
    @network_timeout.setter
    def network_timeout(self, timeout):
        ckresult(_dll.FMOD_System_SetNetworkTimeout(self_ptr, timeout))

    @property
    def num_cdrom_drives(self):
        num = c_int()
        ckresult(_dll.FMOD_System_GetNumCDROMDrives(self._ptr, byref(num)))
        return num.value

    @property
    def num_drivers(self):
        num = c_int()
        ckresult(_dll.FMOD_System_GetNumDrivers(self._ptr, byref(num)))
        return num.value

    def get_num_plugins(self, plugintype):
        num = c_int()
        ckresult(_dll.FMOD_System_GetNumPlugins(self._ptr, plugintype, byref(num)))
        return num.value

    @property
    def output(self):
        output = c_int()
        ckresult(_dll.FMOD_System_GetOutput(self._ptr, byref(output)))
        return output.value
    @output.setter
    def output(self, out):
        ckresult(_dll.FMOD_System_SetOutput(self._ptr, out))

    @property
    def output_by_plugin(self):
        handle = c_uint()
        ckresult(_dll.FMOD_System_GetOutputByPlugin(self._ptr, byref(handle)))
        return handle.value
    @output_by_plugin.setter
    def output_by_plugin(self, handle):
        ckresult(_dll.FMOD_System_SetOutputByPlugin(self._ptr, handle))

