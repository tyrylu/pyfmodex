from ..utils import ckresult
from .library import get_library

class StudioObject(object):
    """A base Fmod studio object."""
    def __init__(self, ptr):
        """Constructor.
        :param ptr: The pointer representing this object.
        """
        self._ptr = ptr
        self._lib = get_library()

    def _call(self, specific_function_suffix, *args):
        func_name = "%s_%s"%(self.function_prefix, specific_function_suffix)
        result = getattr(self._lib, func_name)(self._ptr, *args)
        ckresult(result)
    
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._ptr.value == other._ptr.value
        else:
            return False