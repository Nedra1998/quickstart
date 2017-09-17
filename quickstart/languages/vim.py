"""Loads default values for a Vim script project"""

import os
from os import path
import quickstart.console as out


def git_setting(data, folders, files, commands, replace):
    """Creates a git project at root dir"""
    commands.append("cd %s && git init" % data['root'])
    files.append(("vim/.gitignore", path.join(data['root'], ".gitignore")))


def load_files(data):
    """Sets folders, files, replacement strings and commands"""
    root = data['root']
    folders = [data['root']]
    files = []
    commands = []
    replace = []
    replace.append(("project_name", data['name']))
    replace.append(("project_title", data['name'].title()))
    replace.append(("project_underline", "=" * len(data['name'])))
    replace.append(("project_description", data['description']))
    name, ext = path.splitext(data['name'])
    if ext == '.vim':
        data['name'] = name
    if data['syntax'] is True:
        folders.append(path.join(root, "syntax"))
        files.append(('vim/syntax/tmp.vim', path.join(root, 'syntax',
                                                      data['name'] + ".vim")))
    if data['ftdetect'] is True:
        folders.append(path.join(root, "ftdetect"))
        files.append(('vim/ftdetect/tmp.vim', path.join(root, 'syntax',
                                                        data['name'] + ".vim")))
    if data['ftplugin'] is True:
        folders.append(path.join(root, "ftplugin"))
        folders.append(path.join(root, "ftplugin", data['name']))
        files.append(('vim/ftplugin/tmp/tmp.vim', path.join(
            root, 'ftplugin', data['name'], data['name'] + ".vim")))
    if data['indent'] is True:
        folders.append(path.join(root, "indent"))
        #  files.append(('vim/indent/tmp.vim', path.join(root, 'syntax',
    #  data['name'] + ".vim")))
    if data['autoload'] is True:
        folders.append(path.join(root, "autoload"))
    if data['doc'] is True:
        folders.append(path.join(root, "doc"))
        files.append(('vim/doc/tmp.txt', path.join(root, 'doc',
                                                   data['name'] + ".txt")))
    return folders, files, commands, replace


def main(data):
    """Prompts user for missing data for Vim script projects"""
    out.sub_title("Vim Script", 25)
    out.section("General", 25)
    out.prompt(data, 'name', 'Project name', None, out.nonempty)
    out.prompt(data, 'description', 'Project description', None,
               out.allow_empty)
    out.prompt(data, 'git', 'Create git repo', 'Yes', out.boolean)
    current_dir = path.basename(os.getcwd())
    if current_dir.lower() == data['name'].lower():
        out.prompt(data, 'root', 'Root directory', '.', out.is_path)
    else:
        out.prompt(data, 'root', 'Root directory', data['name'].lower(),
                   out.is_path)
    out.section("Sections", 25)
    out.prompt(data, 'syntax', 'Create syntax', 'Yes', out.boolean)
    out.prompt(data, 'ftdetect', 'Create file type detection', 'Yes',
               out.boolean)
    out.prompt(data, 'ftplugin', 'Create file type plugin', 'Yes', out.boolean)
    out.prompt(data, 'indent', 'Create indentaton', 'Yes', out.boolean)
    out.prompt(data, 'autoload', 'Create autoload', 'Yes', out.boolean)
    out.prompt(data, 'doc', 'Create documentation', 'Yes', out.boolean)
    return load_files(data)
