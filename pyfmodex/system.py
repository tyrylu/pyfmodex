"""Module containing all classes related to the Fmod EX System class."""
from ctypes import *
from .utils import *
from .structures import *
from .globalvars import dll as _dll
from .structobject import Structobject as so
from .globalvars import get_class
from .constants import FMOD_3D, FMOD_SOFTWARE, FMOD_INIT_NORMAL, FMOD_CHANNEL_FREE, FMOD_CREATESTREAM
from .callbackprototypes import SYSTEM_CALLBACK, ROLLOFF_CALLBACK

class Listener(object):
    """An 3d listener."""
    def __init__(self, sptr, id):
        """Constructor, should be considered non-public."""
        pos = VECTOR()
        vel = VECTOR()
        fwd = VECTOR()
        up = VECTOR()
        self._sysptr = sptr
        self._id = id
        ckresult(_dll.FMOD_System_Get3DListenerAttributes(self._sysptr, id, byref(pos), byref(vel), byref(fwd), byref(up)))
        self._pos = pos
        self._vel = vel
        self._fwd = fwd
        self._up = up

    @property
    def position(self):
        """Returns the listener's position.
        :returns: A list in the form [x, y, z] with the position's coordinates.
        :rtype: list
        """
        return self._pos.to_list()
    @position.setter
    def position(self, poslist):
        self._pos = VECTOR.from_list(poslist)
        self._commit()

    @property
    def velocity(self):
        """The velocity vector.
        :returns: List in the form [x, y, z].
        :rtype: list
        """
        return self._vel.to_list()
    @velocity.setter
    def velocity(self, vellist):
        self._vel = VECTOR.from_list(vellist)
        self._commit()

    @property
    def forward(self):
        """The forward vector.
        :returns: List in the form [x, y, z].
        :rtype: list
        """
        return self._fwd.to_list()
    @forward.setter
    def forward(self, fwdlist):
        self._fwd = VECTOR.from_list(fwdlist)
        self._commit()

    @property
    def up(self):
        """The up vector.
        :returns: List in the form [x, y, z].
        :rtype: list
        """
        return self._up.to_list()
    @up.setter
    def up(self, uplist):
        self._up = VECTOR.from_list(uplist)
        self._commit()

    def _commit(self):
        ckresult(_dll.FMOD_System_Set3DListenerAttributes(self._sysptr, self._id, byref(self._pos), byref(self._vel), byref(self._fwd), byref(self._up)))

class DSPBufferSizeInfo(object):
    """Class containing information about the DSP buffer sizes and counts."""
    def __init__(self, sptr, size, count):
        """Constructor, should be considered non-public."""
        self._sysptr = sptr
        self._size = size
        self._count = count

    @property
    def size(self):
        """Size of one of the DSP buffers.
        :rtype: int
        """
        return self._size

    @size.setter
    def size(self, size):
        ckresult(_dll.FMOD_System_SetDSPBufferSize(self._sysptr, size, self._count))
        self._size = size

    @property
    def count(self):
        """Count of DSP buffers used.
        :rtype: int
        """
        return self._count

    @count.setter
    def count(self, count):
        ckresult(_dll.FMOD_System_SetDSPBufferSize(self._sysptr, self._size, count))
        self._count = count

class ThreedSettings(object):
    """Class containing various 3d related settings. Values should be changed before calling System.init."""
    def __init__(self, sptr, dopplerscale, distancefactor, rolloffscale):
        """Constructor, should be considered non-public."""
        self._sysptr = sptr
        self._distancefactor = distancefactor
        self._dopplerscale = dopplerscale
        self._rolloffscale = rolloffscale

    @property
    def distance_factor(self):
        return self._distancefactor

    @distance_factor.setter
    def distance_factor(self, factor):
        ckresult(_dll.FMOD_System_Set3DSettings(self._sysptr, c_float(self._dopplerscale), c_float(factor), c_float(self._rolloffscale)))
        self._distancefactor = factor

    @property
    def doppler_scale(self):
        return self._dopplerscale

    @doppler_scale.setter
    def doppler_scale(self, scale):
        ckresult(_dll.FMOD_System_Set3DSettings(self._sysptr, c_float(scale), c_float(self._distancefactor), c_float(self._rolloffscale)))
        self._dopplerscale = scale

    @property
    def rolloff_scale(self):
        return self._rolloffscale

    @rolloff_scale.setter
    def rolloff_scale(self, rscale):
        ckresult(_dll.FMOD_System_Set3DSettings(self._sysptr, c_float(self._distancefactor), c_float(self._dopplerscale), c_float(rscale)))
        self._rolloffscale = rscale

