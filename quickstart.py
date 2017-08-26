"""Quickstart to create frameworks for projects"""

import os
from os import path
import console as out

__display_version__ = "v0.3"


def mkdir(dir):
    if path.isdir(dir):
        return
    os.makedirs(dir)


def write(source, dest, replace_list):
    with open(source, 'r') as file:
        filedata = file.read()

    for search_str, replace_str in replace_list:
        filedata = filedata.replace(search_str, replace_str)

    with open(dest, 'w') as file:
        file.write(filedata)


def gen_folders(folders):
    out.Section("Folders", 25)
    for path in folders:
        mkdir(path)
        print(out.green("Generated ") + out.magenta("\"%s\"" % path))


def gen_files(files):
    out.Section("Files", 25)
    for source, dest in files:
        print(out.green("Copied ") + out.magenta("\"%s\"" % str(source)))


def gen_commands(commands):
    out.Section("Commands", 25)
    for exe in commands:
        print(out.green("Ran ") + out.magenta("\"%s\"" % str(exe)))


def generate(files, folders, commands, replace):
    out.Title("Genrating", 25)
    gen_folders(folders)
    gen_files(files)
    gen_commands(commands)


def main():
    out.Clear()
    out.Title("Quickstart Utility %s" % __display_version__, 25)
    data = {}
    out.SelectList(data, 'lang', "Languages", ["C++", "Python"])
    folders = []
    files = []
    print()
    if data['lang'] == "C++":
        import languages.cpp
        folders, files, commands, replace = languages.cpp.main(data)
    elif data['lang'] == "Python":
        import languages.python
        #  folders, files, commands = languages.python.main(data)
    else:
        print(out.red("Not a valid type \"%s\"" % lang))

    generate(files, folders, commands, replace)


if __name__ == "__main__":
    main()
