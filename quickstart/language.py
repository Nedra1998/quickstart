"""Gets language specific settings"""

import quickstart.console as out
import json
from collections import OrderedDict
from pprint import pprint
import os

global settings
global root_dir

__bin_dir__ = os.path.dirname(__file__)


def load_options(language):
    """Loads json settings for a language"""
    global settings
    with open(os.path.join(__bin_dir__, "languages/", language +
                           ".json")) as datafile:
        settings = json.load(datafile, object_pairs_hook=OrderedDict)


def get_option(data, option):
    """Gets user input for a single option/option group"""
    if isinstance(option, list) is True:
        if option[2] == "__name__":
            if os.path.basename(os.getcwd()).lower() == data['name'].lower():
                option[2] = '.'
            else:
                option[2] = data['name'].lower()
        if option[3] == 'any':
            out.prompt(data, option[0], option[1], option[2], out.allow_empty)
        elif option[3] == 'str':
            out.prompt(data, option[0], option[1], option[2], out.nonempty)
        elif option[3] == 'boolean':
            out.prompt(data, option[0], option[1], option[2], out.boolean)
        elif option[3] == 'path':
            out.prompt(data, option[0], option[1], option[2], out.is_path)
        elif option[3] == 'select_list':
            out.select_list(data, option[0], option[1], option[4], False)
        elif option[3] == 'list':
            out.prompt(data, option[0], option[1], option[2], out.is_list)
    elif isinstance(option, (dict, OrderedDict)) is True:
        if option['check'][0] in data and option['check'][1] == data[option['check']
                                                                     [0]]:
            for opts in option['opts']:
                get_option(data, opts)

def file_name_replace(data, files):
    name_pref = os.path.splitext(data['name'])
    for idx, file in enumerate(files):
        file_list = list(file)
        file_list[1] = file_list[1].replace("__name__", data['name'])
        file_list[1] = file_list[1].replace("__name_abr__", name_pref[0])
        file = tuple(file_list)
        files[idx] = file
    return files

def get_section(data, section):
    """Gets user input for a section of the options"""
    out.section(section, 25)
    for options in settings['Options'][section]:
        get_option(data, options)


def read_options(language, data):
    """Reads user input for options based on language"""
    load_options(language)
    global settings
    out.sub_title(language, 25)
    for section in settings['Options']:
        get_section(data, section)
    return read_data(data)


def read_cmd(data, cmd, files, exes, subs):
    """Reads line of data and sets files/exes/subs accordingly"""
    if isinstance(cmd, list) is True:
        if cmd[0] == "file":
            if cmd[2] != ".":
                path_str = data[cmd[2]]
            else:
                path_str = ""
            files.append((cmd[1], os.path.join(root_dir, path_str, cmd[3])))
        elif cmd[0] == "exe":
            if cmd[2] != ".":
                path_str = data[cmd[2]]
            else:
                path_str = ""
            exes.append("cd {} && {}".format(os.path.join(root_dir, path_str), cmd[1]))
        elif cmd[0] == "sub":
            if cmd[2][0] == '$':
                subs.append((cmd[1], cmd[2][1:]))
            elif cmd[2] == "__title__":
                subs.append((cmd[1], data['name'].title()))
            elif cmd[2] == "__underline__":
                subs.append((cmd[1], "=" * len(data['name'])))
            else:
                subs.append((cmd[1], data[cmd[2]]))
    elif isinstance(cmd, (dict, OrderedDict)) is True:
        if cmd['check'][0] in data and cmd['check'][1] == data[cmd['check'][0]]:
            for cmds in cmd['data']:
                read_cmd(data, cmds, files, exes, subs)


def read_data(data):
    """Reads project generation data based on language and settings"""
    global settings
    global root_dir
    root_dir = os.path.join(os.getcwd(), data['root_dir'])
    files = []
    exes = []
    subs = []
    for cmd in settings['Data']:
        read_cmd(data, cmd, files, exes, subs)
    files = file_name_replace(data, files)
    return files, exes, subs
