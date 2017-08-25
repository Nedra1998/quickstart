#!/usr/bin/python3

#  import sys, getopt
import fileinput
import sys
import optparse
import os
from os import path

bin_dir = os.path.dirname(__file__)


class style:
    normal = '\033[0m'

    class attr:
        bold = '\033[1m'
        dim = '\033[2m'
        underlined = '\033[4m'
        blink = '\033[5m'
        reverse = '\033[7m'
        hidden = '\033[8m'

    class reset:
        bold = '\033[21m'
        dim = '\033[22m'
        underlined = '\033[24m'
        blink = '\033[25m'
        reverse = '\033[27m'
        hidden = '\033[28m'

    class fg:
        default = '\033[39m'
        black = '\033[30m'
        red = '\033[31m'
        green = '\033[32m'
        yellow = '\033[33m'
        blue = '\033[34m'
        magenta = '\033[35m'
        cyan = '\033[36m'
        grey = '\033[37m'
        dark_grey = '\033[90m'
        white = '\033[97m'

        class light:
            red = '\033[91m'
            green = '\033[92m'
            yellow = '\033[93m'
            blue = '\033[94m'
            magenta = '\033[95m'
            cyan = '\033[96m'

    class bg:
        default = '\033[349m'
        black = '\033[40m'
        red = '\033[41m'
        green = '\033[42m'
        yellow = '\033[43m'
        blue = '\033[44m'
        magenta = '\033[45m'
        cyan = '\033[46m'
        grey = '\033[47m'
        dark_grey = '\033[100m'
        white = '\033[107m'

        class light:
            red = '\033[101m'
            green = '\033[102m'
            yellow = '\033[103m'
            blue = '\033[104m'
            magenta = '\033[105m'
            cyan = '\033[106m'


__display_version__ = '0.2'


def write(str, style_list=['']):
    list_str = ''.join(style_list)
    print(list_str + str + style.normal)


def term_input(prompt):
    print(prompt, end='')
    print(style.attr.bold, end='')
    out = input('')
    print(style.normal, end='')
    return out


class ValidationError(Exception):
    """Raised for validation errors."""


def is_path(x):
    x = path.expanduser(x)
    if path.exists(x) and not path.isdir(x):
        raise ValidationError("Please enter a valid path name.")
    return x


def allow_empty(x):
    return x


def nonempty(x):
    if not x:
        raise ValidationError("Please enter some text.")
    return x


def boolean(x):
    if x.upper() not in ('Y', 'YES', 'N', 'NO'):
        raise ValidationError("Please enter either 'y' or 'n'.")
    return x.upper() in ('Y', 'YES')


def is_type(x):
    if x.upper() not in ('LIB', 'EXE'):
        raise ValidationError("Pleasse enter either 'lib' or 'exe'.")
    return x


def do_prompt(d, name, description, default=None, validator=nonempty):
    if name in d:
        print(style.attr.bold + description + ': %s' % d[name] + style.normal)
    else:
        while True:
            if default is not None:
                prompt = '%s [%s]: ' % (description, default)
            else:
                prompt = description + ': '
            prompt = prompt.encode('utf-8')
            prompt = style.fg.magenta + prompt.decode("utf-8") + style.normal
            x = term_input(prompt).strip()
            if default and not x:
                x = default
            try:
                x = validator(x)
            except ValidationError as err:
                print(style.fg.red + style.attr.bold + '* ' + str(err) +
                      style.normal)
                continue
            break
        d[name] = x


def get_values(d):
    print(style.attr.bold + 'Welcome to the Quickstart utility.' + style.normal)
    print('''
Please enter values for the following settings (just press Enter to
accept a default value, if one is given in brackets).\n''')
    print(style.fg.cyan + '\n=====Basic Options=====\n' + style.normal)
    do_prompt(d, 'path', 'Root project path', '.', is_path)
    do_prompt(d, 'project', 'Project name')
    do_prompt(d, 'type', 'Project Type (lib/exe)', 'lib', is_type)
    do_prompt(d, 'git', 'Create git repo (y/n)', 'y', boolean)
    do_prompt(d, 'author', 'Author of project')
    do_prompt(d, 'version', 'Version of project', '1.0.0', allow_empty)
    print(style.fg.cyan + '\n=====Directory configuration=====\n' +
          style.normal)
    do_prompt(d, 'source_dir', 'Source directory', 'source')
    do_prompt(d, 'include_dir', 'Include directory', 'include')
    do_prompt(d, 'build_dir', 'Build directory', 'build')
    do_prompt(d, 'ext_dir', 'External directory', 'external')
    do_prompt(d, 'test_dir', 'Test directory', 'test')
    do_prompt(d, 'doc_dir', 'Documentation directory', 'docs')
    print(style.fg.cyan + '\n=====Build configuration=====\n' + style.normal)
    do_prompt(d, 'linker', 'Linked libraries', '', allow_empty)
    do_prompt(d, 'travis-ci', 'Create travis-ci integration (y/n)', 'y',
              boolean)
    do_prompt(d, 'codecov', 'Create codecov integration (y/n)', 'y', boolean)
    do_prompt(d, 'mkdocs', 'Create mkdocs documentation (y/n)', 'y', boolean)
    print(style.fg.cyan + '\n=====Description=====\n' + style.normal)
    do_prompt(d, 'description', 'Brief project description', None, allow_empty)
    for key in ('project', 'author', 'version'):
        d[key + '_str'] = d[key].replace('\\', '\\\\').replace("'", "\\'")


