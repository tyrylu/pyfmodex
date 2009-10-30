import os
from ctypes import *
if os.name == "nt":
    THREED_ROLLOFCALLBACK = WINFUNCTYPE(c_float, c_int, c_float)
    CHANNEL_CALLBACK = WINFUNCTYPE(c_int, c_int, c_int, c_void_p, c_void_p)
    FILE_CLOSECALLBACK = WINFUNCTYPE(c_int, c_void_p, c_void_p)
    FILE_OPENCALLBACK = WINFUNCTYPE(c_int, c_char_p, c_int, c_uint, c_void_p, c_void_p)
    FILE_READCALLBACK = WINFUNCTYPE(c_int, c_void_p, c_void_p, c_uint, c_uint, c_void_p)
    FILE_SEEKCALLBACK = WINFUNCTYPE(c_int, c_void_p, c_uint, c_void_p)
    SOUND_NONBLOCKCALLBACK = WINFUNCTYPE(c_int, c_int, c_int)
    SOUND_PCMREADCALLBACK = WINFUNCTYPE(c_int, c_int, c_void_p, c_uint)
    SOUND_PCMSETPOSCALLBACK = WINFUNCTYPE(c_int, c_int, c_int, c_uint, c_int)
else:
    THREED_ROLLOFCALLBACK = CFUNCTYPE(c_float, c_int, c_float)
    CHANNEL_CALLBACK = CFUNCTYPE(c_int, c_int, c_int, c_void_p, c_void_p)
    FILE_CLOSECALLBACK = CFUNCTYPE(c_int, c_void_p, c_void_p)
    FILE_OPENCALLBACK = CFUNCTYPE(c_int, c_char_p, c_int, c_uint, c_void_p, c_void_p)
    FILE_READCALLBACK = CFUNCTYPE(c_int, c_void_p, c_void_p, c_uint, c_uint, c_void_p)
    FILE_SEEKCALLBACK = CFUNCTYPE(c_int, c_void_p, c_uint, c_void_p)
    SOUND_NONBLOCKCALLBACK = CFUNCTYPE(c_int, c_int, c_int)
    SOUND_PCMREADCALLBACK = CFUNCTYPE(c_int, c_int, c_void_p, c_uint)
    SOUND_PCMSETPOSCALLBACK = CFUNCTYPE(c_int, c_int, c_int, c_uint, c_int)
  
     