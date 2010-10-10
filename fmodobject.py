from ctypes import *
from globalvars import dll as _dll

class FmodObject(object):
    def __init__(self, ptr):
        self._ptr = ptr