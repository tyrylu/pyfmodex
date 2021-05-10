import os
import unittest.mock as mock
import pytest
from pyfmodex.enums import DSP_TYPE, SPEAKERMODE, PLUGINTYPE, OUTPUTTYPE, SPEAKER, SOUND_FORMAT, TIMEUNIT
from pyfmodex.flags import SYSTEM_CALLBACK_TYPE, MODE
from pyfmodex import FmodError, System
from pyfmodex.structures import CREATESOUNDEXINFO

test_file = os.path.join(os.path.dirname(__file__), "test.fsb")
def test_version(system):
    assert system.version


def test_attach_filesystem(initialized_system):
    mock_open = mock.Mock(return_value=0)
    initialized_system.attach_file_system(mock_open, None, None, None)
    initialized_system.create_sound(test_file)
    assert mock_open.call_count == 1
    assert mock_open.call_args[0][0] == test_file.encode("utf-8")

def test_create_channel_group(initialized_system):
    group = initialized_system.create_channel_group("test group")
    assert group._ptr.value > 0

def test_create_dsp_by_type(initialized_system):
    initialized_system.create_dsp_by_type(DSP_TYPE.OSCILLATOR)

def test_create_geometry(initialized_system):
    initialized_system.create_geometry(2, 2)
    
def test_create_reverb_3d(initialized_system):
    initialized_system.create_reverb_3d()

def test_create_sound(initialized_system):
    initialized_system.create_sound(test_file)
    with pytest.raises(FmodError) as ex:
        initialized_system.create_sound("some nonexistent.wav")
def test_create_sound_custom(initialized_system):
    exinfo = CREATESOUNDEXINFO()
    exinfo.numchannels = 2
    exinfo.format = SOUND_FORMAT.PCM16.value
    exinfo.defaultfrequency = 44100
    exinfo.length = 44100 * 16 * 2
    sound = initialized_system.create_sound(0, mode=MODE.LOOP_NORMAL | MODE.OPENUSER, exinfo=exinfo)
    sound.release()


def test_create_sound_group(initialized_system):
    initialized_system.create_sound_group("root group")

def test_create_stream(initialized_system):
    initialized_system.create_stream(test_file)

def test_close():
    # We can not use the test session wide fixture, because it would have to be initialized after this test.
    system = System()
    system.init()
    system.close()

def test_num_3d_listeners(initialized_system):
    assert initialized_system.num_3d_listeners == 1
    initialized_system.num_3d_listeners = 2
    assert initialized_system.num_3d_listeners == 2

def test_cpu_usage(initialized_system):
    assert initialized_system.cpu_usage

def test_get_channel(channel):
    chan = channel.system_object.get_channel(channel.index)
    assert chan.index == channel.index

def test_channels_playing(initialized_system):
    assert initialized_system.channels_playing.channels == 0
    assert initialized_system.channels_playing.real_channels == 0

def test_threed_settings(initialized_system):
    settings = initialized_system.threed_settings
    assert settings.distance_factor == 1.0
    settings.rolloff_scale = 2.0
    assert settings.rolloff_scale == 2.0

def test_advanced_settings(system):
    settings = system.advanced_settings
    assert settings.maxAT9Codecs == 0
    system.advanced_settings = settings

def test_dsp_buffer_size(system):
    size = system.dsp_buffer_size
    assert size.count == 4
    size.count = 6
    assert size.count == 6

def test_get_default_mix_matrix(initialized_system):
    matrix = initialized_system.get_default_mix_matrix(SPEAKERMODE.MONO, SPEAKERMODE.STEREO)
    assert len(matrix) == 2
    assert matrix[0] == matrix[1]

def test_driver(system):
    assert system.driver == 0

def test_get_driver_info(system):
    info = system.get_driver_info(0)
    assert info.system_rate == 44100 or info.system_rate == 48000
    assert len(info.name) > 0

def test_file_usage(system):
    usage = system.file_usage
    assert usage.sample_bytes_read == 0

def test_get_geometry_occlusion(system):
    occlusion = system.get_geometry_occlusion([0, 0, 0], [1, 1, 1])
    assert occlusion.direct == 0

def test_geometry_max_world_size(system):
    system.geometry_max_world_size = 10000
    assert system.geometry_max_world_size == 10000

def test_master_channel_group(initialized_system):
    assert initialized_system.master_channel_group
def test_master_sound_group(initialized_system):
    assert initialized_system.master_sound_group

