""""Flags."""

from flags import Flags


class STUDIO_INIT_FLAGS(Flags):  # pylint: disable=invalid-name
    """Studio System initialization flags.

    NORMAL: Use defaults for all initialization options.
    LIVEUPDATE: Enable live update.
    ALLOW_MISSING_PLUGINS: Load banks even if they reference plugins that have not been loaded.
    SYNCHRONOUS_UPDATE: Disable asynchronous processing and perform all processing on the calling thread instead.
    DEFERRED_CALLBACKS: Defer timeline callbacks until the main update.
    LOAD_FROM_UPDATE: No additional threads are created for bank and resource loading.
    """

    __no_flags_name__ = "NORMAL"
    LIVEUPDATE = 0x00000001
    ALLOW_MISSING_PLUGINS = 0x00000002
    SYNCHRONOUS_UPDATE = 0x00000004
    DEFERRED_CALLBACKS = 0x00000008
    LOAD_FROM_UPDATE = 0x00000010


class LOAD_BANK_FLAGS(Flags):  # pylint: disable=invalid-name
    """Flags to control bank loading.

    NORMAL: Standard behavior.
    NONBLOCKING: Bank loading occurs asynchronously rather than occurring immediately.
    DECOMPRESS_SAMPLES: Force samples to decompress into memory when they are loaded, rather than staying compressed.
    UNENCRYPTED: Ignore the encryption key specified by Advanced Settings when loading sounds from this bank (assume the sounds in the bank are not encrypted).
    """

    __no_flags_name__ = "NORMAL"
    NONBLOCKING = 0x00000001
    DECOMPRESS_SAMPLES = 0x00000002
    UNENCRYPTED = 0x00000004
