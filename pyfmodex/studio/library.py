import os
import platform
from ctypes import cdll, windll

arch = platform.architecture()[0]
if os.name == 'nt':
    library_type = windll
    if arch == "32bit":
        library_name = "fmodstudio"
    else:
        library_name = "fmodstudio64"
elif os.name == "posix":
    library_type = cdll
    if arch == "32bit":
        library_name = "libfmodstudio.so"
    else:
        library_name = "libfmodstudio64.so"

library = None
def get_library():
    global library
    if not library:
        library = library_type.LoadLibrary(library_name)
    return library