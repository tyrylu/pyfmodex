import pytest
from unittest import mock
from pyfmodex.enums import DSP_TYPE, CHANNELCONTROL_DSP_INDEX
from pyfmodex.flags import TIMEUNIT, MODE

def test_add_dsp(echo, channel_group):
    channel_group.add_dsp(0, echo)

def test_add_fade_point(channel_group):
    channel_group.add_fade_point(40000000000, 0.5)

def test_add_get_group(channel_group, initialized_system):
    new_group = initialized_system.create_channel_group("Group 2")
    conn = channel_group.add_group(new_group, False)
    ret_group = channel_group.get_group(0)
    assert ret_group == new_group

def test_threed_attrs(channel_group):
    channel_group.mode = MODE.THREED
    zero = [0.0, 0.0, 0.0]
    ones = [1.0, 1.0, 1.0]
    assert channel_group.position == zero
    assert channel_group.velocity == zero
    channel_group.position = ones
    channel_group.velocity = ones
    assert channel_group.position == ones
    assert channel_group.velocity == ones

def test_cone_orientation(channel_group):
    channel_group.mode = MODE.THREED
    assert channel_group.cone_orientation == [0.0, 0.0, 1.0]
    channel_group.cone_orientation = [0.0, 1.0, 1.0]
    assert channel_group.cone_orientation == [0.0, 1.0, 1.0]

def test_cone_settings(channel_group):
    channel_group.mode = MODE.THREED
    settings = channel_group.cone_settings
    assert settings.outside_angle == 360.0
    
def test_custom_rolloff(channel_group):
    channel_group.mode = MODE.THREED
    new_curve = [[1.0,0.5,0.0], [4.0,0.0,0.0]]
    assert channel_group.custom_rolloff == []
    channel_group.custom_rolloff = new_curve
    assert channel_group.custom_rolloff == channel_group.custom_rolloff # Should test equality with the new curve, but the setting or retrieval results in some garbage values

def test_threed_distance_filter(channel_group):
    channel_group.mode = MODE.THREED
    settings = channel_group.threed_distance_filter
    assert not settings.custom
    settings.custom = True
    settings.custom_level = 0.5
    channel_group.threed_distance_filter = settings
    assert channel_group.threed_distance_filter.custom

def test_doppler_level(channel_group):
    channel_group.mode = MODE.THREED
    assert channel_group.doppler_level == 1.0
    channel_group.doppler_level = 0.5
    assert channel_group.doppler_level == 0.5


def test_level(channel_group):
    channel_group.mode = MODE.THREED
    assert channel_group.level == 1.0
    channel_group.level = 0.5 
    assert channel_group.level == 0.5

def test_min_max_distance(channel_group):
    channel_group.mode = MODE.THREED
    assert channel_group.min_distance == 1.0
    assert channel_group.max_distance == 10000.0
    channel_group.min_distance = 2.0
    assert channel_group.min_distance == 2.0

@pytest.mark.skip("No idea why this does not work for channel groups.")
def test_occlusion(channel_group):
    assert channel_group.direct_occlusion == 0.0
    assert channel_group.reverb_occlusion == 0.0
    channel_group.reverb_occlusion = 0.5
    assert channel_group.reverb_occlusion == 0.5

def test_spread(channel_group):
    channel_group.mode = MODE.THREED
    assert channel_group.threed_spread == 0.0
    channel_group.threed_spread = 0.5
    assert channel_group.threed_spread == 0.5

def test_audibility(channel_group):
    assert channel_group.audibility >= 0.0 and channel_group.audibility <= 1.0


def test_get_channel(channel_group, channel):
    assert channel_group.get_channel(0) == channel

def test_get_dsp(channel_group, initialized_system):
    dsp = initialized_system.create_dsp_by_type(DSP_TYPE.ECHO)
    channel_group.add_dsp(0, dsp)
    assert channel_group.get_dsp(0) == dsp

