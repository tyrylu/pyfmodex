import os

BANK_FILE = os.path.join(os.path.dirname(__file__), "..", "Vehicles.bank")

def test_initialize(studio_system):
    studio_system.initialize()

def test_flush_commands(initialized_studio_system):
    initialized_studio_system.flush_commands()

def test_flush_sample_loading(initialized_studio_system):
    initialized_studio_system.flush_sample_loading()

def test_advanced_settings(studio_system):
    settings = studio_system.advanced_settings
    assert settings.commandqueuesize == 32768
    # Note that if the size below is set to something which is not divisible by 2, it gets rounded up.
    settings.commandqueuesize = 65536
    settings.encryptionkey = b"FooBar"
    studio_system.advanced_settings = settings
    assert studio_system.advanced_settings.commandqueuesize == 65536


def test_get_bank(system_with_banks):
    bank = system_with_banks.get_bank("bank:/Vehicles")
    assert bank.event_count == 1

def test_bank_count(system_with_banks):
    assert system_with_banks.bank_count == 3

def test_banks(system_with_banks):
    banks = system_with_banks.banks
    assert len(banks) == 3
    assert banks[2].event_count == 1

def test_buffer_usage(initialized_studio_system):
    usage = initialized_studio_system.buffer_usage
    assert usage.studiohandle.peakusage == 0

def test_update(system_with_banks):
    system_with_banks.update()

def test_load_bank_file(initialized_studio_system):
    bank = initialized_studio_system.load_bank_file(BANK_FILE)
    assert bank.event_count == 1

def test_event(system_with_banks):
    assert system_with_banks.get_event("event:/Vehicles/Car Engine").path == "event:/Vehicles/Car Engine"