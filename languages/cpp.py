import console as out
import os
from os import path


def load_files(data):
    source_dir = path.join(data['root'], data['source_dir'])
    include_dir = path.join(data['root'], data['include_dir'])
    test_dir = path.join(data['root'], data['test_dir'])
    build_dir = path.join(data['root'], data['build_dir'])
    ext_dir = path.join(data['root'], data['ext_dir'])
    doc_dir = path.join(data['root'], data['doc_dir'])
    folders = [source_dir, include_dir, build_dir, ext_dir]
    if data['tests'] is True:
        folders.append(test_dir)
    if data['docs'] is True:
        folders.append(doc_dir)

    files = [('main.cpp', path.join(source_dir, 'main.cpp'))]
    return folders, files


def main(data):
    out.SubTitle("C++", 25)
    out.Section("General", 25)
    out.Prompt(data, 'name', 'Project name', None, out.nonempty)
    out.Prompt(data, 'description', 'Project description', None,
               out.allow_empty)
    out.Prompt(data, 'type', 'Project type (lib/exe)', 'lib', out.is_type)
    out.Prompt(data, 'git', 'Create git repo', 'Yes', out.boolean)
    out.Section("Directories", 25)
    currentDir = os.path.basename(os.path.dirname(os.path.realpath(__file__)))
    if currentDir.lower() == data['name'].lower():
        out.Prompt(data, 'root', 'Root directory', '.', out.is_path)
    else:
        out.Prompt(data, 'root', 'Root directory', data['name'].lower(),
                   out.is_path)
        out.Prompt(data, 'source_dir', 'Source directory', 'source',
                   out.is_path)
    out.Prompt(data, 'include_dir', 'Include directory', 'include', out.is_path)
    out.Prompt(data, 'build_dir', 'Build directory', 'build', out.is_path)
    out.Prompt(data, 'ext_dir', 'External directory', 'external', out.is_path)
    out.Section("Unit Tests", 25)
    out.Prompt(data, 'tests', 'Enable unit tests', 'Yes', out.boolean)
    if data['tests'] is True:
        out.Prompt(data, 'test_dir', 'Test directory', 'test', out.is_path)
    out.Section("Documentation", 25)
    out.Prompt(data, 'docs', 'Create documentation', 'Yes', out.boolean)
    if data['docs'] is True:
        out.SelectList(data, 'doc-sys', 'Documentation Constructor',
                       ['MkDocs', 'Sphinx', 'None'], False)
        out.Prompt(data, 'doc_dir', 'Documentation directory', 'docs',
                   out.is_path)
        out.Section("Compiling", 25)
    out.SelectList(data, 'comp', 'Compiler', ['GNU Make'], False)
    out.Prompt(data, 'link', 'Lined libraries', '', out.is_list)
    out.Section("Continuous Integration", 25)
    out.Prompt(data, 'ci', 'Enable continuous integration', 'Yes', out.boolean)
    if data['ci'] is True:
        out.SelectList(data, 'ci-server', 'Continuous Integration Server',
                       ['Travis-CI'], False)
        out.Prompt(data, 'deploy-pages', 'Auto deploy Github pages', 'Yes',
                   out.boolean)
        out.Prompt(data, 'apt-install', 'Install from apt-get', '', out.is_list)
        out.Prompt(data, 'pip-install', 'Install from pip', '', out.is_list)
        out.SelectList(data, 'coverage', "Code Coverage", ['CodeCov', 'None'],
                       False)
        print()
    return load_files(data)
