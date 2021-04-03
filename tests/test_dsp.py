import pytest
from pyfmodex.enums import (DSP_COMPRESSOR, DSP_ECHO, DSP_OSCILLATOR,
                            DSP_PARAMETER_DATA_TYPE, DSP_PARAMETER_TYPE,
                            DSP_TYPE, DSPCONNECTION_TYPE, RESULT, SPEAKERMODE)
from pyfmodex.exceptions import FmodError


def test_add_input(echo):
    conn = echo.add_input(echo, DSPCONNECTION_TYPE.STANDARD)


def test_disconnect_all(echo):
    echo.disconnect_all(inputs=True, outputs=True)


def test_disconnect_from(echo):
    conn = echo.add_input(echo, DSPCONNECTION_TYPE.STANDARD)
    echo.disconnect_from(echo, conn)
    echo.disconnect_from()


def test_active(echo):
    assert not echo.active
    echo.active = True
    assert echo.active


def test_bypass(echo):
    assert not echo.bypass
    echo.bypass = True
    assert echo.bypass


def test_channel_format(echo):
    format = echo.channel_format
    assert format.num_channels == 0
    assert format.source_speaker_mode is SPEAKERMODE.DEFAULT
    format.num_channels = 2
    echo.channel_format = format
    assert echo.channel_format.num_channels == 2


def test_get_data_parameter_index(echo):
    with pytest.raises(FmodError):
        echo.get_data_parameter_index(DSP_PARAMETER_DATA_TYPE.OVERALLGAIN.value)


def test_idle(echo):
    assert not echo.idle


def test_info(echo):
    assert echo.info.name == b"FMOD Echo"
    assert echo.info.channels == 0


def test_get_input(echo):
    conn = echo.add_input(echo, DSPCONNECTION_TYPE.STANDARD)
    dsp, dsp_conn = echo.get_input(0)
    assert dsp == echo
    assert dsp_conn == conn


def test_input_metering_enabled(initialized_system, echo):
    assert not echo.input_metering_enabled
    echo.input_metering_enabled = True
    assert echo.input_metering_enabled


def test_output_metering_enabled(echo):
    assert not echo.output_metering_enabled
    echo.output_metering_enabled = True
    assert echo.output_metering_enabled


def test_metering_info(echo):
    echo.input_metering_enabled = True
    echo.output_metering_enabled = True
    input, output = echo.metering_info


def test_num_inputs(echo):
    assert echo.num_inputs == 0


def test_num_outputs(echo):
    assert echo.num_outputs == 0


def test_num_parameters(echo):
    assert echo.num_parameters == 4


def test_get_output(echo):
    echo.add_input(echo, DSPCONNECTION_TYPE.STANDARD)
    dsp, dsp_conn = echo.get_output(0)
    assert dsp == echo


def test_output_channel_format(echo):
    format = echo.output_channel_format
    assert format.in_channels == 0


def test_get_set_parameter_bool(compressor):
    val, val_str = compressor.get_parameter_bool(DSP_COMPRESSOR.LINKED)
    assert val
    compressor.set_parameter_bool(DSP_COMPRESSOR.LINKED, False)
    assert not compressor.get_parameter_bool(DSP_COMPRESSOR.LINKED)[0]


def test_get_set_parameter_float(echo):
    val, val_str = echo.get_parameter_float(DSP_ECHO.DELAY)
    assert val == 500.0
    assert val_str == b"500.00"
    echo.set_parameter_float(DSP_ECHO.DELAY, 200.0)
    assert echo.get_parameter_float(DSP_ECHO.DELAY)[0] == 200.0


def test_get_set_parameter_int(oscillator):
    val, val_str = oscillator.get_parameter_int(DSP_OSCILLATOR.TYPE)
    assert val == 0
    oscillator.set_parameter_int(DSP_OSCILLATOR.TYPE, 1)
    assert oscillator.get_parameter_int(DSP_OSCILLATOR.TYPE)[0] == 1


def test_get_parameter_info(echo):
    desc = echo.get_parameter_info(DSP_ECHO.DELAY)
    assert desc.name == b"Delay"


def test_system_object(echo, initialized_system):
    assert echo.system_object == initialized_system


def test_type(echo):
    assert echo.type is DSP_TYPE.ECHO


def test_pre_mix(echo):
    assert echo.pre_mix == 0.0
    echo.pre_mix = 1.0
    assert echo.pre_mix == 1.0


def test_post_mix(echo):
    assert echo.post_mix == 1.0
    echo.post_mix = 2.0
    assert echo.post_mix == 2.0


def test_pre_mix(echo):
    assert echo.dry_mix == 0.0
    echo.dry_mix = 3.0
    assert echo.dry_mix == 3.0


def test_release(echo):
    echo.release()


def test_reset(echo):
    echo.reset()


def test_show_config_dialog(echo):
    with pytest.raises(FmodError) as ex:
        echo.show_config_dialog(None, True)
        assert ex.result is RESULT.UNSUPPORTED
