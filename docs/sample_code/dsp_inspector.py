#!/usr/bin/env python

"""Example code to demonstrate how to enumerate loaded plugins and their
parameters.
"""

import curses
import sys
import time
from dataclasses import dataclass

import pyfmodex
from pyfmodex.enums import DSP_PARAMETER_DATA_TYPE, DSP_PARAMETER_TYPE, PLUGINTYPE
from pyfmodex.structures import DSP_DESCRIPTION

MIN_FMOD_VERSION = 0x00020108
MAX_PLUGINS_IN_VIEW = 5
MAX_PARAMETERS_IN_VIEW = 14

# Create a System object and initialize
system = pyfmodex.System()
VERSION = system.version
if VERSION < MIN_FMOD_VERSION:
    print(
        f"FMOD lib version {VERSION:#08x} doesn't meet "
        f"minimum requirement of version {MIN_FMOD_VERSION:#08x}"
    )
    sys.exit(1)
system.init()


@dataclass
class PluginInfo:
    """Convenience class to hold plugin data and register active state."""

    handle: int
    name: str
    desc: DSP_DESCRIPTION


num_plugins = system.get_num_plugins(PLUGINTYPE.DSP)
plugins_desc = []
for index in range(num_plugins):
    handle = system.get_plugin_handle(PLUGINTYPE.DSP, index)
    name = system.get_plugin_info(handle).name
    desc = system.get_dsp_info_by_plugin(handle)
    plugins_desc.append(PluginInfo(handle, name, desc))


def has_data_parameter(description, data_type):
    """Does the given description contain a parameter of the given data_type?"""
    for idx in range(description.numparameters):
        return description.paramdesc[idx].type == DSP_PARAMETER_TYPE.DATA and (
            (data_type >= 0 and description.paramdesc[idx].datadesc.datatype >= 0)
            or description.paramdesc[idx].datadesc.datatype == data_type
        )


def draw_dspinfo(stdscr, plugin_desc):
    """Pretty print the given DSP Info in the given window."""
    stdscr.addstr(
        "-------------------------------------------------\n"
        "\n"
        f"Name (Version) : {plugin_desc.name} ({plugin_desc.version:x})\n"
        f"SDK Version    : {plugin_desc.pluginsdkversion}\n"
        f"Type           : {'Effect' if plugin_desc.numinputbuffers else 'Sound Generator'}\n"
        f"Parameters     : {plugin_desc.numparameters:d}\n"
        f"Audio Calback  : {'process()' if plugin_desc.process else 'read()'}\n"
        "\n"
        " Reset | Side-Chain | 3D | Audibility | User Data\n"
        "   %s  |     %s     | %s |     %s     |     %s\n"
        % (
            "Y" if plugin_desc.reset else "--",
            "Y"
            if has_data_parameter(plugin_desc, DSP_PARAMETER_DATA_TYPE.SIDECHAIN)
            else "--",
            "Y"
            if has_data_parameter(
                plugin_desc, DSP_PARAMETER_DATA_TYPE.THREED_ATTRIBUTES
            )
            or has_data_parameter(
                plugin_desc, DSP_PARAMETER_DATA_TYPE.THREEDATTRIBUTES_MULTI
            )
            else "--",
            "Y"
            if has_data_parameter(plugin_desc, DSP_PARAMETER_DATA_TYPE.OVERALLGAIN)
            else "--",
            "Y"
            if has_data_parameter(plugin_desc, DSP_PARAMETER_DATA_TYPE.USER)
            or plugin_desc.userdata
            else "--",
        )
    )


