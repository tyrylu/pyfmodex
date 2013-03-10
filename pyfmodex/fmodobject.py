from ctypes import *
from utils import *
from globalvars import dll as _dll
from structobject import Structobject as so

class FmodObject(object):
    def __init__(self, ptr):
        self._ptr = ptr

    def _call_fmod(self, funcname, *args):
        result = getattr(_dll, funcname)(self._ptr, *args)
        if result != 0:
            raise FmodError(result)
