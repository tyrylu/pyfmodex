from ctypes import *
import os
if os.name == 'nt':
    _dll = windll.fmodex
else:
    _dll = CDLL('libfmodex.so')
from . import globalvars
globalvars.dll = _dll
from .utils import ckresult
from .structobject import Structobject as so

def get_debug_level():
    level = c_int()
    ckresult(_dll.FMOD_Debug_GetLevel(byref(level)))
    return level.value

def set_debug_level(level):
    ckresult(_dll.FMOD_Debug_SetLevel(level))

def get_disk_busy():
    busy = c_int()
    ckresult(_dll.FMOD_File_GetDiskBusy(byref(busy)))
    return busy.value

def set_disk_busy(busy):
    ckresult(_dll.FMOD_File_SetDiskBusy(busy))

def get_memory_stats(blocking):
    current = c_int()
    max = c_int()
    ckresult(_dll.FMOD_Memory_GetStats(byref(current), byref(max), blocking))
    return so(current=current.value, maximum=max.value)

