from ctypes import c_int, c_void_p, byref
from .studio_object import StudioObject
from .event_description import EventDescription

class Bank(StudioObject):
    function_prefix = "FMOD_Studio_Bank"
    
    @property
    def event_count(self):
        count = c_int()
        self._call("GetEventCount", byref(count))
        return count.value

    @property
    def events(self):
        count = self.event_count
        array = (c_void_p * count)()
        written = c_int()
        self._call("GetEventList", array, count, byref(written))
        assert count == written.value
        descs = []
        for pointer in array:   
            descs.append(EventDescription(pointer))
        return descs