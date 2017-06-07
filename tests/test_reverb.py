def test_position(reverb):
    assert reverb.position == [0.0, 0.0, 0.0]
    new = [1.0, 2.0, 3.0]
    reverb.position = new
    assert reverb.position == new

def test_min_distance(reverb):
    assert reverb.min_distance == 0.0
    # Note that setting the min distance was ignored by fmod.

def test_max_distance(reverb):
    assert reverb.max_distance == 0.0
    reverb.max_distance = 10.0
    assert reverb.max_distance == 10.0

def test_active(reverb):
    assert reverb.active
    reverb.active = False
    assert not reverb.active

def test_properties(reverb):
    props = reverb.properties
    assert props.EarlyDelay == 7.0
    props.EarlyDelay = 5.0
    reverb.properties = props
    assert reverb.properties.EarlyDelay == 5.0

def test_release(reverb):
    reverb.release()