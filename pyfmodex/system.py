"""Module containing all classes related to the Fmod EX System class."""
from ctypes import *
from .utils import *
from .structures import *
from .globalvars import dll as _dll
from .structobject import Structobject as so
from .globalvars import get_class
from .flags import INIT_FLAGS, MODE, TIMEUNIT
from .enums import OUTPUTTYPE, PLUGINTYPE
from .callback_prototypes import SYSTEM_CALLBACK, ROLLOFF_CALLBACK
from .fmodobject import FmodObject

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

class System(FmodObject):
    def __init__(self, ptr=None, create=True):
        """If create is True, new instance is created. Otherwise ptr must be a valid pointer."""
        self._system_callbacks = {}
        if create:
            self._ptr = c_void_p()
            ckresult(_dll.FMOD_System_Create(byref(self._ptr)))
        else:
            self._ptr = ptr

    def attach_channel_group_to_port(self, port_type, port_index, group, passthru=False):
        ckresult(_dll.FMOD_System_AttachChannelGroupToPort(self._ptr, port_type, port_index, group._ptr, passthru))

    def attach_file_system(self, user_open, user_close, user_read, user_seek):
        if user_open:
            user_open = FILE_OPEN_CALLBACK(user_open)
        if user_close:
            user_close = FILE_CLOSE_CALLBACK(user_close)
        if user_read:
            file_read = FILE_READ_CALLBACK(user_read)
        if user_seek:
            user_seek = FILE_SEEK_CALLBACK(user_seek)
        self._call_fmod("FMOD_System_AttachFileSystem", user_open, user_close, user_read, user_seek)
        self._user_open = user_open
        self._user_close = user_close
        self._user_read = user_read
        self._user_seek = user_seek

    def create_channel_group(self, name):
        name = prepare_str(name)
        cp = c_void_p()
        ckresult(_dll.FMOD_System_CreateChannelGroup(self._ptr, name, byref(cp)))
        return get_class("ChannelGroup")(cp)

    def create_dsp(self, dspdesc):
        dsp_ptr = c_void_p()
        ckresult(_dll.FMOD_System_CreateDSP(self._ptr, byref(dspdesc), byref(dsp_ptr)))
        return get_class("DSP")(dsp_ptr)

    def create_dsp_by_plugin(self, plugin_handle):
        dsp_ptr = c_void_p()
        ckresult(_dll.FMOD_System_CreateDSPByPlugin(self._ptr, plugin_handle, byref(dsp_ptr)))
        return get_class("DSP")(dsp_ptr)

    def create_dsp_by_type(self, type):
        dsp_ptr = c_void_p()
        ckresult(_dll.FMOD_System_CreateDSPByType(self._ptr, type.value, byref(dsp_ptr)))
        return get_class("DSP")(dsp_ptr)

    def create_geometry(self, maxpoligons, maxvertices):
        geo_ptr = c_void_p()
        ckresult(_dll.FMOD_System_CreateGeometry(self._ptr, maxpoligons, maxvertices, byref(geo_ptr)))
        return get_class("Geometry")(geo_ptr)

    def create_reverb_3d(self):
        r_ptr = c_void_p()
        ckresult(_dll.FMOD_System_CreateReverb3D(self._ptr, byref(r_ptr)))
        return get_class("Reverb3D")(r_ptr)

    def create_sound(self, name_or_addr, mode=MODE.THREED, exinfo=None):
        name_or_addr = prepare_str(name_or_addr)
        snd_ptr = c_void_p()
        if exinfo is not None: exinfo = byref(exinfo)
        ckresult(_dll.FMOD_System_CreateSound(self._ptr, name_or_addr, int(mode), exinfo, byref(snd_ptr)))
        return get_class("Sound")(snd_ptr)

    def create_sound_group(self, name):
        name = prepare_str(name)
        sg_ptr = c_void_p()
        ckresult(_dll.FMOD_System_CreateSoundGroup(self._ptr, name, byref(sg_ptr)))
        return get_class("SoundGroup")(sg_ptr)

    def create_stream(self, name_or_addr, mode=MODE.THREED, exinfo=None):
        mode = mode|MODE.CREATESTREAM
        return self.create_sound(name_or_addr, mode, exinfo)
    
    def close(self):
        ckresult(_dll.FMOD_System_Close(self._ptr))

    def detach_channel_group_from_port(self, group):
        ckresult(_dll.FMOD_System_DetachChannelGroupFromPort(self._ptr, group._ptr))
    @property
    def num_3d_listeners(self):
        num = c_int()
        ckresult(_dll.FMOD_System_Get3DNumListeners(self._ptr, byref(num)))
        return num.value

    @num_3d_listeners.setter
    def num_3d_listeners(self, num):
        self._call_fmod("FMOD_System_Set3DNumListeners", num)
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
        self._call_fmod("FMOD_System_GetChannelsPlaying", byref(channels))
        return channels.value

    @property
    def threed_settings(self):
        dscale = c_float()
        distancefactor = c_float()
        rscale = c_float()
        ckresult(_dll.FMOD_System_Get3DSettings(self._ptr, byref(dscale), byref(distancefactor), byref(rscale)))
        return ThreedSettings(self._ptr, distancefactor.value, dscale.value, rscale.value)

    @property
    def advanced_settings(self):
        settings = ADVANCEDSETTINGS()
        ckresult(_dll.FMOD_System_GetAdvancedSettings(self._ptr, byref(settings)))
        return settings

    @advanced_settings.setter
    def advanced_settings(self, settings):
        ckresult(_dll.FMOD_System_SetAdvancedSettings(self._ptr, byref(settings)))

    @property
    def dsp_buffer_size(self):
        size = c_uint()
        count = c_int()
        ckresult(_dll.FMOD_System_GetDSPBufferSize(self._ptr, byref(size), byref(count)))
        return DSPBufferSizeInfo(self._ptr, size.value, count.value)

    def get_dsp_info_by_plugin(self, handle):
        desc = DSP_DESCRIPTION()
        self._call_fmod("FMOD_System_GetDSPInfoByPlugin", byref(desc))
        return desc

    def get_default_mix_matrix(self, source_speaker_mode, target_speaker_mode, matrix_hop=0):
        target_channels = self.get_speaker_mode_channels(target_speaker_mode)
        if matrix_hop:
            source_channels = matrix_hop
        else:
            source_channels = self.get_speaker_mode_channels(source_speaker_mode)
        matrix = (c_float * (source_channels * target_channels))()
        self._call_fmod("FMOD_System_GetDefaultMixMatrix", source_speaker_mode.value, target_speaker_mode.value, matrix, matrix_hop)
        return matrix

    @property
    def driver(self):
        driver = c_int()
        ckresult(_dll.FMOD_System_GetDriver(self._ptr, byref(driver)))
        return driver.value

    @driver.setter
    def driver(self, driver):
        ckresult(_dll.FMOD_System_SetDriver(self._ptr, driver))

    def get_driver_info(self, id):
        name = create_string_buffer(256)
        guid = GUID()
        system_rate = c_int()
        speaker_mode = c_int()
        channels = c_int()
        ckresult(_dll.FMOD_System_GetDriverInfo(self._ptr, id, name, 256, byref(guid), byref(system_rate), byref(speaker_mode), byref(channels)))
        return so(name=name.value, guid=guid, system_rate=system_rate.value, speaker_mode=speaker_mode.value, speaker_mode_channels=channels.value)

    @property
    def file_usage(self):
        sample_bytes = c_longlong()
        stream_bytes = c_longlong()
        other_bytes = c_longlong()
        self._call_fmod("FMOD_System_GetFileUsage", byref(sample_bytes), byref(stream_bytes), byref(other_bytes))
        return so(sample_bytes_read=sample_bytes.value, stream_bytes_read=stream_bytes.value, other_bytes_read=other_bytes.value)

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
    def master_channel_group(self):
        grp_ptr = c_void_p()
        ckresult(_dll.FMOD_System_GetMasterChannelGroup(self._ptr, byref(grp_ptr)))
        return get_class("ChannelGroup")(grp_ptr)

    @property
    def master_sound_group(self):
        grp_ptr = c_void_p()
        ckresult(_dll.FMOD_System_GetMasterSoundGroup(self._ptr, byref(grp_ptr)))
        return get_class("SoundGroup")(grp_ptr)
    def get_nested_plugin(self, handle, index):
        nested = c_uint()
        self._call_fmod("FMOD_System_GetNestedPlugin", handle, index, byref(nested))
        return nested.value

    @property
    def network_proxy(self):
        server = create_string_buffer(256)
        ckresult(_dll.FMOD_System_GetNetworkProxy(self._ptr, byref(server), sizeof(server)))
        return server.value
    @network_proxy.setter
    def network_proxy(self, proxy):
        proxy = prepare_str(proxy)
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
    def num_drivers(self):
        num = c_int()
        ckresult(_dll.FMOD_System_GetNumDrivers(self._ptr, byref(num)))
        return num.value

    def get_num_nested_plugins(self, handle):
        num = c_int()
        self._call_fmod("FMOD_System_GetNumNestedPlugins", handle, byref(num))
        return num.value
    def get_num_plugins(self, plugintype):
        num = c_int()
        ckresult(_dll.FMOD_System_GetNumPlugins(self._ptr, plugintype.value, byref(num)))
        return num.value

    @property
    def output(self):
        output = c_int()
        ckresult(_dll.FMOD_System_GetOutput(self._ptr, byref(output)))
        return OUTPUTTYPE(output.value)

    @output.setter
    def output(self, out):
        ckresult(_dll.FMOD_System_SetOutput(self._ptr, out.value))

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
        ckresult(_dll.FMOD_System_GetPluginHandle(self._ptr, type.value, index, byref(handle)))
        return handle.value

    def get_plugin_info(self, handle):
        type = c_int()
        name = create_string_buffer(256)
        ver = c_uint()
        ckresult(_dll.FMOD_System_GetPluginInfo(self._ptr, handle, byref(type), byref(name), 256, byref(ver)))
        return so(type=PLUGINTYPE(type.value), name=name.value, version=ver.value)

    def get_record_driver_info(self, index):
        name = create_string_buffer(256)
        guid = GUID()
        system_rate = c_int()
        speaker_mode = c_int()
        channels = c_int()
        state = c_int()
        ckresult(_dll.FMOD_System_GetRecordDriverInfo(self._ptr, index, byref(name), sizeof(name), byref(guid), byref(system_rate), byref(speaker_mode), byref(channels), byref(state)))
        return so(name=name.value, guid=guid, system_rate=system_rate.value, speaker_mode=speaker_mode.value, speaker_mode_channels=channels.value, state=state.value)

    @property
    def record_num_drivers(self):
        num = c_int()
        ckresult(_dll.FMOD_System_GetRecordNumDrivers(self._ptr, byref(num)))
        return num.value

    def get_record_position(self, index):
        pos = c_uint()
        ckresult(_dll.FMOD_System_GetRecordPosition(self._ptr, index, byref(pos)))
        return pos.value

    def get_reverb_properties(self, instance = 0):
        props = REVERB_PROPERTIES()
        props.Instance = instance
        ckresult(_dll.FMOD_System_GetReverbProperties(self._ptr, instance, byref(props)))
        return props

    def set_reverb_properties(self, instance, props):
        self._call_fmod("FMOD_System_SetReverbProperties", instance, props)
    @property
    def software_channels(self):
        channels = c_int()
        ckresult(_dll.FMOD_System_GetSoftwareChannels(self._ptr, byref(channels)))
        return channels.value

    @software_channels.setter
    def software_channels(self, num):
        ckresult(_dll.FMOD_System_SetSoftwareChannels(self._ptr, num))
    @property
    def software_format(self):
        rate = c_int()
        mode = c_int()
        speakers = c_int()
        self._call_fmod("FMOD_System_GetSoftwareFormat", byref(rate), byref(mode), byref(speakers))
        return so(sample_rate=rate.value, speaker_mode=mode.value, raw_speakers=speakers.value)
    @software_format.setter
    def software_format(self, format):
        self._call_fmod("FMOD_System_SetSoftwareFormat", format.sample_rate, format.speaker_mode, format.raw_speakers)

    @property
    def sound_ram(self):
        current = c_int()
        max = c_int()
        total = c_int()
        self._call_fmod("FMOD_System_GetSoundRAM", byref(current), byref(max), byref(total))
        return so(current=current.value, max=max.value, total=total.value)
    def get_speaker_mode_channels(self, mode):
        channels = c_int()
        self._call_fmod("FMOD_System_GetSpeakerModeChannels", mode.value, byref(channels))
        return channels.value

    def get_speaker_position(self, speaker):
        x = c_float()
        y = c_float()
        active = c_bool()
        self._call_fmod("FMOD_System_GetSpeakerPosition", speaker.value, byref(x), byref(y), byref(active))
        return so(x=x.value, y=y.value, active=active.value)
    def set_speaker_position(self, speaker, pos):
        self._call_fmod("FMOD_System_SetSpeakerPosition", speaker.value, c_float(pos.x), c_float(pos.y), pos.active)

    @property
    def stream_buffer_size(self):
        size = c_uint()
        unit = c_int()
        self._call_fmod("FMOD_System_GetStreamBufferSize", byref(size), byref(unit))
        return so(size=size.value, unit=TIMEUNIT(unit.value))
    @stream_buffer_size.setter
    def stream_buffer_size(self, size):
        self._call_fmod("FMOD_System_SetStreamBufferSize", size.size, int(size.unit))

    def init(self, maxchannels=1000, flags=INIT_FLAGS.NORMAL, extra=None):
        ckresult(_dll.FMOD_System_Init(self._ptr, maxchannels, int(flags), extra))

    def is_recording(self, id):
        rec = c_int()
        ckresult(_dll.FMOD_System_IsRecording(self._ptr, id, byref(rec)))
        return rec.value

    def load_geometry(self, data):
        d = create_string_buffer(data)
        print(len(data))
        geo_ptr = c_void_p()
        ckresult(_dll.FMOD_System_LoadGeometry(self._ptr, d, len(data), byref(geo_ptr)))
        return get_class("Geometry")(geo_ptr)

    def load_plugin(self, filename, priority):
        filename = prepare_str(filename)
        handle = c_uint()
        ckresult(_dll.FMOD_System_LoadPlugin(self._ptr, filename, byref(handle), priority))
        return handle.value
    
    def lock_dsp(self):
        ckresult(_dll.FMOD_System_LockDSP(self._ptr))

    def mixer_resume(self):
        self._call_fmod("FMOD_System_MixerResume")

    def mixer_suspend(self):
        self._call_fmod("FMOD_System_MixerSuspend")
    def play_dsp(self, d, channel_group=None, paused=False):
        check_type(d, get_class("DSP"))
        if channel_group:
            check_type(channel_group, get_class("ChannelGroup"))
            group_ptr = channel_group._ptr
        else:
            group_ptr = None
        c_ptr = c_void_p()
        self._call_fmod("FMOD_System_PlayDSP", d._ptr, group_ptr, paused, byref(c_ptr))
        return get_class("Channel")(c_ptr)

    def play_sound(self, snd, channel_group=None, paused=False):
        check_type(snd, get_class("Sound"))
        if channel_group:
            check_type(channel_group, get_class("ChannelGroup"))
            group_ptr = channel_group._ptr
        else:
            group_ptr = None
        c_ptr = c_void_p()
        ckresult(_dll.FMOD_System_PlaySound(self._ptr, snd._ptr, group_ptr, paused, byref(c_ptr)))
        return get_class("Channel")(c_ptr)

    def record_start(self, id, snd, loop=False):
        check_type(snd, get_class("Sound"))
        ckresult(_dll.FMOD_System_RecordStart(self._ptr, id, snd._ptr, loop))

    def record_stop(self, id):
        ckresult(_dll.FMOD_System_RecordStop(self._ptr, id))
    def register_codec(self, description, priority):
        handle = c_uint()
        self._call_fmod("FMOD_System_RegisterCodec", byref(description), byref(handle), priority)
        return handle.value

    def register_dsp(self, description):
        handle = c_uint()
        self._call_fmod("FMOD_System_RegisterDSP", byref(description), byref(handle))
        return handle.value
    
    def register_output(self, description):
        handle = c_uint()
        self._call_fmod("FMOD_System_RegisterOutput", byref(description), byref(handle))
        return handle.value
    
    def release(self):
        ckresult(_dll.FMOD_System_Release(self._ptr))

    def set_3d_rolloff_callback(self, callback):
        cb = ROLLOFF_CALLBACK(callback or 0)
        self._rolloff_callback = cb
        ckresult(_dll.FMOD_System_Set3DRolloffCallback(self._ptr, cb))

    def set_callback(self, callback, callback_mask):
        cb = SYSTEM_CALLBACK(callback or 0)
        self._system_callbacks[callback_mask] = cb
        ckresult(_dll.FMOD_System_SetCallback(self._ptr, cb, int(callback_mask)))

    def set_file_system(self, user_open, user_close, user_read, user_seek, user_async_read, user_async_cancel, block_align=-1):
        self._call_fmod("FMOD_System_SetFileSystem", FILE_OPEN_CALLBACK(user_open), FILE_CLOSE_CALLBACK(user_close), FILE_READ_CALLBACK(user_read), FILE_SEEK_CALLBACK(user_seek), FILE_ASYNC_READ(user_async_read), FILE_ASYNC_CANCEL(user_async_cancel), block_align)

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

