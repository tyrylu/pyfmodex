from ctypes import *
from utils import ckresult
from structures import *
from globalvars import dll as _dll
from structobject import Structobject as so

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
        self._size = size

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, count):
        ckresult(_dll.FMOD_System_SetDSPBufferSize(self._sysptr, self._size, count))
        self._count = count

class ThreedSettings(object):
    def __init__(self, sptr, dopplerscale, distancefactor, rolloffscale):
        self._sysptr = sptr
        self._distancefactor = distancefactor
        self._dopplerscale = dopplerscale
        self._rolloffscale = rolloffscale

    @property
    def distance_factor(self):
        return self._distancefactor

    @distance_factor.setter
    def distance_factor(self, factor):
        ckresult(_dll.FMOD_System_Set3DSettings(self._sysptr, self._dopplerscale, factor, self._rolloffscale))
        self._distancefactor = factor

    @property
    def doppler_scale(self):
        return self._dopplerscale

    @doppler_scale.setter
    def doppler_scale(self, scale):
        ckresult(_dll.FMOD_System_Set3DSettings(self._sysptr, scale, self._distancefactor, self._rolloffscale))
        self._dopplerscale = scale

    @property
    def rolloff_scale(self):
        return self._rolloffscale

    @rolloff_scale.setter
    def rolloff_scale(self, rscale):
        ckresult(_dll.FMOD_System_Set3DSettings(self._sysptr, self._distancefactor, self._dopplerscale, rscale))
        self._rolloffscale = rscale

class System(object):
    def __init__(self):
        self._ptr = c_int()
        ckresult(_dll.FMOD_System_Create(byref(self._ptr)))

    def close(self):
        ckresult(_dll.FMOD_System_Close(self._ptr))

    @property
    def num_3d_listeners(self):
        num = c_int()
        ckresult(_dll.FMOD_System_Get3DNumListeners(self._ptr, byref(num)))
        return num.value

    def get_cdrom_drive_name(self, index):
        n1 = c_char_p()
        n2 = c_char_p()
        n3 = c_char_p()
        ckresult(_dll.FMOD_System_GetCDROMDriveName(self._ptr, byref(n1), sizeof(n1), byref(n2), sizeof(n2), byref(n3), sizeof(n3)))
        return so(drive_name=n1.value, scsi_name=n2.value, device_name=n3.value)

    @property
    def cpu_usage(self):
        dsp = c_float()
        stream = c_float()
        geometry = c_float()
        update = c_float()
        total = c_float()
        ckresult(_dll.FMOD_System_GetCPUUsage(self._ptr, byref(dsp), byref(stream), byref(geometry), byref(update), byref(total)))
        return so(dsp=dsp.value, stream=stream.value, geometry=geometry.value, update=update.value, total=total.value)

    @property
    def channels_playing(self):
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
        return so(x=x.value, y=y.value, active=active.value)

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
        return so(hi=hi.value, lo=lo.value)

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
        return so(caps=caps.value, minfreq=minfreq.value, maxfreq=maxfreq.value, mode=mode.value)

    def get_driver_info(self, id):
        name = c_char_p()
        guid = GUID()
        ckresult(_dll.FMOD_System_GetDriverInfo(self._ptr, id, byref(name), sizeof(name), byref(guid)))
        return so(name=nae, guid=guid)

    def get_geometry_occlusion(self, listener, source):
        listener = VECTOR.from_list(listener)
        source = VECTOR.from_list(source)
        direct = c_float()
        reverb = c_float()
        ckresult(_dll.FMOD_System_GetGeometryOcclusion(self._ptr, byref(listener), byref(source), byref(direct), byref(reverb)))
        return so(direct=direct.value, reverb=reverb.value)

    @property
    def geometry_max_world_size(self):
        wsize = c_float()
        ckresult(_dll.FMOD_System_GetGeometrySettings(self._ptr, byref(wsize)))
        return wsize.value

    @geometry_max_world_size.setter
    def geometry_max_world_size(self, size):
        ckresult(_dll.FMOD_System_SetGeometrySettings(self._ptr, size))

    @property
    def hardware_channels(self):
        num2d = c_int()
        num3d = c_int()
        total = c_int()
        ckresult(_dll.FMOD_System_GetHardwareChannels(self._ptr, byref(num2d), byref(num3d), byref(total)))
        return so(num_2d=num2d.value, num_3d=num3d.value, total=total.value)

    def get_memory_info(membits, event_membits):
        #What can be done with fourth argument...?
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

    @property
    def output_handle(self):
        handle = c_void_p()
        ckresult(_dll.FMOD_System_GetOutputHandle(self._ptr, byref(handle)))
        return handle.value

    def get_plugin_handle(type, index):
        handle = c_uint()
        ckresult(_dll.FMOD_System_GetPluginHandle(self._ptr, type, index, byref(handle)))
        return handle.value

    def get_plugin_info(self, handle):
        type = c_int()
        name = c_char_p()
        ver = c_uint()
        ckresult(_dll.FMOD_System_GetPluginInfo(self._ptr, handle, byref(type), byref(name), sizeof(name), byref(ver)))
        return so(type=type.value, name=name.value, version=ver.value)

    def get_record_driver_caps(self, id):
        caps = c_uint()
        minfreq = c_int()
        maxfreq = c_int()
        ckresult(_dll.FMOD_System_GetRecordDriverCaps(self._ptr, id, byref(caps), byref(minfreq), byref(maxfreq)))
        return so(caps=caps.value, minfreq=minfreq.value, maxfreq=maxfreq.value)

    def get_record_driver_info(self, index):
        name = c_char_p()
        guid = GUID()
        ckresult(_dll.FMOD_System_GetRecordDriverInfo(self._ptr, index, byref(name), sizeof(name), byref(guid)))
        return so(name=name.value, guid=guid)

    @property
    def record_num_drivers(self):
        num = c_int()
        ckresult(_dll.FMOD_System_GetRecordNumDrivers(self._ptr, byref(num)))
        return num.value

    def get_record_position(self, index):
        pos = c_uint()
        ckresult(_dll.FMOD_System_GetRecordPosition(self._ptr, index, byref(ppos)))
        return pos.value

    @property
    def reverb_ambient_properties(self):
        props = REVERBPROPERTIES()
        ckresult(_dll.FMOD_System_GetReverbAmbientProperties(self._ptr, byref(props)))

    @reverb_ambient_properties.setter
    def reverb_ambient_properties(self, props):
        ckresult(_dll.FMOD_System_SetReverbAmbientProperties(self._ptr, byref(props)))

    def get_reverb_properties(self, instance = 0):
        props = REVERBPROPERTIES()
        props.Instance = instance
        ckresult(_dll.FMOD_System_GetReverbProperties(self._ptr, byref(props)))
        return props

    def set_reverb_properties(self, props, instance=0):
        props.Instance = instance
        ckresult(_dll.FMOD_System_SetReverbProperties(self._ptr, byref(props)))

    @property
    def software_channels(self):
        channels = c_int()
        ckresult(_dll.FMOD_System_GetSoftwareChannels(self._ptr, byref(channels)))
        return channels.value

    @software_channels.setter
    def software_channels(self, num):
        ckresult(_dll.FMOD_System_SetSoftwareChannels(self._ptr, num))