def plugin_selector(stdscr, activeplugin_idx):
    """Draw a simple TUI, grab keypresses and let the user select a plug-in.

    Returns a string when the state of the TUI should change representing the
    desired state.
    """
    # Show the menu
    stdscr.addstr(
        "Press j to select the next plug-in\n"
        "Press k to select the previous plug-in\n"
        "Press l to view the plug-in parameters\n"
        "Press q to quit",
    )

    while True:
        for i in range(MAX_PLUGINS_IN_VIEW):
            idx = (activeplugin_idx - MAX_PLUGINS_IN_VIEW // 2 + i) % num_plugins
            row = 5 + i

            stdscr.move(row, 0)
            stdscr.clrtoeol()
            if activeplugin_idx == idx:
                stdscr.addstr(">")
            stdscr.addstr(row, 2, plugins_desc[idx].name)

        subscr = stdscr.derwin(row + 2, 0)
        draw_dspinfo(subscr, plugins_desc[activeplugin_idx].desc)

        # Listen to the user
        try:
            keypress = stdscr.getkey()
            if keypress == "j":
                activeplugin_idx = (activeplugin_idx + 1) % num_plugins
            elif keypress == "k":
                activeplugin_idx = (activeplugin_idx - 1) % num_plugins
            elif keypress == "l":
                return "parameter_viewer", activeplugin_idx
            elif keypress == "q":
                return "quit", 0
        except curses.error as cerr:
            if cerr.args[0] != "no input":
                raise cerr


def draw_dspparameters(subscr, scroll, num_parameters, dsp):
    """Pretty print the Parameter Info of the given DSP in the given window."""
    subscr.erase()
    for idx in range(min(num_parameters, MAX_PARAMETERS_IN_VIEW)):
        scrolled_idx = idx + scroll
        param_desc = dsp.get_parameter_info(scrolled_idx)
        subscr.addstr(f"{scrolled_idx:2d}: {param_desc.name.decode():15s} ")
        if param_desc.type == DSP_PARAMETER_TYPE.FLOAT.value:
            val_min = param_desc.desc_union.floatdesc.min
            val_max = param_desc.desc_union.floatdesc.max
            val_def = param_desc.desc_union.floatdesc.defaultval
            val_lab = param_desc.label.decode()
            subscr.addstr(f"[{val_min:g}, {val_max:g}] ({val_def:.2f}{val_lab})")
        elif param_desc.type == DSP_PARAMETER_TYPE.INT.value:
            val_min = param_desc.desc_union.intdesc.min
            val_max = param_desc.desc_union.intdesc.max
            val_def = param_desc.desc_union.intdesc.defaultval
            if param_desc.desc_union.intdesc.valuenames:
                subscr.addstr("[")
                subscr.addstr(
                    ", ".join(
                        [
                            param_desc.desc_union.intdesc.valuenames[i].decode()
                            for i in range(val_max - val_min + 1)
                        ]
                    )
                )
                subscr.addstr("] (")
                subscr.addstr(
                    param_desc.desc_union.intdesc.valuenames[val_def - val_min].decode()
                )
                subscr.addstr(")")
            else:
                val_lab = param_desc.label.decode()
                subscr.addstr(f"[{val_min:d}, {val_max:d}] ({val_def:d}{val_lab})")
        elif param_desc.type == DSP_PARAMETER_TYPE.BOOL.value:
            val_def = param_desc.desc_union.booldesc.defaultval
            if param_desc.desc_union.booldesc.valuenames:
                subscr.addstr("[")
                subscr.addstr(
                    ", ".join(
                        [
                            param_desc.desc_union.booldesc.valuenames[i].decode()
                            for i in (0, 1)
                        ]
                    )
                )
                subscr.addstr("] (")
                subscr.addstr(
                    param_desc.desc_union.booldesc.valuenames[
                        1 if val_def else 0
                    ].decode()
                )
                subscr.addstr(")")
            else:
                lab_def = "On" if val_def else "Off"
                subscr.addstr(f"[On, Off] ({lab_def})")
        elif param_desc.type == DSP_PARAMETER_TYPE.DATA.value:
            subscr.addstr(f"(Data type: {param_desc.desc_union.datadesc.datatype})")

        subscr.addstr("\n")


def parameter_viewer(stdscr, activeplugin_idx):
    """Draw a simple TUI, grab keypresses and let the user browse plug-in
    parameters.

    Returns a string when the state of the TUI should change representing the
    desired state.
    """
    # Show the menu
    stdscr.addstr(
        "Press j to scroll down\n"
        "Press k to scroll up\n"
        "Press h to return to the plug-in list\n"
        "Press q to quit",
    )

    dsp = system.create_dsp_by_plugin(plugins_desc[activeplugin_idx].handle)
    num_parameters = dsp.num_parameters
    scroll = 0

    stdscr.addstr(
        5,
        0,
        f"{dsp.info.name} Parameters:\n"
        "-------------------------------------------------\n",
    )

    stdscr.refresh()
    subscr = stdscr.derwin(7, 0)
    while True:
        draw_dspparameters(subscr, scroll, num_parameters, dsp)

        # Listen to the user
        try:
            keypress = subscr.getkey()
            if keypress == "j":
                if MAX_PARAMETERS_IN_VIEW + scroll < num_parameters:
                    scroll += 1
            elif keypress == "k":
                if scroll > 0:
                    scroll -= 1
            elif keypress == "h":
                dsp.release()
                return "plugin_selector"
            elif keypress == "q":
                dsp.release()
                return "quit"
        except curses.error as cerr:
            if cerr.args[0] != "no input":
                raise cerr


# Main loop
def main(stdscr):
    """Draw a simple TUI with a subwindow containing information based on the
    TUI state.
    """
    stdscr.clear()
    stdscr.nodelay(True)

    # Create small visual display
    stdscr.addstr(
        "==========================\n"
        "Plug-in Inspector Example.\n"
        "=========================="
    )

    stdscr.refresh()
    subscr = stdscr.subwin(4, 0)

    tui_state = "plugin_selector"
    activeplugin_idx = 0
    while True:
        subscr.erase()

        if tui_state == "plugin_selector":
            tui_state, activeplugin_idx = plugin_selector(subscr, activeplugin_idx)
        elif tui_state == "parameter_viewer":
            tui_state = parameter_viewer(subscr, activeplugin_idx)
        else:
            break

        system.update()
        time.sleep(50 / 1000)


curses.wrapper(main)

# Shut down
system.release()
