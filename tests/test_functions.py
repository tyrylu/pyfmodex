import pyfmodex

def test_get_set_disk_busy(initialized_system):
    assert not pyfmodex.get_disk_busy()
    pyfmodex.set_disk_busy(1)
    assert pyfmodex.get_disk_busy()
    pyfmodex.set_disk_busy(0)

def test_get_memory_stats(initialized_system):
    stats = pyfmodex.get_memory_stats(True)
    assert stats.current > 0
    assert stats.maximum > 0