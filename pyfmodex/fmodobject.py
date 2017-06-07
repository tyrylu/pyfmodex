from .globalvars import dll as _dll
from .enums import RESULT
from .exceptions import FmodError

class FmodObject(object):
    """A base Fmod ex object."""
    def __init__(self, ptr):
        """Constructor.
        :param ptr: The pointer representing this object.
        """
        self._ptr = ptr

    def _call_fmod(self, funcname, *args):
        result = getattr(_dll, funcname)(self._ptr, *args)
        result = RESULT(result)
        if result is not RESULT.OK:
            raise FmodError(result)
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._ptr.value == other._ptr.value
        else:
            return False