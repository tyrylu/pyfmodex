import os
import platform
from ctypes import cdll, windll

arch = platform.architecture()[0]
if os.name == 'nt':
    library_type = windll
    library_name = "fmodstudio"
elif os.name == "posix":
    library_type = cdll
    library_name = "libfmodstudio.so"
                                            
library = None
def get_library():
    global library
    if not library:
        library = library_type.LoadLibrary(library_name)
    return library