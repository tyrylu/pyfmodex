class FmodError(Exception):
    def __init__(self, errcode):
        self.errcode = errcode

    def __str__(self):
        return "Fmod error, code %i"%self.errcode


def ckresult(result):
    if result != 0:
        raise FmodError(result)