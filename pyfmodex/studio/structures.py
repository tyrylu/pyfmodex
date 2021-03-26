"""C strucs"""

# pylint: disable=too-few-public-methods,invalid-name
# these are not your average classes

from ctypes import Structure, c_char_p, c_float, c_int, c_uint, sizeof


class ADVANCEDSETTINGS(Structure):
    """Settings for advanced features like configuring memory and cpu usage.

    cbSize: Size of this structure in bytes.
    commandqueuesize: Command queue size for studio async processing.
    handleinitialsize: Initial size to allocate for handles. Memory for handles
        will grow as needed in pages.
    studioupdateperiod: Update period of Studio when in async mode, in
        milliseconds. Will be quantized to the nearest multiple of mixer duration.
    idlesampledatapoolsize: Size in bytes of sample data to retain in memory
        when no longer used, to avoid repeated disk I/O. Use -1 to disable.
    streamingscheduledelay: Specify the schedule delay for streams, in samples.
        Lower values can reduce latency when scheduling events containing streams
        but may cause scheduling issues if too small.
    encryptionkey: Specify the key for loading sounds from encrypted banks.
    """

    _fields_ = [
        ("cbsize", c_int),
        ("commandqueuesize", c_uint),
        ("handleinitialsize", c_uint),
        ("studioupdatedperiod", c_int),
        ("idlesampledatapoolsize", c_int),
        ("streamingscheduledelay", c_uint),
        ("encryptionkey", c_char_p),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cbsize = sizeof(self)


class BUFFER_INFO(Structure):
    """Information for a single buffer in FMOD Studio.

    currentusage: Current buffer usage in bytes.
    peakusage: Peak buffer usage in bytes.
    capacity: Buffer capacity in bytes.
    stallcount: Cumulative number of stalls due to buffer overflow.
    stalltime:  Cumulative amount of time stalled due to buffer overflow, in
        seconds.
    """

    _fields_ = [
        ("currentusage", c_int),
        ("peakusage", c_int),
        ("capacity", c_int),
        ("stallcount", c_int),
        ("stalltime", c_float),
    ]


class BUFFER_USAGE(Structure):
    """Information for FMOD Studio buffer usage.

    studiocommandqueue: Information for the Studio Async Command buffer.
    studiohandle: Information for the Studio handle table.
    """

    _fields_ = [("studiocommandqueue", BUFFER_INFO), ("studiohandle", BUFFER_INFO)]


class PARAMETER_DESCRIPTION(Structure):
    """An event parameter.

    name: Parameter name.
    minimum: Minimum parameter value.
    maximum: Maximum parameter value.
    defaultvalue: Default parameter value.
    type: Parameter type.
    """
    # TODO: id vs index, flags -> because of FMOD API update to 2.0?

    _fields_ = [
        ("name", c_char_p),
        ("index", c_int),
        ("minimum", c_float),
        ("maximum", c_float),
        ("defaultvalue", c_float),
        ("type", c_int),
    ]
