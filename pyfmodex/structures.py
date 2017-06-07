from ctypes import *
from .function_prototypes import *
from .callback_prototypes import *
from .structure_declarations import *

GUID._fields_ = [("data1", c_uint), ("data2", c_ushort), ("data3", c_ushort), ("data4", c_char * 8)]

class ADVANCEDSETTINGS(Structure):
    _fields_ = [("cbsize", c_int), ("maxMPEGcodecs", c_int), ("maxADPCMcodecs", c_int), ("maxXMAcodecs", c_int), ("maxVorbisCodecs", c_int), ("maxAT9Codecs", c_int), ("maxFADPCMCodecs", c_int), ("maxPCMcodecs", c_int), ("ASIONumChannels", c_int), ("ASIOChannelList", POINTER(c_char_p)), ("ASIOSpeakerList", POINTER(c_int)), ("HRTFMinAngle", c_float), ("HRTFMaxAngle", c_float), ("HRTFFreq", c_float), ("vol0virtualvol", c_float), ("defaultDecodeBufferSize", c_uint), ("profileport", c_ushort), ("geometryMaxFadeTime", c_uint), ("distanceFilterCenterFreq", c_float), ("reverb3Dinstance", c_int), ("DSPBufferPoolSize", c_int), ("stackSizeStream", c_uint), ("stackSizeNonBlocking", c_uint), ("stackSizeMixer", c_uint), ("resamplerMethod", c_int), ("commandQueueSize", c_uint), ("randomSeed", c_uint)]

    def __init__(self, *args, **kwargs):
        Structure.__init__(self, *args, **kwargs)
        self.cbsize = sizeof(self)

ASYNCREADINFO._fields_ = [("handle", c_void_p), ("offset", c_uint), ("sizebytes", c_uint), ("priority", c_int), ("userdata", c_void_p), ("buffer", c_void_p), ("bytesread", c_uint), ("done", FILE_ASYNCDONE_FUNC)]

class CODEC_DESCRIPTION(Structure):
    _fields_ = [("name", c_char_p), ("version", c_uint), ("defaultasstream", c_int), ("timeunits", c_int), ("open", CODEC_OPEN_CALLBACK), ("close", CODEC_CLOSE_CALLBACK), ("read", CODEC_READ_CALLBACK), ("getlength", CODEC_GETLENGTH_CALLBACK), ("setposition", CODEC_SETPOSITION_CALLBACK), ("getposition", CODEC_GETPOSITION_CALLBACK), ("soundcreate", CODEC_SOUNDCREATE_CALLBACK), ("getwaveformat", CODEC_GETWAVEFORMAT_CALLBACK)]

CODEC_WAVEFORMAT._fields_ = [("name", c_char_p), ("format", c_int), ("channels", c_int), ("frequency", c_int), ("lengthbytes", c_uint), ("lengthpcm", c_uint), ("pcmblocksize", c_uint), ("loopstart", c_int), ("loopend", c_int), ("mode", c_int), ("channelmask", c_int), ("channelorder", c_int), ("peakvolume", c_float)]

CODEC_STATE._fields_ = [("numsubsounds", c_int), ("waveformat", CODEC_WAVEFORMAT), ("plugindata", c_void_p), ("filehandle", c_void_p), ("filesize", c_uint), ("fileread", FILE_READ_CALLBACK), ("fileseek", FILE_SEEK_CALLBACK), ("metadata", CODEC_METADATA_CALLBACK), ("waveformatversion", c_int)]

COMPLEX._fields_ = [("real", c_float), ("imag", c_float)]

CREATESOUNDEXINFO._fields_ = [("cbsize", c_int), ("length", c_uint), ("fileoffset", c_uint), ("numchannels", c_int), ("defaultfrequency", c_int), ("format", c_int), ("decodebuffersize", c_uint), ("initialsubsound", c_int), ("numsubsounds", c_int), ("inclusionlist", POINTER(c_int)), ("inclusionlistnum", c_int), ("pcmreadcallback", SOUND_PCMREADCALLBACK), ("pcmsetposcallback", SOUND_PCMSETPOSCALLBACK), ("nonblockcallback", SOUND_NONBLOCKCALLBACK), ("dlsname", c_char_p), ("encryptionkey", c_char_p), ("maxpolyphony", c_int), ("userdata", c_void_p), ("suggestedsoundtype", c_int), ("useropen", FILE_OPEN_CALLBACK), ("userclose", FILE_CLOSE_CALLBACK), ("userread", FILE_READ_CALLBACK), ("userseek", FILE_SEEK_CALLBACK), ("userasyncread", FILE_ASYNCREAD_CALLBACK), ("userasynccancel", FILE_ASYNCCANCEL_CALLBACK), ("fileuserdata", c_void_p), ("filebuffersize", c_int), ("channelorder", c_int), ("channelmask", c_int), ("initialsoundgroup", c_void_p), ("initialseekposition", c_uint), ("initialseekpostype", c_int), ("ignoresetfilesystem", c_int), ("audioqueuepolicy", c_uint), ("minmidigranularity", c_uint), ("nonblockthreadid", c_int), ("fsbguid", GUID)]

