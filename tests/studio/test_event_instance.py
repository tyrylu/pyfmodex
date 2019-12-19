from pyfmodex.studio.enums import PLAYBACK_STATE

def test_start(instance):
    instance.start()
    instance.stop()

def test_paused(instance):
    assert not instance.paused
    instance.paused = True
    assert instance.paused

def test_playback_state(event):
    assert event.create_instance().playback_state is PLAYBACK_STATE.STOPPED

def test_stop(instance):
    instance.stop()

def test_get_parameter_by_name(instance):
    value, actual = instance.get_parameter_by_name("rpm")
    assert value == 0.0
    assert actual == 0.0

def test_set_parameter_by_name(instance):
    instance.set_parameter_by_name("rpm", 8000)
    val, actual = instance.get_parameter_by_name("rpm")
    assert val == 8000.0
    assert actual == 0.0

def test_channel_group(instance):
    group = instance.channel_group