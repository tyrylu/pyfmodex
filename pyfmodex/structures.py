from ctypes import *

class ADVANCEDSETTINGS(Structure):
    _fields_ = [("cbsize", c_int), ("maxMPEGcodecs", c_int), ("maxADPCMcodecs", c_int), ("maxXMAcodecs", c_int), ("maxCELDcodecs", c_int), ("maxPCMcodecs", c_int), ("ASIONumChannels", c_int), ("ASIOChannelList", POINTER(c_char_p)), ("ASIOSpeakerList", POINTER(c_int)), ("max3DReverbDSPs", c_int), ("HRTFMinAngle", c_float), ("HRTFMaxAngle", c_float), ("HRTFFreq", c_float), ("vol0virtualvol", c_float), ("eventqueuesize", c_int), ("defaultDecodeBufferSize", c_uint), ("debugLogFilename", c_char_p), ("profileport", c_ushort), ("geometryMaxFadeTime", c_uint), ("maxSpectrumWaveDataBuffers", c_uint), ("musicSystemCacheDelay", c_uint), ("distanceFilterCentreFreq", c_float)]

    def __init__(self, *args, **kwargs):
        Structure.__init__(self, *args, **kwargs)
        self.cbsize = sizeof(self)

class ASYNCREADINFO(Structure):
    _fields_ = [("handle", c_void_p), ("offset", c_uint), ("sizebytes", c_uint), ("priority", c_int), ("buffer", c_void_p), ("bytesread", c_uint), ("result", c_int), ("userdata", c_void_p)]

# This tricky import here avoids circular import issues with importing ASYNCREADINFO in callbackprototypes.
from .callbackprototypes import *

class CDTOC(Structure):
    _fields_ = [("numtracks", c_int), ("min", c_int * 100), ("sec", c_int * 100), ("frame", c_int * 100)]

class CREATESOUNDEXINFO(Structure):
    _fields_ = [("cbsize", c_int), ("length", c_uint), ("fileoffset", c_uint), ("numchannels", c_int), ("defaultfrequency", c_int), ("format", c_int), ("decodebuffersize", c_uint), ("initialsubsound", c_int), ("numsubsounds", c_int), ("inclusionlist", POINTER(c_int)), ("inclusionlistnum", c_int), ("pcmreadcallback", SOUND_PCMREADCALLBACK), ("pcmsetposcallback", SOUND_PCMSETPOSCALLBACK), ("nonblockcallback", SOUND_NONBLOCKCALLBACK), ("dlsname", c_char_p), ("encryptionkey", c_char_p), ("maxpolyphony", c_int), ("userdata", c_void_p), ("suggestedsoundtype", c_int), ("useropen", FILE_OPENCALLBACK), ("userclose", FILE_CLOSECALLBACK), ("userread", FILE_READCALLBACK), ("userseek", FILE_SEEKCALLBACK), ("userasyncread", FILE_ASYNCREADCALLBACK), ("userasynccancel", FILE_ASYNCCANCELCALLBACK), ("speakermap", c_int), ("initialsoundgroup", POINTER(c_int)), ("initialseekposition", c_uint), ("initialseekpostype", c_int), ("ignoresetfilesystem", c_int), ("cddaforceaspi", c_int), ("audioqueuepolicy", c_uint), ("minmidigranularity", c_uint), ("nonblockthreadid", c_int)]

    def __init__(self, *args, **kwargs):
        Structure.__init__(self, *args, **kwargs)
        self.cbsize = sizeof(self)

class DSP_PARAMETERDESC(Structure):
    _fields_ = [("min", c_float), ("max", c_float), ("defaultval", c_float), ("name", c_char * 16), ("label", c_char * 16), ("description", c_char_p)]

class GUID(Structure):
    _fields_ = [("data1", c_uint), ("data2", c_ushort), ("data3", c_ushort), ("data4", c_char * 8)]

class REVERB_CHANNELPROPERTIES(Structure):
    _fields_ = [("Direct", c_int), ("DirectHF", c_int), ("Room", c_int), ("RoomHF", c_int), ("Obstruction", c_int), ("ObstructionLFRatio", c_float), ("Occlusion", c_int), ("OcclusionLFRatio", c_float), ("OcclusionRoomRatio", c_float), ("OcclusionDirectRatio", c_float), ("Exclusion", c_int), ("ExclusionLFRatio", c_float), ("OutsidevolumeHF", c_int), ("DopplerFactor", c_float), ("RolloffFactor", c_float), ("RoomRolloffFactor", c_float), ("AirAbsorptionFactor", c_float), ("Flags", c_uint), ("ConnectionPoint", c_int)]

class REVERBPROPERTIES(Structure):
    _fields_ = [("Instance", c_int), ("Environment", c_int), ("EnvSize", c_float), ("EnvDiffusion", c_float), ("Room", c_int), ("RoomHF", c_int), ("RoomLF", c_int), ("DecayTime", c_float), ("DecayHFRatio", c_float), ("DecayLFRatio", c_float), ("Reflections", c_int), ("ReflectionsDelay", c_float), ("ReflectionsPan", c_float * 3), ("Reverb", c_int), ("ReverbDelay", c_float), ("ReverbPan", c_float * 3), ("EchoTime", c_float), ("EchoDepth", c_float), ("ModulationTime", c_float), ("ModulationDepth", c_float), ("AirAbsorptionHF", c_float), ("HFReference", c_float), ("LFreference", c_float), ("RoomRolloffFactor", c_float), ("Diffusion", c_float), ("Density", c_float), ("Flags", c_uint)]

class TAG(Structure):
    _fields_ = [("type", c_int), ("datatype", c_int), ("name", c_char_p), ("data", c_void_p), ("datalen", c_uint), ("updated", c_int)]

class VECTOR(Structure):
    _fields_ = [("x", c_float), ("y", c_float), ("z", c_float)]

    @staticmethod
    def from_list(lst):
        vec = VECTOR()
        vec.x = lst[0]
        vec.y = lst[1]
        vec.z = lst[2]
        return vec

    def to_list(self):
        return [self.x, self.y, self.z]