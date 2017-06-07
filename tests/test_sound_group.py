from pyfmodex.enums import SOUNDGROUP_BEHAVIOR

def test_max_audible(sound_group):
    assert sound_group.max_audible == -1
    sound_group.max_audible = 5
    assert sound_group.max_audible == 5

def test_max_audible_behavior(sound_group):
    new_behavior = SOUNDGROUP_BEHAVIOR.MUTE
    assert sound_group.max_audible_behavior is SOUNDGROUP_BEHAVIOR.FAIL
    sound_group.max_audible_behavior = new_behavior
    assert sound_group.max_audible_behavior is new_behavior

def test_mute_fade_speed(sound_group):
    assert sound_group.mute_fade_speed == 0.0
    sound_group.mute_fade_speed = 0.5
    assert sound_group.mute_fade_speed == 0.5

def test_name(sound_group):
    assert sound_group.name == b"test group"

def test_num_playing(sound_group):
    assert sound_group.num_playing == 0

def test_num_sounds(sound_group):
    assert sound_group.num_sounds == 0

def test_get_sound(sound, sound_group):
    sound.sound_group = sound_group
    assert sound_group.get_sound(0) == sound

def test_system_object(initialized_system, sound_group):
    assert sound_group.system_object == initialized_system

def test_volume(sound_group):
    assert sound_group.volume == 1.0
    sound_group.volume = 0.5
    assert sound_group.volume == 0.5

def test_release(sound_group):
    sound_group.release()

def test_stop(sound_group):
    sound_group.stop()