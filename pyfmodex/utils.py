import sys
from . import constants
#Generate mapping from fmod ex error codes to their enum names which are enough for somethink like basic meaning.
errmembers = [str(m) for m in dir(constants) if str(m).startswith("FMOD_ERR")]
#Use dict, so we arn't dependent on the order in which we'll found them.
errors_mapping = {}
for member in errmembers:
    val = getattr(constants, member)
    errors_mapping[val] = member.replace("_", " ")

class FmodError(Exception):
    def __init__(self, errcode):
        self.errcode = errcode
        self.msg = errors_mapping[errcode]

    def __str__(self):
        return self.msg



def ckresult(result):
    if result != 0:
        raise FmodError(result)


def LOWORD(long):
    return int&0xFFFF
 
def HIWORD(long):
    return int>>16

def MAKELONG(lo,hi):
    return (hi<<16)+lo

def check_type(obj, cls, msg="Bad type of passed argument (%s), expected %s"):
    if not isinstance(obj, cls): raise TypeError(msg%(str(type(obj)),str(cls)))
    
def prepare_str(string, encoding=sys.getfilesystemencoding()):
    if hasattr(string, "encode"):
        return string.encode(encoding)