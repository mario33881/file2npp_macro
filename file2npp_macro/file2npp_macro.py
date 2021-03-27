#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FILE2NPP_MACRO:
This script converts the content of a file
into a macro for notepad++.

I suggest you to check if you have already
assigned the hotkey to a command before
putting the output macro inside the shortcuts.xml file.

Please specify:
* <input>: input file path
* <output>: output file path
* <name>: name of the macro
* <key>: key to press to execute the macro
* A combination of --shift --alt --ctrl if the shift and/or alt and/or
  ctrl key need to be pressed at the same time as the <key> key to execute the macro

Usage:
  file2npp_macro.py <input> <output> <name> <key> [--shift|--alt|--ctrl]
  file2npp_macro.py -h | --help
  file2npp_macro.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  --shift       Hotkey needs the shift key.
  --alt         Hotkey needs the alt key.
  --ctrl        Hotkey needs the ctrl key.
"""
import html
import string
import os

import lxml.etree
import lxml.builder
import docopt

from _version import __version__

E = lxml.builder.ElementMaker()

digits_ascii = [c for c in string.digits + string.ascii_lowercase]

valid_keys = [
        {"key": "backspace", "code": 8},
        {"key": "tab", "code": 9},
        {"key": "enter", "code": 13},
        {"key": "esc", "code": 27},
        {"key": "spacebar", "code": 32},
        {"key": "page_up", "code": 33},
        {"key": "page_down", "code": 34},
        {"key": "end", "code": 35},
        {"key": "home", "code": 36},
        {"key": "left", "code": 37},
        {"key": "up", "code": 38},
        {"key": "right", "code": 39},
        {"key": "down", "code": 40},
        {"key": "ins", "code": 45},
        {"key": "del", "code": 46},
        {"key": "numpad_0", "code": 96},
        {"key": "numpad_1", "code": 97},
        {"key": "numpad_2", "code": 98},
        {"key": "numpad_3", "code": 99},
        {"key": "numpad_4", "code": 100},
        {"key": "numpad_5", "code": 101},
        {"key": "numpad_6", "code": 102},
        {"key": "numpad_7", "code": 103},
        {"key": "numpad_8", "code": 104},
        {"key": "numpad_9", "code": 105},

        {"key": "num_*", "code": -2},
        {"key": "num_+", "code": -2},
        {"key": "num_-", "code": -2},
        {"key": "num_.", "code": -2},
        {"key": "num_/", "code": -2},

        {"key": "f1", "code": 112},
        {"key": "f2", "code": 113},
        {"key": "f3", "code": 114},
        {"key": "f4", "code": 115},
        {"key": "f5", "code": 116},
        {"key": "f6", "code": 117},
        {"key": "f7", "code": 118},
        {"key": "f8", "code": 119},
        {"key": "f9", "code": 120},
        {"key": "f10", "code": 121},
        {"key": "f11", "code": 122},
        {"key": "f12", "code": 123},

        {"key": "~", "code": -2},
        {"key": "-", "code": -2},
        {"key": "=", "code": -2},
        {"key": "[", "code": -2},
        {"key": "]", "code": -2},
        {"key": ";", "code": -2},
        {"key": "'", "code": -2},
        {"key": "\\", "code": -2},
        {"key": ",", "code": -2},
        {"key": ".", "code": -2},
        {"key": "/", "code": -2},
        {"key": "<>", "code": -2},
        ]


def attribute(key, value):
    """
    Makes an attribute for lxml.

    "key"="value"

    :param str key: key of the attribute
    :param str value: value of the attribute
    :return dict attr: attribute for lxml
    """
    attr = {key: value}
    return attr


def read_file(t_file):
    """
    Reads the <t_file> file and yields one line at a time.
    :param str t_file: path to a file to read
    :yield str line: read line
    """
    with open(t_file, "r") as f:
        line = f.readline()

        while line != "":
            yield line
            line = f.readline()


def make_action(t_key):
    """
    Makes an Action element.

    These elements correspond to one keypress.

    A generic Action element is:

    <Action type="1" message="2170" wParam="0" lParam="0" sParam="{{ key }}" />

    Where:
    * {{ key }} is the pressed key (<t_key>)

    > Everything else seems always set to the same values

    :param str t_key: key that is pressed/simulated
    :return E action_el: lxml element, Action element
    """
    action = E.Action
    action_el = action(
        attribute("type", "1"),
        message="2170",
        wParam="0",
        lParam="0",
        sParam=t_key
        )

    return action_el


def make_macro(t_file, t_name, t_ctrl_flag, t_alt_flag, t_shift_flag, t_key):
    """
    Makes a Macro element with the Actions.

    This is a generic Macro element
    <Macro name="{{ name }}" Ctrl="{{ ctrl }}" Alt="{{ alt }}" Shift="{{ shift }}" Key="{{ key_code }}">

    Where:
    * {{ name }} is the name of macro (<t_name>)
    * {{ ctrl }} = yes if the ctrl key is part of the hotkey (<t_ctrl_flag> = True)
                   no if it is not part of the hotkey (<t_ctrl_flag> = False)
    * {{ alt }} = yes if the alt key is part of the hotkey
                  no if it is not part of the hotkey (<t_alt_flag> = False)
    * {{ shift }} = yes if the shift key is part of the hotkey (<t_alt_flag> = True)
                    no if it is not part of the hotkey (<t_shift_flag> = False)
    * {{ key_code }} is the code that corresponds to a key (the key is <t_key>)

    :param str t_file: file to convert to a macro
    :param str t_name: name of the macro
    :param bool t_ctrl_flag: True = the Ctrl key is part of the hotkey
    :param bool t_alt_flag: True = the Alt key is part of the hotkey
    :param bool t_shift_flag: True = the Shift key is part of the hotkey
    :param str t_key: key that is part of the hotkey
    :return E macro_el: lxml element, Macro element
    """

    macro = E.Macro

    # convert booleans to the
    # corresponding string accepted by notepad++:
    # True is "yes", False is "no"

    ctrl = "no"
    if t_ctrl_flag:
        ctrl = "yes"

    alt = "no"
    if t_alt_flag:
        alt = "yes"

    shift = "no"
    if t_shift_flag:
        shift = "yes"

    # get the code corresponding to the key
    key = str(key_to_code(t_key))

    # make the macro element:
    #
    # <Macro name="{{ name }}" Ctrl="{{ ctrl }}" Alt="{{ alt }}" Shift="{{ shift }}" Key="{{ key_code }}">
    #
    # Where:
    # * {{ name }} is the name of macro (<t_name>)
    # * {{ ctrl }} = yes if the ctrl key is part of the hotkey (<t_ctrl_flag> = True)
    #                no if it is not part of the hotkey (<t_ctrl_flag> = False)
    # * {{ alt }} = yes if the alt key is part of the hotkey
    #               no if it is not part of the hotkey (<t_alt_flag> = False)
    # * {{ shift }} = yes if the shift key is part of the hotkey (<t_alt_flag> = True)
    #                 no if it is not part of the hotkey (<t_shift_flag> = False)
    # * {{ key_code }} is the code that corresponds to a key (the key is <t_key>)

    macro_el = macro(
        name=t_name,
        Ctrl=ctrl,
        Alt=alt,
        Shift=shift,
        Key=key
        )

    # read <t_file> file line by line
    for line in read_file(t_file):
        # read char by char
        for char in line:
            if char == "\n":
                # newline corresponds to two actions: "&#x000D;" and "&#x000A;"
                action = make_action("&#x000D;")
                macro_el.append(action)

                action = make_action("&#x000A;")
                macro_el.append(action)
            else:
                # A char corresponds to one action
                action = make_action(char)
                macro_el.append(action)

    return macro_el


def write_macros(t_file, t_macros_el):
    """
    Writes the Macros element <t_macros_el>
    to the <t_file> file.

    :param str t_file: output file path
    :param E t_macros_el: lxml element (Macros)
    """
    with open(t_file, "wb") as f:
        f.write(lxml.etree.tostring(t_macros_el, pretty_print=True).decode('utf-8').replace("&amp;", "&").encode('ascii', 'xmlcharrefreplace'))


def key_to_code(t_key):
    """
    Converts a key to the corresponding code
    for notepad++ hotkey.

    :param str t_key: hotkey
    :return int code: hotkey key code
    """
    code = -1
    i = 0

    while code < 0 and i < len(valid_keys):
        if valid_keys[i]["key"] == t_key.lower().replace(" ", "_"):
            code = valid_keys[i]["code"]
        else:
            if t_key in digits_ascii:
                code = ord(t_key)
        i += 1

    return code


if __name__ == "__main__":

    arguments = docopt.docopt(__doc__, version=__version__)

    key_code = key_to_code(arguments["<key>"])

    if key_code >= 0:
        if os.path.isfile(arguments["<input>"]):
            print("Converting input file to a macro...")

            macro_el = make_macro(
                arguments["<input>"],
                arguments["<name>"],
                arguments["--ctrl"],
                arguments["--alt"],
                arguments["--shift"],
                arguments["<key>"]
                )

            print("Preparing macros element...")
            macros = E.Macros
            macros_el = macros(
                macro_el
                )

            if os.path.isfile(arguments["<output>"]):
                r = ""
                while r.lower() not in ["y", "n", "ye", "yes", "no"]:
                    print("Output file already exists...")
                    r = input("Do you want to overwrite its content? [y/n] ")

                    if r.lower() not in ["y", "n", "ye", "yes", "no"]:
                        print("Invalid option")

                if r in ["y", "ye", "yes"]:
                    print("Writing to output file... ", end="")
                    write_macros(arguments["<output>"], macros_el)
                    print(" Done")
                else:
                    print("Ending script.")
            else:
                print("Writing to output file... ", end="")
                write_macros(arguments["<output>"], macros_el)
                print(" Done")
        else:
            print("Input file '", arguments["<input>"], "' doesn't exist", sep="")

    elif key_code == -1:
        print("This key is not supported by notepad++, please change it")

    elif key_code == -2:
        print("This key is currently not supported by " + __file__.strip(".py") + ", please change it")
        print("> Or, if you are a developer, you can help to support it by contributing to the source code here:")
        print("> https://github.com/mario33881/" + __file__.strip(".py"))
