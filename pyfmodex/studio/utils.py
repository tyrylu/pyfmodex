import pyfmodex


def fmod_version():
    system = pyfmodex.System()
    version = system.version
    system.close()
    return version
