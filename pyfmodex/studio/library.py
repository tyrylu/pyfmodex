"""Util method to get the FMOD LIBRARY from the filesystem into ctypes."""

import os
import platform

arch = platform.architecture()[0]
if os.name == "nt":
    from ctypes import windll
    library_type = windll
    LIBRARY_NAME = "fmodstudio"
elif os.name == "posix":
    from ctypes import cdll
    library_type = cdll
    LIBRARY_NAME = "libfmodstudio.so"

LIBRARY = None


def get_library():
    """Load libary file according to architecture's ctype method."""
    global LIBRARY
    if not LIBRARY:
        LIBRARY = library_type.LoadLibrary(LIBRARY_NAME)
    return LIBRARY
