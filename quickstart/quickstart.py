"""Quickstart to create frameworks for projects"""

import os
from os import path
import quickstart.console as out
import quickstart.language as language
#  import console as out

__display_version__ = "v0.5"

__bin_dir__ = os.path.dirname(__file__)


def mkdir(folder):
    """Creates a new directory at dir"""
    if path.isdir(folder):
        return
    os.makedirs(folder)


def write(source, dest, replace_list):
    """
    Creates a file copied from source to dest, and replaces matches with
    replacement from replace_list
    """
    source = path.join(__bin_dir__, "templates/", source)
    if path.isfile(source):
        with open(source, 'r') as file:
            filedata = file.read()

        for search_str, replace_str in replace_list:
            if isinstance(replace_str, str):
                filedata = filedata.replace(search_str, replace_str)
            elif isinstance(replace_str, list):
                list_str = ''
                for string in replace_str:
                    list_str += ''.join(string) + ' '
                filedata = filedata.replace(search_str, list_str)

        with open(dest, 'w') as file:
            file.write(filedata)
        return True
    else:
        return False

def gen_folder(dest):
    if os.path.exists(os.path.dirname(dest)) is False:
        gen_folder(os.path.dirname(dest))
    os.mkdir(dest)


def gen_files(files, replace):
    """Generates all files for project"""
    out.section("Files", 25)
    for source, dest in files:
        tmp = dest
        if os.path.exists(os.path.dirname(dest)) is False:
            gen_folder(os.path.dirname(dest))
        if write(source, dest, replace) is True:
            print(out.green("Copied ") + out.magenta("\"%s\"" % str(source)))
        else:
            print(
                out.red("File does not exist ") + out.magenta(
                    "\"%s\"" % str(source)))


def gen_commands(commands):
    """Run all commands for project"""
    out.section("Commands", 25)
    for exe in commands:
        os.system(exe)
        print(out.green("Ran ") + out.magenta("\"%s\"" % str(exe)))


def generate(files, commands, replace):
    """Generates project folders/files/commands"""
    out.title("Genrating", 25)
    gen_files(files, replace)
    gen_commands(commands)


def main():
    """allows user to enter data for project, and genorates project"""
    out.clear()
    out.title("Quickstart Utility %s" % __display_version__, 25)
    data = {}
    out.select_list(data, 'lang', "Languages", ["C++", "Python", "Vim"])
    folders = []
    files = []
    print()
    if data['lang'] == "C++":
        files, commands, replace = language.read_options("cpp", data)
    elif data['lang'] == "Python":
        language.read_options("python", data)
    elif data['lang'] == "Vim":
        language.read_options("vim", data)
    else:
        print(out.red("Not a valid language \"{}\"".format(data['lang'])))

    generate(files, commands, replace)


if __name__ == "__main__":
    main()
