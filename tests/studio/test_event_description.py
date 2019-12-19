def test_path(event):
    assert event.path == "event:/Vehicles/Car Engine"

def test_create_instance(event):
    inst = event.create_instance()
    assert inst.is_valid

def test_parameter_description_count(event):
    assert event.parameter_description_count == 8

def test_user_property_count(event):
    assert event.user_property_count == 0