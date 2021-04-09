"""Strcuture declarations."""

# pylint: disable=too-few-public-methods
# Just declaring at this point...

# pylint: disable=invalid-name
# Just staying close to the original names here.


from ctypes import Structure


class CODEC_STATE(Structure):
    """Codec state structure that is passed into each callback."""


class CREATESOUNDEXINFO(Structure):
    """Additional options for creating a Sound."""


class DSP_STATE(Structure):
    """DSP plugin structure that is passed into each callback."""


class DSP_BUFFER_ARRAY(Structure):
    """Structure for input and output buffers."""


class ASYNCREADINFO(Structure):
    """Information about a single asynchronous file operation."""


class OUTPUT_STATE(Structure):
    """Output object state passed into every callback provides access to plugin
    developers data and system functionality.
    """


class GUID(Structure):
    """Structure describing a globally unique identifier."""


class OUTPUT_OBJECT3DINFO(Structure):
    """Output 3D Object Info."""


class CODEC_WAVEFORMAT(Structure):
    """Codec wave format.

    This structure defines the attributes of a sound, and determines the format
    of the Sound object when it is created with
    :py:meth:`~pyfmodex.system.System.create_sound` or
    :py:meth:`~pyfmodex.system.System.create_stream`.
    """


class THREED_ATTRIBUTES(Structure):
    """Structure describing a position, velocity and orientation."""


class COMPLEX(Structure):
    """Complex number structure."""
