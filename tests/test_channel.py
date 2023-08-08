import os
from unittest import mock

from pyfmodex.enums import CHANNELCONTROL_DSP_INDEX, DSP_TYPE, TIMEUNIT
from pyfmodex.flags import MODE


def test_add_dsp(echo, channel):
    channel.add_dsp(0, echo)


def test_add_fade_point(channel):
    channel.add_fade_point(40000000000, 0.5)


def test_threed_attrs(channel):
    zero = [0.0, 0.0, 0.0]
    ones = [1.0, 1.0, 1.0]
    assert channel.position == zero
    assert channel.velocity == zero
    channel.position = ones
    channel.velocity = ones
    assert channel.position == ones
    assert channel.velocity == ones


def test_cone_orientation(channel):
    assert channel.cone_orientation == [0.0, 0.0, 1.0]
    channel.cone_orientation = [0.0, 1.0, 1.0]
    assert channel.cone_orientation == [0.0, 1.0, 1.0]


def test_cone_settings(channel):
    settings = channel.cone_settings
    assert settings.outside_angle == 360.0


def test_custom_rolloff(channel):
    new_curve = [[1.0, 0.5, 0.0], [4.0, 0.0, 0.0]]
    assert channel.custom_rolloff == []
    channel.custom_rolloff = new_curve
    assert channel.custom_rolloff == new_curve
    
    
def test_threed_distance_filter(channel):
    settings = channel.threed_distance_filter
    assert not settings.custom
    settings.custom = True
    settings.custom_level = 0.5
    channel.threed_distance_filter = settings
    assert channel.threed_distance_filter.custom


def test_doppler_level(channel):
    assert channel.doppler_level == 1.0
    channel.doppler_level = 0.5
    assert channel.doppler_level == 0.5


def test_level(channel):
    assert channel.level == 1.0
    channel.level = 0.5
    assert channel.level == 0.5


def test_min_max_distance(channel):
    assert channel.min_distance == 1.0
    assert channel.max_distance == 10000.0
    channel.min_distance = 2.0
    assert channel.min_distance == 2.0


def test_occlusion(channel):
    assert channel.direct_occlusion == 0.0
    assert channel.reverb_occlusion == 0.0
    channel.direct_occlusion = 0.5
    assert channel.direct_occlusion == 0.5


def test_spread(channel):
    assert channel.threed_spread == 0.0
    channel.threed_spread = 0.5
    assert channel.threed_spread == 0.5


def test_audibility(channel):
    assert channel.audibility >= 0.0 and channel.audibility <= 1.0


def test_channel_group(channel, initialized_system):
    group = initialized_system.create_channel_group("test_group422")
    # channel.channel_group = group # Setting breaks some other tests
    assert (
        channel.channel_group._ptr.value
        == initialized_system.master_channel_group._ptr.value
    )  # Ideally, it would be checked with the new group


def test_current_sound(channel):
    assert channel.current_sound.name == b"Ring"


def test_get_dsp(channel, initialized_system):
    dsp = initialized_system.create_dsp_by_type(DSP_TYPE.ECHO)
    channel.add_dsp(0, dsp)
    assert channel.get_dsp(0)._ptr.value == dsp._ptr.value


def test_delay(channel):
    delay = channel.delay
    assert delay.dsp_start == 0
    delay.dsp_end = 20000000000
    channel.delay = delay
    assert channel.delay.dsp_end == 20000000000


def test_fade_points(channel):
    channel.add_fade_point(200, 0.25)
    channel.add_fade_point(2000, 0.5)
    assert channel.fade_points == ([200, 2000], [0.25, 0.5])


def test_frequency(channel):
    assert channel.frequency == 44100
    channel.frequency = 48000
    assert channel.frequency == 48000


def test_index(channel):
    assert channel.index == 999


def test_loop_count(channel):
    assert channel.loop_count == -1
    channel.loop_count = 1
    assert channel.loop_count == 1


def test_loop_points(channel):
    channel.set_loop_points(0, TIMEUNIT.MS, 60, TIMEUNIT.MS)
    assert channel.get_loop_points(TIMEUNIT.MS, TIMEUNIT.MS) == (0, 60)


def test_low_pass_gain(channel):
    assert channel.low_pass_gain == 1.0
    channel.low_pass_gain = 0.5
    assert channel.low_pass_gain == 0.5


def test_mix_matrix(channel):
    assert channel.get_mix_matrix() == []
    matrix = [0.5, 0.5]
    channel.set_mix_matrix(matrix, 1, 2)
    assert channel.get_mix_matrix() == matrix


def test_mode(channel):
    assert channel.mode == MODE.THREED | MODE.LOOP_OFF
    new_mode = MODE.LOOP_NORMAL
    channel.mode = new_mode
    assert channel.mode == new_mode | MODE.THREED


def test_mute(channel):
    assert not channel.mute
    channel.mute = True
    assert channel.mute


def test_num_dsps(channel):
    assert channel.num_dsps == 1


def test_paused(channel):
    assert channel.paused


def test_pitch(channel):
    assert channel.pitch == 1.0
    channel.pitch = 2.0
    assert channel.pitch == 2.0


def test_get_position(channel):
    assert channel.get_position(TIMEUNIT.MS) == 0


def test_priority(channel):
    assert channel.priority == 128
    channel.priority = 2
    assert channel.priority == 2


def test_channel_get_set_reverb_wet(channel):
    assert channel.get_reverb_wet(0) == 1.0
    channel.set_reverb_wet(0, 0.5)
    assert channel.get_reverb_wet(0) == 0.5


def test_system_object(initialized_system, channel):
    assert initialized_system._ptr.value == channel.system_object._ptr.value


def test_volume(channel):
    assert channel.volume == 1.0
    channel.volume = 0.5
    assert channel.volume == 0.5


def test_volume_ramp(channel):
    assert channel.volume_ramp
    channel.volume_ramp = False
    assert not channel.volume_ramp


def test_is_playing(channel):
    assert channel.is_playing


def test_is_virtual(channel):
    assert not channel.is_virtual


def test_add_remove_dsp(echo, channel):
    channel.add_dsp(0, echo)
    channel.remove_dsp(echo)


def test_remove_fade_points(channel):
    channel.remove_fade_points(0, 20000000000)


def test_set_callback(channel):
    mock_callback = mock.Mock(return_value=0)
    channel.set_callback(mock_callback)


def test_dsp_clock(channel):
    assert channel.dsp_clock.dsp_clock == 0
    assert channel.dsp_clock.parent_clock > 5000


def test_get_set_dsp_index(channel, echo):
    channel.add_dsp(0, echo)
    assert channel.get_dsp_index(echo) == 0
    channel.set_dsp_index(echo, 1)
    assert channel.get_dsp_index(echo) == 1


def test_set_fade_point_ramp(channel):
    channel.set_fade_point_ramp(20000000000, 0.5)


def test_set_mix_levels_input(channel):
    channel.set_mix_levels_input(0.5, 0.5)


def test_set_mix_levels_output(many_speakers_system):
    many_speakers_system.init()
    snd = many_speakers_system.create_sound(
        os.path.join(os.path.dirname(__file__), "test.fsb")
    )
    channel = snd.get_subsound(0).play(paused=True)
    channel.set_mix_levels_output(0.5, 1.0, 1.0, 0.25, 0.0, 0.0, 0.5, 0.125)
    print(channel.get_mix_matrix())


def test_set_pan(channel):
    channel.set_pan(-1.0)


def test_stop(channel):
    channel.stop()

def test_set_position(channel):
    channel.set_position(0, TIMEUNIT.MS)