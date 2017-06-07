"""Fmod ex python bindings."""
from .fmodex import get_disk_busy, set_disk_busy, get_memory_stats, initialize_debugging, initialize_memory
from . import globalvars
# Avoid recursive import hell
from . import dsp, dsp_connection, geometry, channel, channel_group, reverb, sound, sound_group, system 
from .utils import FmodError
__version__ = "0.5.1"

c = {}
c["DSP"] = dsp.DSP
c["DSP_Connection"] = dsp_connection.DSPConnection
c["Geometry"] = geometry.Geometry
c["Channel"] = channel.Channel
c["ChannelGroup"] = channel_group.ChannelGroup
c["Reverb3D"] = reverb.Reverb3D
c["Sound"] = sound.Sound
c["SoundGroup"] = sound_group.SoundGroup
c["System"] = system.System
globalvars.class_list = c
from . import constants
System = c["System"]