def mkdir(dir):
    if path.isdir(dir):
        return
    os.makedirs(dir)


def write_file(fpath, tpath, d):
    fpath = path.join(d['path'], fpath)
    tpath = path.join(bin_dir, 'templates/', tpath)
    replace_list = [['project_name', d['project_str']], [
        'project_title', d['project_str'].title()
    ], ['project_description',
        d['description']], ['project_source_dir', d['source_dir']], [
            'project_test_dir', d['test_dir']
        ], ['project_build_dir',
            d['build_dir']], ['project_external_dir',
                              d['ext_dir']], ['project_doc_dir', d['doc_dir']],
                    ['project_include_dir', d['include_dir']],
                    ['project_link', d['linker']], ['project_type', d['type']]]

    with open(tpath, 'r') as file:
        filedata = file.read()

    for search_str, replace_str in replace_list:
        filedata = filedata.replace(search_str, replace_str)

    with open(fpath, 'w') as file:
        file.write(filedata)


def generate(d):
    d['linker'] = "-l" + d['linker']
    source_dir = path.join(d['path'], d['source_dir'])
    include_dir = path.join(d['path'], d['include_dir'])
    build_dir = path.join(d['path'], d['build_dir'])
    docs_dir = path.join(d['path'], d['doc_dir'])
    test_dir = path.join(d['path'], d['test_dir'])
    ext_dir = path.join(d['path'], d['ext_dir'])
    mkdir(source_dir)
    mkdir(include_dir)
    mkdir(build_dir)
    mkdir(docs_dir)
    mkdir(test_dir)
    mkdir(ext_dir)

    write_file('README.md', 'README_t.md', d)
    write_file('.gitignore', 'gitignore_t', d)
    write_file('Makefile', 'Makefile_t', d)
    write_file(path.join(d['source_dir'], 'Makefile'), 'source/Makefile_t', d)
    write_file(path.join(d['source_dir'], 'main.cpp'), 'source/main_t.cpp', d)
    write_file(path.join(d['ext_dir'], 'Makefile'), 'external/Makefile_t', d)
    write_file(path.join(d['test_dir'], 'Makefile'), 'test/Makefile_t', d)
    write_file(
        path.join(d['test_dir'], 'test_tmp.cpp'), 'test/test_tmp_t.cpp', d)
    if d['travis-ci'] is True:
        write_file('.travis.yml', 'travis_t.yml', d)
    if d['codecov'] is True:
        write_file('.codecov.yml', 'codecov_t.yml', d)
    if d['mkdocs'] is True:
        write_file('mkdocs.yml', 'mkdocs_t.yml', d)
        write_file(path.join(d['doc_dir'], 'index.md'), 'docs/index_t.md', d)
    if d['git'] is True:
        os.system('git init ' + d['path'])
        os.system(
            'cd ' + d['path'] +
            ' && git submodule add https://github.com/google/googletest.git ' +
            path.join(d['ext_dir'], 'googletest'))


def main():
    parser = optparse.OptionParser(
        version='Quickstart V%s' % __display_version__)

    group = parser.add_option_group('Project basic options')
    group.add_option(
        '-r', '--root', metavar='PATH', dest='path', help='root project path')
    group.add_option(
        '-p',
        '--project',
        metavar='PROJECT',
        dest='project',
        help='project name')
    group.add_option(
        '--type', metavar='TYPE', dest='type', help='project type(lib/exe)')
    group.add_option(
        '-g',
        '--git',
        action='store_true',
        dest='git',
        default=False,
        help='Creates git repository')
    group.add_option(
        '-a', '--author', metavar='AUTHOR', dest='author', help='author names')
    group.add_option(
        '-v', metavar='VERSION', dest='version', help='version of project')
    group = parser.add_option_group('Directory configuration')
    group.add_option(
        '-s',
        '--source',
        metavar='PATH',
        dest='source_dir',
        help='path to source directory')
    group.add_option(
        '-i',
        '--include',
        metavar='PATH',
        dest='include_dir',
        help='path to include directory')
    group.add_option(
        '-b',
        '--build',
        metavar='PATH',
        dest='build_dir',
        help='path to build directory')
    group.add_option(
        '-d',
        '--doc',
        metavar='PATH',
        dest='doc_dir',
        help='path to documentation directory')
    group.add_option(
        '-t',
        '--test',
        metavar='PATH',
        dest='test_dir',
        help='path to test directory')
    group.add_option(
        '-e',
        '--external',
        metavar='PATH',
        dest='ext_dir',
        help='path to externals directory')
    group = parser.add_option_group('Build configuration')
    group.add_option(
        '-l', '--link', metavar='LINK', dest='linker', help='linked libraries')
    group.add_option(
        '--travis',
        action='store_true',
        dest='travis-ci',
        default=False,
        help='Create Travis-ci integration')
    group.add_option(
        '--cov',
        action='store_true',
        dest='codecov',
        default=False,
        help='Create CodeCov integration')
    group.add_option(
        '--mkdocs',
        action='store_true',
        dest='mkdocs',
        default=False,
        help='Creates mkdocs documentation')

    try:
        opts, args = parser.parse_args(sys.argv[1:])
    except SystemExit as err:
        return err.code

    d = vars(opts)
    d = dict((k, v) for k, v in d.items() if not (v is None or v is False))
    try:
        get_values(d)
    except (KeyboardInterrupt, EOFError):
        print()
        print(style.attr.bold + style.fg.red + '[Interrupted]' + style.normal)
        return 130
    generate(d)


if __name__ == "__main__":
    main()
