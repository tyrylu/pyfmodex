from ctypes import *
from utils import *
from globalvars import dll as _dll
from structobject import Structobject as so

class FmodObject(object):
    def __init__(self, ptr):
        self._ptr = ptr