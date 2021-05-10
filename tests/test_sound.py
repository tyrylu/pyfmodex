import pytest
from pyfmodex.enums import SOUND_TYPE, SOUND_FORMAT, OPENSTATE, RESULT, TIMEUNIT
from pyfmodex.flags import MODE
from pyfmodex.exceptions import FmodError

def test_add_delete_syncpoint(sound):
    point = sound.add_sync_point(1, TIMEUNIT.MS, "test")
    assert point > 0
    sound.delete_sync_point(point)

def test_threed_cone_settings(sound):
    settings = sound.threed_cone_settings
    assert settings.outside_angle == 360
    settings.inside_angle = 90
    assert settings.inside_angle == 90

def test_custom_rolloff(sound):
    assert sound.custom_rolloff == []
    curve = [[0,1,0],[3,0.5,0]]
    sound.custom_rolloff = curve
    assert sound.custom_rolloff == curve
    sound.custom_rolloff = []

def test_min_distance(sound):
    assert sound.min_distance == 1.0
    sound.min_distance = 2.0
    assert sound.min_distance == 2.0

def test_max_distance(sound):
    assert sound.max_distance == 10000
    sound.max_distance = 20000
    assert sound.max_distance == 20000

def test_default_frequency(sound):
    assert sound.default_frequency == 44100
    sound.default_frequency = 22050
    assert sound.default_frequency == 22050

def test_default_priority(sound):
    assert sound.default_priority == 128
    sound.default_priority = 129
    assert sound.default_priority == 129

def test_format(sound):
    format = sound.format
    assert format.type is SOUND_TYPE.FSB
    assert format.channels == 1
    assert format.bits == 0
    assert format.format is SOUND_FORMAT.NONE

def test_get_length(sound):
    assert sound.get_length(TIMEUNIT.MS) == 0
    assert sound.get_subsound(0).get_length(TIMEUNIT.MS) == 32838

def test_loop_count(sound):
    assert sound.loop_count == -1
    sound.loop_count = 2
    assert sound.loop_count == 2

def test_loop_points(sound):
    sound.get_subsound(0).set_loop_points(0, TIMEUNIT.MS, 60, TIMEUNIT.MS)
    assert sound.get_subsound(0).get_loop_points(TIMEUNIT.MS, TIMEUNIT.MS) == (0, 60)

def test_mode(sound):
    assert sound.mode is MODE.THREED
    new_mode = MODE.THREED|MODE.LOOP_NORMAL
    sound.mode = new_mode
    assert sound.mode == new_mode



def test_num_music_channels(midi_sound):
    assert midi_sound.num_music_channels == 13

def test_set_get_music_channel_volume(midi_sound):
    midi_sound.set_music_channel_volume(1, 0.5)
    assert midi_sound.get_music_channel_volume(1) == 0.5

def test_name(sound):
    assert sound.name == b"test.fsb"

def test_num_subsounds(sound):
    assert sound.num_subsounds == 2

def test_num_sync_points(sound):
    assert sound.num_sync_points == 0

def test_num_tags(sound):
    assert sound.num_tags.tags == 0
    assert sound.num_tags.updated_tags == 0

def test_open_state(sound):
    state = sound.open_state
    assert state.state is OPENSTATE.READY
    assert state.percent_buffered == 0
    assert not state.starving

def test_sound_group(sound, system):
    group = system.create_sound_group("test group")
    sound.sound_group = group
    assert sound.sound_group._ptr.value == group._ptr.value

def test_subsound_and_parent(sound):
    subsound = sound.get_subsound(1)
    assert subsound.subsound_parent._ptr.value == sound._ptr.value

def test_get_syncpoint(sound):
    point = sound.add_sync_point(0, TIMEUNIT.MS, "foo")
    assert sound.get_sync_point(0) == point

def test_get_sync_point_info(sound):
    
    point = sound.add_sync_point(42, TIMEUNIT.MS, "foobar")
    info = sound.get_sync_point_info(point, TIMEUNIT.MS)
    assert info.name == b"foobar"
    assert info.offset == 41
    assert sound.get_sync_point_info(point, TIMEUNIT.PCM).offset == 1852

def test_system_object(sound):
    assert sound.system_object

def test_lock_unlock(sound):
    ret = sound.get_subsound(0).lock(0, 16)
    sound.get_subsound(0).unlock(ret[0], ret[1])

def test_music_speed(midi_sound):
    assert midi_sound.music_speed == 1.0
    midi_sound.music_speed = 0.5
    assert midi_sound.music_speed == 0.5

def test_read_data(sound):
    """We should probably write a proper test for this."""
    with pytest.raises(FmodError) as ex:
        data, length = sound.get_subsound(0).read_data(20)
        assert ex.result is RESULT.UNSUPPORTED