def exinfo_init(self, *args, **kwargs):
    Structure.__init__(self, *args, **kwargs)
    self.cbsize = sizeof(self)
CREATESOUNDEXINFO.__init__ = exinfo_init

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

THREED_ATTRIBUTES._fields_ = [("position", VECTOR), ("velocity", VECTOR), ("forward", VECTOR), ("up", VECTOR)]
    
DSP_BUFFER_ARRAY._fields_ = [("numbuffers", c_int), ("buffernumchannels", POINTER(c_int)), ("bufferchannelmask", POINTER(c_int)), ("buffers", POINTER(POINTER(c_float))), ("speakermode", c_int)]

class DSP_METERING_INFO(Structure):
    _fields_ = [("numsamples", c_int), ("peaklevel", c_float * 32), ("rmslevel", c_float * 32), ("numchannels", c_short)]

class DSP_PARAMETER_3DATTRIBUTES(Structure):
    _fields_ = [("relative", THREED_ATTRIBUTES), ("absolute", THREED_ATTRIBUTES)]

class DSP_PARAMETER_3DATTRIBUTES_MULTI(Structure):
    _fields_ = [("numlisteners", c_int), ("relative", THREED_ATTRIBUTES * 8), ("weight", c_float * 8), ("absolute", THREED_ATTRIBUTES)]

class DSP_PARAMETER_DESC_BOOL(Structure):
    _fields_ = [("defaultval", c_bool), ("valuenames", POINTER(c_char_p))]

class DSP_PARAMETER_DESC_DATA(Structure):
    _fields_ = [("datatype", c_int)]

class DSP_PARAMETER_FLOAT_MAPPING_PIECEWISE_LINEAR(Structure):
    _fields_ = [("numpoints", c_int), ("pointparamvalues", POINTER(c_float)), ("pointpositions", POINTER(c_float))]

class DSP_PARAMETER_FLOAT_MAPPING(Structure):
    _fields_ = [("type", c_int), ("piecewiselinearmapping", DSP_PARAMETER_FLOAT_MAPPING_PIECEWISE_LINEAR)]

class DSP_PARAMETER_DESC_FLOAT(Structure):
    _fields_ = [("min", c_float), ("max", c_float), ("defaultval", c_float), ("mapping", DSP_PARAMETER_FLOAT_MAPPING)]

class DSP_PARAMETER_DESC_INT(Structure):
    _fields_ = [("min", c_int), ("max", c_int), ("defaultval", c_int), ("goestoinf", c_bool), ("valuenames", POINTER(c_char_p))]

class DSP_PARAMETER_FFT(Structure):
    _fields_ = [("length", c_int), ("numchannels", c_int), ("spectrum", c_float * 32)]

class DSP_PARAMETER_OVERALLGAIN(Structure):
    _fields_ = [("linear_gain", c_float), ("linear_gain_additive", c_float)]

class DSP_PARAMETER_SIDECHAIN(Structure):
    _fields_ = [("sidechainenable", c_bool)]

class DSP_STATE_DFT_FUNCTIONS(Structure):
    _fields_ = [("fftreal", DSP_DFT_FFTREAL_FUNC), ("inversefftreal", DSP_DFT_IFFTREAL_FUNC)]

class DSP_STATE_PAN_FUNCTIONS(Structure):
    _fields_ = [("summonomatrix", DSP_PAN_SUMMONOMATRIX_FUNC), ("sumstereomatrix", DSP_PAN_SUMSTEREOMATRIX_FUNC), ("sumsurroundmatrix", DSP_PAN_SUMSURROUNDMATRIX_FUNC), ("summonotosurroundmatrix", DSP_PAN_SUMMONOTOSURROUNDMATRIX_FUNC), ("sumstereotosurroundmatrix", DSP_PAN_SUMSTEREOTOSURROUNDMATRIX_FUNC), ("getrolloffgain", DSP_PAN_GETROLLOFFGAIN_FUNC)]

class DSP_STATE_FUNCTIONS(Structure):
    _fields_ = [("alloc", DSP_ALLOC_FUNC), ("realloc", DSP_REALLOC_FUNC), ("free", DSP_FREE_FUNC), ("getsamplerate", DSP_GETSAMPLERATE_FUNC), ("getblocksize", DSP_GETBLOCKSIZE_FUNC), ("dft", POINTER(DSP_STATE_DFT_FUNCTIONS)), ("pan", POINTER(DSP_STATE_PAN_FUNCTIONS)), ("getspeakermode", DSP_GETSPEAKERMODE_FUNC), ("getclock", DSP_GETCLOCK_FUNC), ("getlistenerattributes", DSP_GETLISTENERATTRIBUTES_FUNC), ("log", DSP_LOG_FUNC), ("getuserdata", DSP_GETUSERDATA_FUNC)]

DSP_STATE._fields_ = [("instance", c_void_p), ("plugindata", c_void_p), ("channelmask", c_int), ("sourcespeakermode", c_int), ("sidechaindata", POINTER(c_float)), ("sidechainchannels", c_int), ("functions", POINTER(DSP_STATE_FUNCTIONS)), ("systemobject", c_int)]

