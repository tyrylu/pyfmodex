from ctypes import *
from .fmodobject import *
from .globalvars import get_class
from .utils import check_type
from .flags import CHANNELMASK
from .enums import SPEAKERMODE, DSP_TYPE
from .structobject import Structobject as so
from .structures import DSP_METERING_INFO, DSP_PARAMETER_DESC

class DSP(FmodObject):

    def add_input(self, input, connection_type):
        check_type(input, DSP)
        connptr = c_void_p()
        self._call_fmod("FMOD_DSP_AddInput", input._ptr, byref(connptr), connection_type.value)
        return get_class("DSP_Connection")(connptr)

    def disconnect_all(self, inputs=False, outputs=False):
        self._call_fmod("FMOD_DSP_DisconnectAll", inputs, outputs)

    def disconnect_from(self, dsp=None, connection=None):
        dsp_ptr = None
        connection_ptr = None
        if dsp:
            check_type(dsp, DSP)
            dsp_ptr = dsp._ptr
        if connection:
            check_type(connection, get_class("DSP_Connection"))
            connection_ptr = connection._ptr
        self._call_fmod("FMOD_DSP_DisconnectFrom", dsp_ptr, connection_ptr)

    @property
    def active(self):
        ac = c_bool()
        self._call_fmod("FMOD_DSP_GetActive", byref(ac))
        return ac.value
    @active.setter
    def active(self, ac):
        self._call_fmod("FMOD_DSP_SetActive", ac)

    @property
    def bypass(self):
        bp = c_bool()
        self._call_fmod("FMOD_DSP_GetBypass", byref(bp))
        return bp.value
    @bypass.setter
    def bypass(self, bp):
        self._call_fmod("FMOD_DSP_SetBypass", bp)

    @property
    def channel_format(self):
        mask = c_int()
        num_channels = c_int()
        speaker_mode = c_int()
        self._call_fmod("FMOD_DSP_GetChannelFormat", byref(mask), byref(num_channels), byref(speaker_mode))
        return so(channel_mask=CHANNELMASK(mask.value), num_channels=num_channels.value, source_speaker_mode=SPEAKERMODE(speaker_mode.value))
    @channel_format.setter
    def channel_format(self, format):
        self._call_fmod("FMOD_DSP_SetChannelFormat", int(format.channel_mask), format.num_channels, format.source_speaker_mode.value)

    def get_data_parameter_index(self, data_type):
        index = c_int()
        self._call_fmod("FMOD_DSP_GetDataParameterIndex", data_type, byref(index))
        return index.value
    
    @property
    def idle(self):
        res = c_bool()
        self._call_fmod("FMOD_DSP_GetIdle", byref(res))
        return res.value
    @property
    def info(self):
        name = create_string_buffer(33)
        ver = c_uint()
        chans = c_int()
        cfgw = c_int()
        cfgh = c_int()
        self._call_fmod("FMOD_DSP_GetInfo", byref(name), byref(ver), byref(chans), byref(cfgw), byref(cfgh))
        return so(name=name.value, version=ver.value, channels=chans.value, config_width=cfgw.value, config_height=cfgh.value)

    def get_input(self, index):
        i_ptr = c_void_p()
        ic_ptr = c_void_p()
        self._call_fmod("FMOD_DSP_GetInput", index, byref(i_ptr), byref(ic_ptr))
        return (DSP(i_ptr), get_class("DSP_Connection")(ic_ptr))

    @property
    def _metering_enabled(self):
        input = c_bool()
        output = c_bool()
        self._call_fmod("FMOD_DSP_GetMeteringEnabled", byref(input), byref(output))
        return input.value, output.value
    @_metering_enabled.setter
    def _metering_enabled(self, values):
        self._call_fmod("FMOD_DSP_SetMeteringEnabled", values[0], values[1])
        
    @property
    def input_metering_enabled(self):
        return self._metering_enabled[0]
    @input_metering_enabled.setter
    def input_metering_enabled(self, val):
        self._metering_enabled = (val, self._metering_enabled[1])
        
    @property
    def output_metering_enabled(self):
        return self._metering_enabled[1]
    @output_metering_enabled.setter
    def output_metering_enabled(self, val):
        self._metering_enabled = (self._metering_enabled[0], val)

    @property
    def metering_info(self):
        input = DSP_METERING_INFO()
        output = DSP_METERING_INFO()
        self._call_fmod("FMOD_DSP_GetMeteringInfo", byref(input), byref(output))
        return input, output
    
    @property
    def num_inputs(self):
        num = c_int()
        self._call_fmod("FMOD_DSP_GetNumInputs", byref(num))
        return num.value

    @property
    def num_outputs(self):
        num = c_int()
        self._call_fmod("FMOD_DSP_GetNumOutputs", byref(num))
        return num.value

    @property
    def num_parameters(self):
        num = c_int()
        self._call_fmod("FMOD_DSP_GetNumParameters", byref(num))
        return num.value
    
    def get_output(self, index):
        o_ptr = c_void_p()
        oc_ptr = c_void_p()
        self._call_fmod("FMOD_DSP_GetOutput", index, byref(o_ptr), byref(oc_ptr))
        return (DSP(o_ptr), get_class("DSP_Connection")(oc_ptr))

    @property
    def output_channel_format(self):
        inmask = c_int()
        outmask = c_int()
        inchannels = c_int()
        outchannels = c_int()
        inmode = c_int()
        outmode = c_int()
        self._call_fmod("FMOD_DSP_GetOutputChannelFormat", byref(inmask), byref(inchannels), byref(inmode), byref(outmask), byref(outchannels), byref(outmode))
        return so(in_mask=CHANNELMASK(inmask.value), out_mask=CHANNELMASK(outmask.value), in_channels=inchannels.value, out_channels=outchannels.value, in_speaker_mode=SPEAKERMODE(inmode.value), out_speaker_mode=outmode.value) # The parameter should be an SPEAKERMODE, but the echo dsp returned basically random value there.
    def get_parameter_bool(self, index):
        value_str = create_string_buffer(256)
        value = c_bool()
        self._call_fmod("FMOD_DSP_GetParameterBool", index, byref(value), value_str, len(value_str))
        return value.value, value_str.value
        
    def get_parameter_data(self, index):
        value_str = create_string_buffer(256)
        value = c_void_p()
        value_len = c_uint()
        self._call_fmod("FMOD_DSP_GetParameterData", index, byref(value), byref(value_len), value_str, len(value_str))
        return value, value_len.value, value_str.value
    def get_parameter_float(self, index):
        value_str = create_string_buffer(256)
        value = c_float()
        self._call_fmod("FMOD_DSP_GetParameterFloat", index, byref(value), value_str, len(value_str))
        return value.value, value_str.value

    def get_parameter_info(self, index):
        descs = (DSP_PARAMETER_DESC * 2)()
        desc = (DSP_PARAMETER_DESC * 1)()
        self._call_fmod("FMOD_DSP_GetParameterInfo", index, byref(desc))    
        return desc[0]

    def get_parameter_int(self, index):
        value_str = create_string_buffer(256)
        value = c_int()
        self._call_fmod("FMOD_DSP_GetParameterInt", index, byref(value), value_str, len(value_str))
        return value.value, value_str.value

    def set_parameter_bool(self, index, val):
        self._call_fmod("FMOD_DSP_SetParameterBool", index, val)
    def set_parameter_data(self, index, ptr, length):
        self._call_fmod("FMOD_DSP_SetParameterData", index, ptr, length)

    def set_parameter_float(self, index, val):
        self._call_fmod("FMOD_DSP_SetParameterFloat", index, c_float(val))
    
    def set_parameter_int(self, index, val):
        self._call_fmod("FMOD_DSP_SetParameterInt", index, val)
    
    @property
    def system_object(self):
        sptr = c_void_p()
        self._call_fmod("FMOD_DSP_GetSystemObject", byref(sptr))
        return get_class("System")(sptr, False)

    @property
    def type(self):
        typ = c_int()
        self._call_fmod("FMOD_DSP_GetType", byref(typ))
        return DSP_TYPE(typ.value)

    @property
    def _wet_dry_mix(self):
        pre = c_float()
        post = c_float()
        dry = c_float()
        self._call_fmod("FMOD_DSP_GetWetDryMix", byref(pre), byref(post), byref(dry))
        return pre.value, post.value, dry.value
    @_wet_dry_mix.setter
    def _wet_dry_mix(self, values):
        self._call_fmod("FMOD_DSP_SetWetDryMix", c_float(values[0]), c_float(values[1]), c_float(values[2]))
    @property
    def pre_mix(self):
        return self._wet_dry_mix[0]
    @pre_mix.setter
    def pre_mix(self, val):
        mix = list(self._wet_dry_mix)
        mix[0] = val
        self._wet_dry_mix = mix
    @property
    def post_mix(self):
        return self._wet_dry_mix[1]
    @post_mix.setter
    def post_mix(self, val):
        mix = list(self._wet_dry_mix)
        mix[1] = val
        self._wet_dry_mix = mix
    @property
    def dry_mix(self):
        return self._wet_dry_mix[2]
    @dry_mix.setter
    def dry_mix(self, val):
        mix = list(self._wet_dry_mix)
        mix[2] = val
        self._wet_dry_mix = mix

    def release(self):
        self._call_fmod("FMOD_DSP_Release")

    def reset(self):
        self._call_fmod("FMOD_DSP_Reset")

    def show_config_dialog(self, hwnd, show=True):
        self._call_fmod("FMOD_DSP_ShowConfigDialog", hwnd, show)