def test_network_proxy(system):
    assert system.network_proxy == b""
    system.network_proxy = "proxy.org"
    assert system.network_proxy == b"proxy.org"
    system.network_proxy = ""

def test_network_timeout(system):
    assert system.network_timeout == 5000
    system.network_timeout = 10000
    assert system.network_timeout == 10000

def test_nm_drivers(system):
    assert system.num_drivers > 0

def test_get_num_plugins(system):
    assert system.get_num_plugins(PLUGINTYPE.CODEC) > 0

def test_output(system):
    system.output = OUTPUTTYPE.NOSOUND
    assert system.output is OUTPUTTYPE.NOSOUND
    system.output = OUTPUTTYPE.AUTODETECT

def test_output_handle(initialized_system):
    if initialized_system.output_handle:
        assert initialized_system.output_handle > 0

def test_get_plugin_handle(system):
    assert system.get_plugin_handle(PLUGINTYPE.CODEC,  0) > 0

def test_get_plugin_info(system):
    handle = system.get_plugin_handle(PLUGINTYPE.CODEC,  0)
    info = system.get_plugin_info(handle)
    assert info.type is PLUGINTYPE.CODEC
    assert info.name == b"FMOD FSB Codec"

def test_get_record_driver_info(initialized_system):
    info = initialized_system.get_record_driver_info(0)
    assert info.system_rate == 44100 or info.system_rate == 48000
        

def test_record_num_drivers(initialized_system):
    assert initialized_system.record_num_drivers.drivers > 0

def test_reverb_properties(initialized_system):
    props = initialized_system.get_reverb_properties(0)
    assert props.Instance == 0
    assert props.EarlyDelay == 7.0
    props.EarlyDelay = 5.0
    initialized_system.set_reverb_properties(0, props)
    assert initialized_system.get_reverb_properties(0).EarlyDelay == 5.0

def test_software_channels(system):
    assert system.software_channels == 64
    system.software_channels = 128
    assert system.software_channels == 128

def test_software_format(system):
    format = system.software_format
    assert format.sample_rate > 0
    format.sample_rate = 96000
    system.software_format = format
    assert system.software_format.sample_rate == 96000

def test_get_speaker_mode_channels(initialized_system):
    assert initialized_system.get_speaker_mode_channels(SPEAKERMODE.STEREO) == 2

def test_get_set_speaker_position(initialized_system):
    pos = initialized_system.get_speaker_position(SPEAKER.FRONT_RIGHT)
    assert pos.active
    assert pos.x == 0.5
    pos.active = False
    initialized_system.set_speaker_position(SPEAKER.FRONT_RIGHT, pos)
    assert not initialized_system.get_speaker_position(SPEAKER.FRONT_RIGHT).active

def test_stream_buffer_size(system):
    size = system.stream_buffer_size
    assert size.size == 16384
    assert size.unit is TIMEUNIT.RAWBYTES
    size.size = 65535
    system.stream_buffer_size = size
    assert system.stream_buffer_size.size == 65535

def test_is_recording(initialized_system):
    assert not initialized_system.is_recording(0)

def test_lock_unlock_dsp(initialized_system):
    initialized_system.lock_dsp()
    initialized_system.unlock_dsp()

def test_mixer_suspend_resume(initialized_system):
    initialized_system.mixer_suspend()
    initialized_system.mixer_resume()

def test_play_dsp(initialized_system):
    dsp = initialized_system.create_dsp_by_type(DSP_TYPE.OSCILLATOR)
    channel = initialized_system.play_dsp(dsp, paused=True)
    channel.stop()

def test_play_sound(initialized_system, sound):
    channel = initialized_system.play_sound(sound.get_subsound(0), paused=True)
    channel.stop()

def test_set_3d_rolloffcallback(system):
    mock_callback = mock.Mock(return_value=0)
    system.set_3d_rolloff_callback(mock_callback)

def test_set_callback(initialized_system):
    mock_callback = mock.Mock(return_value=0)
    initialized_system.set_callback(mock_callback, SYSTEM_CALLBACK_TYPE.PREUPDATE)
    initialized_system.update()
    assert mock_callback.call_count == 1
    initialized_system.set_callback(None, SYSTEM_CALLBACK_TYPE.PREUPDATE)

def test_listener(initialized_system):
    listener = initialized_system.listener()
    assert listener.position == [0.0, 0.0, 0.0]
    listener.position = [1.0, 2.0, 3.0]
    assert listener.position == [1.0, 2.0, 3.0]
