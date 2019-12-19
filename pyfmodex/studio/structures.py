from ctypes import Structure, c_char_p, c_int, c_uint, c_float, sizeof

class ADVANCEDSETTINGS(Structure):
    _fields_ = [("cbsize", c_int), ("commandqueuesize", c_uint), ("handleinitialsize", c_uint), ("studioupdatedperiod", c_int), ("idlesampledatapoolsize", c_int), ("streamingscheduledelay", c_uint), ("encryptionkey", c_char_p)]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cbsize = sizeof(self)

class BUFFER_INFO(Structure):
    _fields_ = [("currentusage", c_int), ("peakusage", c_int), ("capacity", c_int), ("stallcount", c_int), ("stalltime", c_float)]

class BUFFER_USAGE(Structure):
    _fields_ = [("studiocommandqueue", BUFFER_INFO), ("studiohandle", BUFFER_INFO)]

class PARAMETER_DESCRIPTION(Structure):
    _fields_ = [("name", c_char_p), ("index", c_int), ("minimum", c_float), ("maximum", c_float), ("defaultvalue", c_float), ("type", c_int)]
