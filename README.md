# FILE2NPP_MACRO

This is a Python script that converts a file content
into a macro for Notepad++.

> I suggest you to check if you have already
> assigned the hotkey on notepad++ to a command before
> putting the macro inside the ```%appdata%\Notepad++\shortcuts.xml``` file.

> Close and then re-open notepad++ to be able to use the macro.

> Check the ```examples``` folder to see some examples of usage.

## Index
* [Usage](#usage)
* [Description](#description-)
* [Requirements](#requirements-)
* [Changelog](#changelog-)
* [Author](#author-)

## Usage

First you need to execute the script:

    file2npp_macro.py <input> <output> <name> <key> [--shift|--alt|--ctrl]
    file2npp_macro.py -h | --help
    file2npp_macro.py --version

    Options:
    -h --help     Show this screen.
    --version     Show version.
    --shift       Hotkey needs the shift key.
    --alt         Hotkey needs the alt key.
    --ctrl        Hotkey needs the ctrl key.

The parameters are:
* ```<input>```: input file path
* ```<output>```: output file path
* ```<name>```: name of the macro
* ```<key>```: key to press to execute the macro
* A combination of ```--shift```, ```--alt```, ```--ctrl``` if the shift and/or alt and/or 
  ctrl key need to be pressed at the same time as the ```<key>``` key to execute the macro

The output file has this format:

```xml
<Macros>    
    <Macro name="my_macro" Ctrl="no" Alt="yes" Shift="no" Key="76">
        <Action type="1" message="2170" wParam="0" lParam="0" sParam="" />
        ...
        <Action type="1" message="2170" wParam="0" lParam="0" sParam="" />
    </Macro>
</Macros>
```

The next thing to do is to open the file that contains the macros:

    %appdata%\Notepad++\shortcuts.xml

Add the ```<Macro></Macro>``` element (with its content) 
to the ```<Macros></Macros>``` element inside the file.

Close and then re-open notepad++ to be able to use the macro.

Check the ```examples``` folder to see some examples of usage.

[Go to the index](#index)

## Description ![](https://i.imgur.com/wMdaLI0.png)

The script:
1. Parses the parameters
2. Checks if the input file exists
3. Calls the ```make_macro()``` function to create the ```<Macro>``` element:

    make_macro(t_file, t_name, t_ctrl_flag, t_alt_flag, t_shift_flag, t_key)

    Makes a Macro element with the Actions.

    This is a generic Macro element
    ```<Macro name="{{ name }}" Ctrl="{{ ctrl }}" Alt="{{ alt }}" Shift="{{ shift }}" Key="{{ key_code }}">```
    
    Where:
    * ```{{ name }}``` is the name of macro (```<t_name>```)
    * ```{{ ctrl }}``` = yes if the ctrl key is part of the hotkey (```<t_ctrl_flag>``` = True)

      ```{{ ctrl }}``` = no if it is not part of the hotkey (```<t_ctrl_flag>``` = False)

    * ```{{ alt }}``` = yes if the alt key is part of the hotkey

      ```{{ alt }}``` = no if it is not part of the hotkey (```<t_alt_flag>``` = False)
    * ```{{ shift }}``` = yes if the shift key is part of the hotkey (```<t_alt_flag>``` = True)

      ```{{ shift }}``` = no if it is not part of the hotkey (```<t_shift_flag>``` = False)
    * ```{{ key_code }}``` is the code that corresponds to a key (the key is ```<t_key>```)
        
            :param str t_file: file to convert to a macro
            :param str t_name: name of the macro
            :param bool t_ctrl_flag: True = the Ctrl key is part of the hotkey
            :param bool t_alt_flag: True = the Alt key is part of the hotkey
            :param bool t_shift_flag: True = the Shift key is part of the hotkey
            :param str t_key: key that is part of the hotkey
            :return E macro_el: lxml element, Macro element
    
    This function calls the ```key_to_code()``` function to convert ```<t_key>``` to a code
    that is recognized by notepad++:

        key_to_code(t_key)
    
    Converts a key to the corresponding code
    for notepad++ hotkey.

        :param str t_key: hotkey
        :return int code: hotkey key code
    
    Then the ```make_macro()``` calls the ```read_file()``` to read each
    line of the input file to thenpass each character 
    to ```make_action()``` to make the ```<Action>```
    and appends the returned elements inside the ```<Macro>``` element:
    
        make_action(t_key):
    
    Makes an Action element.

    These elements correspond to one keypress.

    A generic Action element is:

    ```<Action type="1" message="2170" wParam="0" lParam="0" sParam="{{ key }}" />```

    Where:
    * ```{{ key }}``` is the pressed key (```<t_key>```)

    > Everything else seems always set to the same values

        :param str t_key: key that is pressed/simulated
        :return E action_el: lxml element, Action element
    
    ```
    read_file(t_file)
    ```
    
    Reads the ```<t_file>``` file and yields one line at a time.
    
        :param str t_file: path to a file to read
        :yield str line: read line

4. Puts the ```<Macro>``` element inside a ```<Macros>``` element.
5. Calls the ```write_macros()``` function to write the ```<Macros>``` element to the output file.
    > If the output file already exist the script asks if you want to overwrite its content

        write_macros(t_file, t_macros_el)

    Writes the Macros element ```<t_macros_el>```
    to the ```<t_file>``` file.

        :param str t_file: output file path
        :param E t_macros_el: lxml element (Macros)

The ```attribute()``` function is used by the ```make_action()``` function:

    attribute(key, value)

Makes an attribute for lxml.

```"key"="value"```

    :param str key: key of the attribute
    :param str value: value of the attribute
    :return dict attr: attribute for lxml

[Go to the index](#index)

## Requirements ![](https://i.imgur.com/H3oBumq.png)
* Python 3
* docopt library (command line parameters manager)
* lxml library (xml parser/builder)

[Go to the index](#index)

## Changelog ![](https://i.imgur.com/SDKHpak.png)

### 2020-03-21 01_01
First version

[Go to the index](#index)

## Author ![](https://i.imgur.com/ej4EVF6.png)
[Stefano Zenaro (mario33881)](https://github.com/mario33881)
