from ctypes import c_void_p, byref
from ..flags import INIT_FLAGS
from ..utils import prepare_str, ckresult
from .. import System
from .studio_object import StudioObject
from .flags import STUDIO_INIT_FLAGS, LOAD_BANK_FLAGS
from .bank import Bank
from .event_description import EventDescription
from .library import get_library

class StudioSystem(StudioObject):
    function_prefix = "FMOD_Studio_System"
    
    def __init__(self, ptr=None, create=True, version=0x00011002):
        """If create is True, new instance is created. Otherwise ptr must be a valid pointer."""
        super().__init__(ptr)
        self._system_callbacks = {}
        if create:
            self._ptr = c_void_p()
            ckresult(get_library().FMOD_Studio_System_Create(byref(self._ptr), version))
        else:
            self._ptr = ptr

    def initialize(self, max_channels=1000, studio_flags=STUDIO_INIT_FLAGS.NORMAL, flags=INIT_FLAGS.NORMAL, extra=None):
        print(extra)
        self._call("Initialize", max_channels, int(studio_flags), int(flags), extra)

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