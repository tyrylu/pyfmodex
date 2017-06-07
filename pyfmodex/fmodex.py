from ctypes import *
import os, platform
arch = platform.architecture()[0]
if os.name == 'nt':
    if arch == "32bit":
        _dll = windll.fmod
    else:
        _dll = windll.fmod64
elif os.name == "posix":
    if arch == "32bit":
        _dll = CDLL('libfmod.so')
    else:
        _dll = CDLL('libfmod64.so')
from . import globalvars
globalvars.dll = _dll
from .callback_prototypes import DEBUG_CALLBACK
from .utils import ckresult
from .structobject import Structobject as so

def get_disk_busy():
    """Gets the busy status of the disk.
    :returns: Whether the disk is busy.
    :rtype: boolean
    """
    busy = c_int()
    ckresult(_dll.FMOD_File_GetDiskBusy(byref(busy)))
    return busy.value

def set_disk_busy(busy):
    """Sets the busy status.
    :param busy: The busy status.
    :type busy: boolean
"""
    ckresult(_dll.FMOD_File_SetDiskBusy(busy))

def get_memory_stats(blocking):
    """Returns the current memory stats.
    :param blocking: Gather more accurate stats, but perhaps don't return inmediately.
    :type blocking: boolean
    :returns: A StructObject with the values current and maximum.
    """
    current = c_int()
    max = c_int()
    ckresult(_dll.FMOD_Memory_GetStats(byref(current), byref(max), blocking))
    return so(current=current.value, maximum=max.value)

def initialize_memory(poolmem, poollen, useralloc, userrealloc, userfree, memtypeflags):
    """Initialize fmod memory routines.
    :param poolmem: A custom preallocated memory pool.
    :type poolmem: c_void_p
    :param poollen: The size of the pool.
    :type poollen: int
    :param useralloc: A custom allocation function.
    :type useralloc: function having a malloc like behavior and signature.
    :param userrealloc: A custom reallocation function.
    :type userrealloc: function having a realloc like behavior and signature.
    :param userfree: A custom memory freeing function.
    :type userfree: function having a free like behavior and signature.
    :param memtypeflags: The types of memory this configuration applies to.
    :type memtypeflags: MEMORY_FLAGS"""
    ckresult(_dll.FMOD_Memory_Initialize(poolmem, poollen, useralloc, userrealloc, userfree, memtypeflags))
    
def initialize_debugging(flags, mode, callback, filename):
    """Initializes the logging system.
    :param flags: The debug output control flags.
    :type flags: DEBUG_FLAGS
    :param mode: The output type.
    :type mode: DEBUG_MODE
    :param callback: Debugging callback, if applicable.
    :type callback: DEBUG_CALLBACK like function
    :param filename: The file to log to, if applicable.
    :param filename: str"""
    ckresult(_dll.FMOD_Debug_Initialize(flags, mode, DEBUG_CALLBACK(callback), filename))