class DSP_PARAMETER_DESC(Structure):
    _fields_ = [("type", c_int), ("name", c_char * 16), ("label", c_char * 16), ("description", c_char_p), ("floatdesc", DSP_PARAMETER_DESC_FLOAT), ("intdesc", DSP_PARAMETER_DESC_INT), ("descbool", DSP_PARAMETER_DESC_BOOL), ("datadesc", DSP_PARAMETER_DESC_DATA)]

class DSP_DESCRIPTION(Structure):
    _fields_ = [("pluginsdkversion", c_uint), ("name", c_char * 32), ("version", c_uint), ("numinputbuffers", c_int), ("numoutputbuffers", c_int), ("create", DSP_CREATE_CALLBACK), ("release", DSP_RELEASE_CALLBACK), ("reset", DSP_RESET_CALLBACK), ("read", DSP_READ_CALLBACK), ("process", DSP_PROCESS_CALLBACK), ("setposition", DSP_SETPOSITION_CALLBACK), ("numparameters", c_int), ("paramdesc", POINTER(POINTER(DSP_PARAMETER_DESC))), ("setparameterfloat", DSP_SETPARAM_FLOAT_CALLBACK), ("setparameterint", DSP_SETPARAM_INT_CALLBACK), ("setparameterbool", DSP_SETPARAM_BOOL_CALLBACK), ("setparameterdata", DSP_SETPARAM_DATA_CALLBACK), ("getparameterfloat", DSP_GETPARAM_FLOAT_CALLBACK), ("getparameterint", DSP_GETPARAM_INT_CALLBACK), ("getparameterbool", DSP_GETPARAM_BOOL_CALLBACK), ("getparameterdata", DSP_GETPARAM_DATA_CALLBACK), ("shouldiprocess", DSP_SHOULDIPROCESS_CALLBACK), ("userdata", c_void_p), ("sys_register", DSP_SYSTEM_REGISTER_CALLBACK), ("sys_deregister", DSP_SYSTEM_DEREGISTER_CALLBACK), ("sys_mix", DSP_SYSTEM_MIX_CALLBACK)]
    
class ERRORCALLBACK_INFO(Structure):
    _fields_ = [("result", c_int), ("instancetype", c_int), ("instance", c_void_p), ("functionname", c_char_p), ("functionparams", c_char_p)]


class OUTPUT_DESCRIPTION(Structure):
    _fields_ = [("apiversion", c_uint), ("name", c_char_p), ("version", c_uint), ("polling", c_int), ("getnumdrivers", OUTPUT_GETNUMDRIVERS_CALLBACK), ("getdriverinfo", OUTPUT_GETDRIVERINFO_CALLBACK), ("init", OUTPUT_INIT_CALLBACK), ("start", OUTPUT_START_CALLBACK), ("stop", OUTPUT_STOP_CALLBACK), ("close", OUTPUT_CLOSE_CALLBACK), ("update", OUTPUT_UPDATE_CALLBACK), ("gethandle", OUTPUT_GETHANDLE_CALLBACK), ("getposition", OUTPUT_GETPOSITION_CALLBACK), ("lock", OUTPUT_LOCK_CALLBACK), ("unlock", OUTPUT_UNLOCK_CALLBACK), ("mixer", OUTPUT_MIXER_CALLBACK), ("object3dgetinfo", OUTPUT_OBJECT3DGETINFO_CALLBACK), ("object3dalloc", OUTPUT_OBJECT3DALLOC_CALLBACK), ("object3dfree", OUTPUT_OBJECT3DFREE_CALLBACK), ("object3dupdate", OUTPUT_OBJECT3DUPDATE_CALLBACK), ("openport", OUTPUT_OPENPORT_CALLBACK), ("closeport", OUTPUT_CLOSEPORT_CALLBACK)]

OUTPUT_OBJECT3DINFO._fields_ = [("buffer", POINTER(c_float)), ("bufferlength", c_uint), ("position", VECTOR), ("gain", c_float), ("spread", c_float), ("priority", c_float)]


OUTPUT_STATE._fields_ = [("plugindata", c_void_p), ("readfrommixer", OUTPUT_READFROMMIXER), ("alloc", OUTPUT_ALLOC), ("free", OUTPUT_FREE), ("log", OUTPUT_LOG), ("copyport", OUTPUT_COPYPORT)]

class PLUGINLIST(Structure):
    _fields_ = [("type", c_int), ("description", c_void_p)]

class REVERB_PROPERTIES(Structure):
    _fields_ = [("DecayTime", c_float), ("EarlyDelay", c_float), ("LateDelay", c_float), ("HFReference", c_float), ("HFDecayRatio", c_float), ("Diffusion", c_float), ("Density", c_float), ("LowShelfFrequency", c_float), ("LowShelfGain", c_float), ("HighCut", c_float), ("EarlyLateMix", c_float), ("WetLevel", c_float)]

class TAG(Structure):
    _fields_ = [("type", c_int), ("datatype", c_int), ("name", c_char_p), ("data", c_void_p), ("datalen", c_uint), ("updated", c_bool)]
