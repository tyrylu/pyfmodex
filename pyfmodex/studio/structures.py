from ctypes import Structure, c_char_p, c_int, c_float

class PARAMETER_DESCRIPTION(Structure):
    _fields_ = [("name", c_char_p), ("index", c_int), ("minimum", c_float), ("maximum", c_float), ("defaultvalue", c_float), ("type", c_int)]