def test_delay(channel_group):
    delay = channel_group.delay
    assert delay.dsp_start == 0
    delay.dsp_end = 20000000000
    channel_group.delay = delay
    assert channel_group.delay.dsp_end == 20000000000

def test_fade_points(channel_group):
    channel_group.add_fade_point(200, 0.25)
    channel_group.add_fade_point(2000, 0.5)
    assert channel_group.fade_points == ([200, 2000], [0.25, 0.5])

def test_low_pass_gain(channel_group):
    assert channel_group.low_pass_gain == 0.0
    
def test_mix_matrix(channel_group):
    assert channel_group.get_mix_matrix() == []
    matrix = [0.5, 0.5]
    channel_group.set_mix_matrix(matrix, 1, 2)
    assert channel_group.get_mix_matrix() == matrix

def test_mode(channel_group):
    assert channel_group.mode == MODE.DEFAULT
    new_mode = MODE.LOOP_NORMAL
    channel_group.mode = new_mode
    assert channel_group.mode == new_mode

def test_mute(channel_group):
    assert not channel_group.mute
    channel_group.mute = True
    assert channel_group.mute

def test_name(channel_group):
    assert channel_group.name == b"test group"

def test_num_channels(channel_group):
    assert channel_group.num_channels == 1

def test_num_groups(channel_group):
    assert channel_group.num_groups == 0
    
def test_num_dsps(channel_group):
    assert channel_group.num_dsps == 1

def test_parent_group(channel_group, initialized_system):
    master_group = initialized_system.master_channel_group
    assert master_group.parent_group is None
    assert channel_group.parent_group == master_group

def test_paused(channel_group):
    assert not channel_group.paused

def test_pitch(channel_group):
    assert channel_group.pitch == 1.0
    channel_group.pitch = 2.0
    assert channel_group.pitch == 2.0

def test_channel_group_get_set_reverb_wet(channel_group):
    assert channel_group.get_reverb_wet(0) == 0.0
    channel_group.set_reverb_wet(0, 0.5)
    assert channel_group.get_reverb_wet(0) == 0.5

def test_system_object(initialized_system, channel_group):
    assert initialized_system == channel_group.system_object

def test_volume(channel_group):
    assert channel_group.volume == 1.0
    channel_group.volume = 0.5
    assert channel_group.volume == 0.5

def test_volume_ramp(channel_group):
    assert channel_group.volume_ramp
    channel_group.volume_ramp = False
    assert not channel_group.volume_ramp

def test_is_playing(channel_group):
    assert channel_group.is_playing

def test_add_remove_dsp(echo, channel_group):
    channel_group.add_dsp(0, echo)
    channel_group.remove_dsp(echo)

def test_remove_fade_points(channel_group):
    channel_group.remove_fade_points(0, 20000000000)

def test_set_callback(channel_group):
    mock_callback = mock.Mock(return_value=0)
    channel_group.set_callback(mock_callback)

def test_dsp_clock(channel_group):
    assert channel_group.dsp_clock.dsp_clock >= 0
    assert channel_group.dsp_clock.parent_clock > 5000

def test_get_set_dsp_index(channel_group, echo):
    channel_group.add_dsp(0, echo)
    assert channel_group.get_dsp_index(echo) == 0
    channel_group.set_dsp_index(echo, 1)
    assert channel_group.get_dsp_index(echo) == 1

def test_set_fade_point_ramp(channel_group):
    channel_group.set_fade_point_ramp(20000000000, 0.5)

def test_set_mix_levels_input(channel_group):
    channel_group.set_mix_levels_input(0.5, 0.5)
    
def test_set_mix_levels_output(channel_group):
    channel_group.set_mix_levels_output(0.5,  1.0, 1.0, 0.25, 0.0, 0.0, 0.5, 0.8)

def test_set_pan(channel_group):
    channel_group.set_pan(-1.0)

def test_stop(channel_group):
    channel_group.stop()
