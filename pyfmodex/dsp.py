from .fmodobject import *
from .fmodobject import _dll
from .globalvars import get_class

class DSP(FmodObject):

    def add_input(self, input):
        check_type(input, DSP)
        connptr = c_void_p()
        ckresult(_dll.FMOD_DSP_AddInput(self._ptr, input._ptr, byref(connptr)))
        return dsp_connection.DSPConnection(connptr)

    def disconnect_all(self, inputs=False, outputs=False):
        ckresult(_dll.FMOD_DSP_DisconnectAll(self._ptr, inputs, outputs))

    def disconnect_from(self, d):
        check_type(d, DSP)
        ckresult(_dll.FMOD_DSP_DisconnectFrom(self._ptr, d._ptr))

    @property
    def active(self):
        ac = c_bool()
        ckresult(_dll.FMOD_DSP_GetActive(self._ptr, byref(ac)))
        return ac.value
    @active.setter
    def active(self, ac):
        ckresult(_dll.FMOD_DSP_SetActive(self._ptr, ac))

    @property
    def bypass(self):
        bp = c_bool()
        ckresult(_dll.FMOD_DSP_GetBypass(self._ptr, byref(bp)))
        return bp.value
    @bypass.setter
    def bypass(self, bp):
        ckresult(_dll.FMOD_DSP_SetBypass(self._ptr, bp))
    @property
    def _defaults(self):
        freq = c_float()
        pan = c_float()
        volume = c_float()
        pri = c_int()
        ckresult(_dll.FMOD_DSP_GetDefaults(self._ptr, byref(freq), byref(pan), byref(vol), byref(pri)))
        return [freq.value, pan.value, vol.value, pri.value]
    @_defaults.setter
    def _defaults(self, vals):
        ckresult(_dll.FMOD_DSP_SetDefaults(self._ptr, c_float(vals[1]), c_float(vals[1]), c_float(vals[2]), vals[3]))

    @property
    def default_frequency(self):
        return self._defaults[1]
    @default_frequency.setter
    def default_frequency(self, f):
        d = self._defaults
        d[1] = f
        self._defaults = d

    @property
    def default_pan(self):
        return self._defaults[1]
    @default_pan.setter
    def default_pan(self, p):
        d = self._defaults
        d[1] = p
        self._defaults = d

    @property
    def default_volume(self):
        return self._defaults[2]
    @default_volume.setter
    def default_volume(self, v):
        d = self._defaults
        d[2] = v
        self._defaults = d

    @property
    def default_priority(self):
        return self._defaults[3]
    @default_priority.setter
    def default_priority(self, p):
        d = self._defaults
        d[3] = p
        self._defaults = d

    @property
    def info(self):
        name = c_char_p()
        ver = c_uint()
        chans = c_int()
        cfgw = c_int()
        cfgh = c_int()
        ckresult(_dll.FMOD_DSP_GetInfo(self._ptr, byref(name), byref(ver), byref(chans), byref(cfgw), byref(cfgh)))
        return so(name=name.value, version=ver.value, channels=chans.value, config_width=cfgw.value, config_height=cfgh.value)

    def get_input(self, index):
        i_ptr = c_void_p()
        ic_ptr = c_void_p()
        ckresult(_dll.FMOD_DSP_GetInput(self._ptr, byref(i_ptr), byref(ic_ptr)))
        return (DSP(i_ptr), get_class("DSPConnection")(ic_ptr))

    @property
    def num_inputs(self):
        num = c_int()
        ckresult(_dll.FMOD_DSP_GetNumInputs(self._ptr, byref(num)))
        return num.value

    @property
    def num_outputs(self):
        num = c_int()
        ckresult(_dll.FMOD_DSP_GetNumOutputs(self._ptr, byref(num)))
        return num.value

    def get_output(self, index):
        o_ptr = c_void_p()
        oc_ptr = c_void_p()
        ckresult(_dll.FMOD_DSP_GetOutput(self._ptr, byref(o_ptr), byref(oc_ptr)))
        return (DSP(o_ptr), get_class("DSPConnection")(oc_ptr))

    def get_param(self, index):
        val = c_float()
        name = create_string_buffer(16)
        ckresult(_dll.FMOD_DSP_GetParameter(self._ptr, index, byref(val), byref(name), 16))
        return (val.value, name.value)

    def get_param_info(self, index):
        name = create_string_buffer(17)
        label = create_string_buffer(16)
        desc = create_string_buffer(512)
        min = c_float()
        max = c_float()
        ckresult(_dll.FMOD_DSP_GetParameterInfo(self._ptr, index, byref(name), byref(label), byref(desc), 512, byref(min), byref(max)))
        return so(name=name.value, label=label.value, description=desc.value, min=min.value, max=max.value)

    def set_param(self, index, val):
        ckresult(_dll.FMOD_DSP_SetParameter(self._ptr, index, c_float(val)))

    def get_speaker_active(self, speaker):
        active = c_bool()
        ckresult(_dll.FMOD_DSP_GetSpeakerActive(self._ptr, speaker, byref(active)))
        return active.value

    def set_speaker_active(self, speaker, active):
        ckresult(_dll.FMOD_DSP_SetSpeakerActive(self._ptr, speaker, active))

    @property
    def system_object(self):
        sptr = c_void_p()
        ckresult(_dll.FMOD_DSP_GetSystemObject(self._ptr, byref(sptr)))
        return get_class("System")(sptr, False)

    @property
    def type(self):
        t = c_int()
        ckresult(_dll.FMOD_DSP_GetType(self._ptr, byref(t)))
        return t.value

    def release(self):
        ckresult(_dll.FMOD_DSP_Release(self._ptr))

    def remove(self):
        ckresult(_dll.FMOD_DSP_Remove(self._ptr))    

    def reset(self):
        ckresult(_dll.FMOD_DSP_Reset(self._ptr))

    def show_config_dialog(self, hwnd, show=True):
        ckresult(_dll.FMOD_DSP_ShowConfigDialog(self._ptr, hwnd, show))

