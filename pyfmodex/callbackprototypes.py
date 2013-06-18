import os
from ctypes import *

from .structures import ASYNCREADINFO

if os.name == "nt":
    func = WINFUNCTYPE
else:
    func = CFUNCTYPE

ROLLOFF_CALLBACK = func(c_float, c_int, c_float)
CHANNEL_CALLBACK = func(c_int, c_int, c_int, c_void_p, c_void_p)
FILE_ASYNCCANCELCALLBACK = func(c_int, c_void_p, c_void_p)
FILE_ASYNCREADCALLBACK = func(c_int, POINTER(ASYNCREADINFO), c_void_p)
FILE_CLOSECALLBACK = func(c_int, c_void_p, c_void_p)
FILE_OPENCALLBACK = func(c_int, c_char_p, c_int, c_uint, c_void_p, c_void_p)
FILE_READCALLBACK = func(c_int, c_void_p, c_void_p, c_uint, c_uint, c_void_p)
FILE_SEEKCALLBACK = func(c_int, c_void_p, c_uint, c_void_p)
SOUND_NONBLOCKCALLBACK = func(c_int, c_int, c_int)
SOUND_PCMREADCALLBACK = func(c_int, c_int, c_void_p, c_uint)
SOUND_PCMSETPOSCALLBACK = func(c_int, c_int, c_int, c_uint, c_int)
SYSTEM_CALLBACK = func(c_int, c_int, c_int)
