"""Handy util methods."""

import pyfmodex


def fmod_version():
    """Get FMOD API version number."""
    system = pyfmodex.System()
    version = system.version
    system.close()
    return version
