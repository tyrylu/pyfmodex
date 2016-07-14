"""Fmod ex python bindings."""
from .fmodex import get_debug_level, set_debug_level, get_disk_busy, set_disk_busy, get_memory_stats
from . import globalvars
# Avoid recursive import hell
from . import dsp, dsp_connection, geometry, channel, channel_group, reverb, sound, sound_group, system 
__version__ = "0.4.0"

c = {}
c["DSP"] = dsp.DSP
c["DSP_Connection"] = dsp_connection.DSPConnection
c["Geometry"] = geometry.Geometry
c["Channel"] = channel.Channel
c["ChannelGroup"] = channel_group.ChannelGroup
c["Reverb"] = reverb.Reverb
c["Sound"] = sound.Sound
c["SoundGroup"] = sound_group.SoundGroup
c["System"] = system.System
globalvars.class_list = c
from . import constants
System = c["System"]