class System(object):
    def __init__(self, ptr=None, create=True):
        """If create is True, new instance is created. Otherwise ptr must be a valid pointer."""
        if create:
            self._ptr = c_void_p()
            ckresult(_dll.FMOD_System_Create(byref(self._ptr)))
        else:
            self._ptr = ptr

    def add_dsp(self,d):
        check_type(d, get_class("DSP"))
        dsp_ptr = c_void_p()
        ckresult(_dll.FMOD_System_AddDSP(self._ptr, d._ptr, byref(dsp_ptr)))
        return get_class("DSP_Connection")(dsp_ptr)

    def create_channel_group(self, name):
        name = prepare_str(name)
        cp = c_int()
        ckresult(_dll.FMOD_System_CreateChannelGroup(self._ptr, name, byref(cp)))
        return get_class("ChannelGroup")(cp)

    def create_codec(self, desc, priority):
        ckresult(_dll.FMOD_System_CreateCodec(self._ptr, desc, priority))

    def create_dsp(self, dspdesc):
        dsp_ptr = c_void_p()
        ckresult(_dll.FMOD_System_CreateDSP(self._ptr, dspdesc, byref(dsp_ptr)))
        return get_class("DSP")(dsp_ptr)

    def create_dsp_by_plugin(self, plugin_handle):
        dsp_ptr = c_void_p()
        ckresult(_dll.FMOD_System_CreateDSPByPlugin(self._ptr, plugin_handle, byref(dsp_ptr)))
        return get_class("DSP")(dsp_ptr)

    def create_dsp_by_type(self, type):
        dsp_ptr = c_void_p()
        ckresult(_dll.FMOD_System_CreateDSPByType(self._ptr, type, byref(dsp_ptr)))
        return get_class("DSP")(dsp_ptr)

    def create_geometry(self, maxpoligons, maxvertices):
        geo_ptr = c_void_p()
        ckresult(_dll.FMOD_System_CreateGeometry(self._ptr, maxpoligons, maxvertices, byref(geo_ptr)))
        return get_class("Geometry")(geo_ptr)

    def create_reverb(self):
        r_ptr = c_void_p()
        ckresult(_dll.FMOD_System_CreateReverb(self._ptr, byref(r_ptr)))
        return get_class("Reverb")(r_ptr)

    def create_sound(self, name_or_addr, mode=FMOD_3D|FMOD_SOFTWARE, exinfo=None):
        name_or_addr = prepare_str(name_or_addr)
        snd_ptr = c_void_p()
        if exinfo is not None: exinfo = byref(exinfo)
        ckresult(_dll.FMOD_System_CreateSound(self._ptr, name_or_addr, mode, exinfo, byref(snd_ptr)))
        return get_class("Sound")(snd_ptr)

    def create_sound_group(self, name):
        name = prepare_str(name)
        sg_ptr = c_void_p()
        ckresult(_dll.FMOD_System_CreateSoundGroup(self._ptr, name, byref(sg_ptr)))
        return get_class("SoundGroup")(sg_ptr)

    def create_stream(self, name_or_addr, mode=FMOD_3D|FMOD_SOFTWARE, exinfo=None):
        name_or_addr = prepare_str(name_or_addr)
        mode = mode|FMOD_CREATESTREAM
        return self.create_sound(name_or_addr, mode, exinfo)
    
    def close(self):
        ckresult(_dll.FMOD_System_Close(self._ptr))

    @property
    def num_3d_listeners(self):
        num = c_int()
        ckresult(_dll.FMOD_System_Get3DNumListeners(self._ptr, byref(num)))
        return num.value

    def get_cdrom_drive_name(self, index):
        n1 = create_string_buffer(256)
        n2 = create_string_buffer(256)
        n3 = create_string_buffer(256)
        ckresult(_dll.FMOD_System_GetCDROMDriveName(self._ptr, index, byref(n1), sizeof(n1), byref(n2), sizeof(n2), byref(n3), sizeof(n3)))
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

    def get_channel(self, id):
        c_ptr = c_void_p()
        ckresult(_dll.FMOD_System_GetChannel(self._ptr, id, byref(c_ptr)))
        return get_class("Channel")(c_ptr)

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
        ckresult(_dll.FMOD_System_Set3DSpeakerPosition(self._ptr, speaker, c_float(x), c_float(y), active))

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
        return MAKELONG(hi.value, lo.value)


    @property
    def dsp_head(self):
        dsp_ptr = c_void_p()
        ckresult(_dll.FMOD_System_GetDSPHead(self._ptr, byref(dsp_ptr)))
        return get_class("DSP")(dsp_ptr)

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
        outputfreq = c_int()
        mode = c_uint()
        ckresult(_dll.FMOD_System_GetDriverCaps(self._ptr, id, byref(caps), byref(outputfreq), byref(mode)))
        return so(caps=caps.value, moutput_frequency=outputfreq.value, mode=mode.value)

    def get_driver_info(self, id):
        name = create_string_buffer(256)
        guid = GUID()
        ckresult(_dll.FMOD_System_GetDriverInfo(self._ptr, id, name, 256, byref(guid)))
        return so(name=name.value, guid=guid)

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
        ckresult(_dll.FMOD_System_SetGeometrySettings(self._ptr, c_float(size)))

    @property
    def hardware_channels(self):
        num2d = c_int()
        num3d = c_int()
        total = c_int()
        ckresult(_dll.FMOD_System_GetHardwareChannels(self._ptr, byref(num2d), byref(num3d), byref(total)))
        return so(num_2d=num2d.value, num_3d=num3d.value, total=total.value)


    @property
    def master_channel_group(self):
        grp_ptr = c_void_p()
        ckresult(_dll.FMOD_System_GetMasterChannelGroup(self._ptr, byref(grp_ptr)))
        return get_class("ChannelGroup")(grp_ptr)

    @property
    def master_sound_group(self):
        grp_ptr = c_void_p()
        ckresult(_dll.FMOD_System_GetMasterSoundGroup(self._ptr, byref(grp_ptr)))
        return get_class("SoundGroup")(grp_ptr)
    
    def get_memory_info(self, membits, event_membits):
        #Detailed memory info support will be there, but currently this is not the most important thing.
        usage = c_uint()
        ckresult(_dll.FMOD_System_GetMemoryInfo(self._ptr, membits, event_membits, byref(usage), None))
        return usage.value

    @property
    def network_proxy(self):
        server = create_string_buffer(256)
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
        ckresult(_dll.FMOD_System_SetNetworkTimeout(self._ptr, timeout))

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

    def get_plugin_handle(self, type, index):
        handle = c_uint()
        ckresult(_dll.FMOD_System_GetPluginHandle(self._ptr, type, index, byref(handle)))
        return handle.value

    def get_plugin_info(self, handle):
        type = c_int()
        name = create_string_buffer(256)
        ver = c_uint()
        ckresult(_dll.FMOD_System_GetPluginInfo(self._ptr, handle, byref(type), byref(name), 256, byref(ver)))
        return so(type=type.value, name=name.value, version=ver.value)

    def get_record_driver_caps(self, id):
        caps = c_uint()
        minfreq = c_int()
        maxfreq = c_int()
        ckresult(_dll.FMOD_System_GetRecordDriverCaps(self._ptr, id, byref(caps), byref(minfreq), byref(maxfreq)))
        return so(caps=caps.value, minfreq=minfreq.value, maxfreq=maxfreq.value)

    def get_record_driver_info(self, index):
        name = create_string_buffer(256)
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
        ckresult(_dll.FMOD_System_GetRecordPosition(self._ptr, index, byref(pos)))
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

    @property
    def speaker_mode(self):
        mode = c_int()
        ckresult(_dll.FMOD_System_GetSpeakerMode(self._ptr, byref(mode)))
        return mode.value
    @speaker_mode.setter
    def speaker_mode(self, mode):
        ckresult(_dll.FMOD_System_SetSpeakerMode(self._ptr, mode))

    def get_spectrum(self, numvalues, channeloffset, window):
        arr = c_float * numvalues
        arri = arr()
        ckresult(_dll.FMOD_System_GetSpectrum(self._ptr, byref(arri), numvalues, channeloffset, window))
        return list(arri)
    def get_wave_data(self, numvalues, channeloffset):
        arr = c_float * numvalues
        arri = arr()
        ckresult(_dll.FMOD_System_GetWaveData(self._ptr, byref(arri), numvalues, channeloffset))
        return list(arri)
    def init(self, maxchannels=1000, flags=FMOD_INIT_NORMAL, extra=None):
        ckresult(_dll.FMOD_System_Init(self._ptr, maxchannels, flags, extra))

    def is_recording(self, id):
        rec = c_int()
        ckresult(_dll.FMOD_System_IsRecording(self._ptr, id, byref(rec)))
        return rec.value

    def load_geometry(self, data):
        d = c_void_p(data)
        geo_ptr = c_void_p()
        ckresult(_dll.FMOD_System_LoadGeometry(self._ptr, d, len(data), byref(geo_ptr)))
        return get_class("Geometry")(geo_ptr)

    def load_plugin(self, filename, priority):
        filename = prepare_str(filename)
        handle = c_uint()
        ckresult(_dll.FMOD_System_LoadPlugin(self._ptr, filename, byref(handle), priority))

    def lock_dsp(self):
        ckresult(_dll.FMOD_System_LockDSP(self._ptr))

    def play_dsp(self, d, paused=False, channelid=FMOD_CHANNEL_FREE):
        check_type(d, get_class("DSP"))
        c_ptr = c_void_p()
        ckresult(_dll.FMOD_System_PlayDSP(self._ptr, channelid, d._ptr, paused, byref(c_ptr)))
        return get_class("Channel")(c_ptr)

    def play_sound(self, snd, paused=False, channelid=FMOD_CHANNEL_FREE):
        check_type(snd, get_class("Sound"))
        c_ptr = c_void_p()
        ckresult(_dll.FMOD_System_PlaySound(self._ptr, channelid, snd._ptr, paused, byref(c_ptr)))
        return get_class("Channel")(c_ptr)

    def record_start(self, id, snd, loop=False):
        check_type(snd, get_class("Sound"))
        ckresult(_dll.FMOD_System_RecordStart(self._ptr, id, snd._ptr, loop))

    def record_stop(self, id):
        ckresult(_dll.FMOD_System_RecordStop(self._ptr, id))

    def release(self):
        ckresult(_dll.FMOD_System_Release(self._ptr))

    def set_3d_rolloff_callback(self, callback):
        cb = ROLLOFF_CALLBACK(callback)
        ckresult(_dll.FMOD_System_Set3DRolloffCallback(self._ptr, cb))
    def set_callback(self, callback):
        cb = FMOD_SYSTEM_CALLBACK(callback)
        ckresult(_dll.FMOD_System_SetCallback(self._ptr, cb))

    def set_plugin_path(self, path):
        ckresult(_dll.FMOD_System_SetPluginPath(self._ptr, path))

    def unload_plugin(self, handle):
        ckresult(_dll.FMOD_System_UnloadPlugin(self._ptr, handle))

    def unlock_dsp(self):
        ckresult(_dll.FMOD_System_UnlockDSP(self._ptr))

    def update(self):
        ckresult(_dll.FMOD_System_Update(self._ptr))

    @property
    def version(self):
        ver = c_uint()
        ckresult(_dll.FMOD_System_GetVersion(self._ptr, byref(ver)))
        return ver.value

    def listener(self, id=0):
        return Listener(self._ptr, id)

    @property
    def num_record_drivers(self):
        num = c_int()
        ckresult(_dll.FMOD_System_GetRecordNumDrivers(self._ptr, byref(num)))
        return num.value
