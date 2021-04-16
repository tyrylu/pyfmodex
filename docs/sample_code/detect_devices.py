"""Sample code to list identification information about all sound devices
(audio out and audio in) detected by FMOD Engine on a system.
"""

import re

import pyfmodex
from pyfmodex.enums import RESULT, SPEAKERMODE
from pyfmodex.exceptions import FmodError
from pyfmodex.flags import DRIVER_STATE

system = pyfmodex.System()
system.init()


def _pp_driverinfo(driverinfo, indent=1):
    """Pretty print driverinfo.

    Lists all keys in the given pyfmodex.structobject with their values,
    indented by the given number of four spaces.

    .. todo:: Figure out how the GUID structure works exactly.
    """
    for key in driverinfo.keys():
        value = driverinfo[key]
        if isinstance(value, bytes):
            value = value.decode()
        elif isinstance(value, pyfmodex.structure_declarations.GUID):
            continue
        elif key == "system_rate":
            value = f"{value} kHz"
        elif key == "speaker_mode":
            value = SPEAKERMODE(value).name
        elif key == "state":
            value = re.sub(r"^DRIVER_STATE.|\)$", "", str(DRIVER_STATE(value))).replace(
                "|", ", "
            )
        print("    " * indent, end="")
        print(f"{key}: {value}")
    print()


def list_drivers(title, meth):
    """List and prettyprint information about drivers returned by the given
    method.
    """
    print(title)
    print("-" * len(title))
    counter = 0
    while True:
        try:
            driverinfo = meth(counter)
        except FmodError as fmoderr:
            if fmoderr.result == RESULT.INVALID_PARAM:
                break
            raise fmoderr
        print(f"Index {counter}:")
        _pp_driverinfo(driverinfo)
        counter += 1


list_drivers("Detected audio OUT devices", system.get_driver_info)
list_drivers("Detected audio IN devices", system.get_record_driver_info)
