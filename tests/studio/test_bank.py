def test_event_count(bank):
    assert bank.event_count == 1

def test_events(bank):
    events = bank.events
    assert len(events) == 1
    assert events[0].path == "event:/Vehicles/Car Engine"