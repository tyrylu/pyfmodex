class FmodError(Exception):
    def __init__(self, errcode):
        self.errcode = errcode

    def __str__(self):
        return "Fmod error, code %i"%self.errcode

def ckresult(result):
    if result != 0:
        raise FmodError(result)

def LOWORD(long):
    return long&0xFFFF
 
def HIWORD(long):
    return long>>16

def MAKELONG(lo,hi):
    return (hi<<16)+lo

def check_type(obj, cls, msg="Bad type of passed argument (%s), expected %s"):
    if not isinstance(obj, cls): raise TypeError(msg%(str(type(obj)),str(cls)))