import sys
from .enums import RESULT
from .exceptions import FmodError


def ckresult(result):
    result = RESULT(result)
    if result is not RESULT.OK:
        raise FmodError(result)

def check_type(obj, cls, msg="Bad type of passed argument (%s), expected %s"):
    if not isinstance(obj, cls): raise TypeError(msg%(str(type(obj)),str(cls)))
    
def prepare_str(string, encoding=sys.getfilesystemencoding()):
    if hasattr(string, "encode"):
        return string.encode(encoding)