"""Gets language specific settings"""

import quickstart.console as out
import json
from collections import OrderedDict
from pprint import pprint
import os

global settings

__bin_dir__ = os.path.dirname(__file__)


def load_options(language):
    """Loads json settings for a language"""
    global settings
    with open(os.path.join(__bin_dir__, "languages/", language + ".json")) as datafile:
        settings = json.load(datafile, object_pairs_hook=OrderedDict)


def get_option(data, option):
    """Gets user input for a single option/option group"""
    if isinstance(option, list) is True:
        if(option[3] == 'any'):
            out.prompt(data, option[0], option[1], option[2], out.allow_empty)
        elif(option[3] == 'str'):
            out.prompt(data, option[0], option[1], option[2], out.nonempty)
        elif(option[3] == 'boolean'):
            out.prompt(data, option[0], option[1], option[2], out.boolean)
        elif(option[3] == 'path'):
            out.prompt(data, option[0], option[1], option[2], out.is_path)
        elif(option[3] == 'select_list'):
            out.select_list(data, option[0], option[1], option[4], False)
    elif isinstance(option, (dict, OrderedDict)) is True:
        if option['check'][0] in data and option['check'][1] == data[option['check'][0]]:
            for opts in option['opts']:
                get_option(data, opts)


def get_section(data, section):
    """Gets user input for a section of the options"""
    out.section(section, 25)
    for options in settings['Options'][section]:
        get_option(data, options)

def read_options(language):
    """Reads user input for options based on language"""
    load_options(language)
    global settings
    data = {}
    out.sub_title(language, 25)
    for section  in settings['Options']:
        get_section(data, section)
