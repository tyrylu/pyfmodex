import os
from ctypes import *
from .structure_declarations import *

if os.name == "nt":
    func = WINFUNCTYPE
else:
    func = CFUNCTYPE

DSP_ALLOC_FUNC = func(c_void_p, c_uint, c_int, c_char_p)
DSP_REALLOC_FUNC = func(c_void_p, c_void_p, c_uint, c_int, c_char_p)
DSP_FREE_FUNC = func(None, c_void_p, c_int, c_char_p)
DSP_LOG_FUNC = func(None, c_int, c_char_p, c_int, c_char_p, c_char_p, c_void_p) # I hope the varargs semantics are correct
DSP_GETSAMPLERATE_FUNC = func(c_int, POINTER(DSP_STATE), POINTER(c_int))
DSP_GETBLOCKSIZE_FUNC = func(c_int, POINTER(DSP_STATE), POINTER(c_uint))
DSP_GETSPEAKERMODE_FUNC = func(c_int, POINTER(DSP_STATE), POINTER(c_int), POINTER(c_int))
DSP_GETCLOCK_FUNC = func(c_int, POINTER(DSP_STATE), POINTER(c_ulonglong), POINTER(c_int), POINTER(c_int))
DSP_GETLISTENERATTRIBUTES_FUNC = func(c_int, POINTER(DSP_STATE), POINTER(c_int), POINTER(THREED_ATTRIBUTES))
DSP_GETUSERDATA_FUNC = func(c_int, POINTER(DSP_STATE), POINTER(c_void_p))
DSP_DFT_FFTREAL_FUNC = func(c_int, POINTER(DSP_STATE), c_int, POINTER(c_float), POINTER(COMPLEX), POINTER(c_float), c_int)
DSP_DFT_IFFTREAL_FUNC = func(c_int, POINTER(DSP_STATE), c_int, POINTER(COMPLEX), POINTER(c_float), POINTER(c_float), c_int)
DSP_PAN_SUMMONOMATRIX_FUNC = func(c_int, POINTER(DSP_STATE), c_int, c_float, c_float, POINTER(c_float))
DSP_PAN_SUMSTEREOMATRIX_FUNC = func(c_int, POINTER(DSP_STATE), c_int, c_float, c_float, c_float, c_int, POINTER(c_float))
DSP_PAN_SUMSURROUNDMATRIX_FUNC = func(c_int, POINTER(DSP_STATE), c_int, c_int, c_float, c_float, c_float, c_float, c_float, c_int, POINTER(c_float), c_int)
DSP_PAN_SUMMONOTOSURROUNDMATRIX_FUNC = func(c_int, POINTER(DSP_STATE), c_int, c_float, c_float, c_float, c_float, c_int, POINTER(c_float))
DSP_PAN_SUMSTEREOTOSURROUNDMATRIX_FUNC = func(c_int, POINTER(DSP_STATE), c_int, c_float, c_float, c_float, c_float, c_float, c_int, POINTER(c_float))
DSP_PAN_GETROLLOFFGAIN_FUNC = func(c_int, POINTER(DSP_STATE), c_int, c_float, c_float, c_float, c_float)
FILE_ASYNCDONE_FUNC = func(c_int, POINTER(ASYNCREADINFO), c_int)
OUTPUT_READFROMMIXER = func(c_int, POINTER(OUTPUT_STATE), c_void_p, c_uint)
OUTPUT_COPYPORT = func(c_int, POINTER(OUTPUT_STATE), c_int, c_void_p, c_uint)
OUTPUT_ALLOC = func(c_void_p, c_uint, c_uint, c_char_p, c_int)
OUTPUT_FREE = func(None, c_void_p, c_char_p, c_int)
OUTPUT_LOG = func(None, c_int, c_char_p, c_int, c_char_p, c_char_p, c_void_p) # Varargs, again
