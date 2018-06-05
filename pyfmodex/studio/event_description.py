from ctypes import c_int, c_void_p, byref, create_string_buffer
from .studio_object import StudioObject
from .event_instance import EventInstance

class EventDescription(StudioObject):
    function_prefix = "FMOD_Studio_EventDescription"
    
    @property
    def path(self):
        required = c_int()
        self._call("GetPath", None, 0, byref(required))
        path_buffer = create_string_buffer(required.value)
        self._call("GetPath", path_buffer, len(path_buffer), None)
        return path_buffer.value.decode("utf-8")

    def create_instance(self):
        instance_ptr = c_void_p()
        self._call("CreateInstance", byref(instance_ptr))
        return EventInstance(instance_ptr)

    @property
    def parameter_count(self):
        count = c_int()
        self._call("GetParameterCount", byref(count))
        return count.value

    @property
    def user_property_count(self):
        count = c_int()
        self._call("GetUserPropertyCount", byref(count))
        return count.value