from ctypes import c_void_p, c_int, byref
from ..flags import INIT_FLAGS
from ..utils import prepare_str, ckresult, check_type
from .. import System
from .studio_object import StudioObject
from .flags import STUDIO_INIT_FLAGS, LOAD_BANK_FLAGS
from .structures import ADVANCEDSETTINGS, BUFFER_USAGE
from .bank import Bank
from .event_description import EventDescription
from .library import get_library
from .utils import fmod_version


class StudioSystem(StudioObject):
    function_prefix = "FMOD_Studio_System"

    def __init__(self, ptr=None, create=True, version=None):
        """If create is True, new instance is created. Otherwise ptr must be a valid pointer."""
        super().__init__(ptr)
        self._system_callbacks = {}
        if create:
            if not version:
                version = fmod_version()
            self._ptr = c_void_p()
            ckresult(get_library().FMOD_Studio_System_Create(byref(self._ptr), version))
        else:
            self._ptr = ptr

    @property
    def advanced_settings(self):
        settings = ADVANCEDSETTINGS()
        self._call("GetAdvancedSettings", byref(settings))
        return settings

    @advanced_settings.setter
    def advanced_settings(self, value):
        check_type(value, ADVANCEDSETTINGS)
        self._call("SetAdvancedSettings", byref(value))

    def get_bank(self, path):
        path = prepare_str(path)
        ptr = c_void_p()
        self._call("GetBank", path, byref(ptr))
        return Bank(ptr)

    @property
    def bank_count(self):
        count = c_int()
        self._call("GetBankCount", byref(count))
        return count.value

    @property
    def banks(self):
        array = (c_void_p * self.bank_count)()
        self._call("GetBankList", byref(array), len(array), None)
        return [Bank(ptr) for ptr in array]

    @property
    def buffer_usage(self):
        usage = BUFFER_USAGE()
        self._call("GetBufferUsage", byref(usage))
        return usage

    def initialize(
        self,
        max_channels=1000,
        studio_flags=STUDIO_INIT_FLAGS.NORMAL,
        flags=INIT_FLAGS.NORMAL,
        extra=None,
    ):
        self._call("Initialize", max_channels, int(studio_flags), int(flags), extra)

    def release(self):
        self._call("Release")

    def flush_commands(self):
        self._call("FlushCommands")

    def flush_sample_loading(self):
        self._call("FlushSampleLoading")

    def load_bank_file(self, filename, flags=LOAD_BANK_FLAGS.NORMAL):
        filename = prepare_str(filename)
        bank_ptr = c_void_p()
        self._call("LoadBankFile", filename, int(flags), byref(bank_ptr))
        return Bank(bank_ptr)

    def update(self):
        self._call("Update")

    @property
    def low_level_system(self):
        system_ptr = c_void_p()
        self._call("GetLowLevelSystem", byref(system_ptr))
        return System(system_ptr)

    def get_event(self, path):
        ptr = c_void_p()
        self._call("GetEvent", prepare_str(path), byref(ptr))
        return EventDescription(ptr)
