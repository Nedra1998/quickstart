"""Loads default values for Python projects"""

import os
from os import path
import quickstart.console as out

#  import console as out

source_dir = ""


def git_setting(data, folders, files, commands, replace):
    commands.append("cd %s && git init" % data['root'])
    files.append(("python/.gitignore", path.join(data['root'], ".gitignore")))


def test_setting(data, folders, files, commands, replace):
    """Sets test settings if enbabled"""
    test_dir = path.join(source_dir, 'test')
    folders.append(test_dir)
    files.append(("python/test/__init__.py", path.join(test_dir,
                                                       "__init__.py")))


def doc_setting(data, folders, files, commands, replace):
    doc_dir = path.join(data['root'], 'doc')
    folders.append(doc_dir)
    if data['doc-sys'] == "Sphinx":
        folders.append(path.join(doc_dir, 'source'))
        folders.append(path.join(doc_dir, 'source', '_static'))
        files.append(('python/docs/Makefile', path.join(doc_dir, 'Makefile')))
        files.append(('python/docs/source/conf.py', path.join(
            doc_dir, 'source', 'conf.py')))
        files.append(('python/docs/source/index.rst', path.join(
            doc_dir, 'source', 'index.rst')))
        if "sphinx" not in data['pip-install']:
            data['pip-install'].append("sphinx")


def ci_settings(data, folders, files, commands, replace):
    ci_file = ["python/", ""]
    if data['ci-server'] == "Travis-CI":
        ci_file[0] += "travis"
        ci_file[1] = path.join(data['root'], ".travis.yml")

    if data['deploy-pages'] is True:
        ci_file[0] += "_dp"

    if data['coverage'] == "CodeCov":
        ci_file[0] += "_cc"
        files.append(("python/.codecov.yml", path.join(data['root'],
                                                       ".codecov.yml")))

        ci_file[0] += ".yml"
    files.append(ci_file)

    project_apt = "- sudo apt-get install "
    if data['apt-install'] == []:
        project_apt = ""
    else:
        for pack in data['apt-install']:
            project_apt += str(pack) + ' '

    replace.append(("project_apt", str(project_apt)))

    project_pip = "- sudo pip install "
    if data['pip-install'] == []:
        project_pip = ""
    else:
        for pack in data['pip-install']:
            project_pip += str(pack) + ' '

    replace.append(("project_pip", str(project_pip)))


def load_files(data):
    """Sets folders, files, replacement strings and commands"""
    global source_dir
    source_dir = path.join(data['root'], data['name'])

    folders = [data['root'], source_dir]
    files = [('python/source.py', path.join(
        source_dir, data['name'] + ".py")), ('python/__init__.py', path.join(
            source_dir, "__init__.py")), ('python/setup.py', path.join(
                data['root'], "setup.py")), ('python/README.rst', path.join(
                    data['root'], "README.rst"))]
    commands = []
    replace = []
    replace.append(("project_name", data['name']))
    replace.append(("project_title", data['name'].title()))
    replace.append(("project_underline", "=" * len(data['name'])))
    replace.append(("project_description", data['description']))

    if data['git'] is True:
        git_setting(data, folders, files, commands, replace)

    if data['tests'] is True:
        test_setting(data, folders, files, commands, replace)

    if data['docs'] is True:
        doc_setting(data, folders, files, commands, replace)

    if data['ci'] is True:
        ci_settings(data, folders, files, commands, replace)

    return folders, files, commands, replace


def main(data):
    """Prompts user for missing data for python projects"""
    out.sub_title("Python", 25)
    out.section("General", 25)
    out.prompt(data, 'name', 'Project name', None, out.nonempty)
    out.prompt(data, 'description', 'Project description', None,
               out.allow_empty)
    out.prompt(data, 'git', 'Create git repo', 'Yes', out.boolean)
    out.section("Directories", 25)
    current_dir = path.basename(os.getcwd())
    if current_dir.lower() == data['name'].lower():
        out.prompt(data, 'root', 'Root directory', '.', out.is_path)
    else:
        out.prompt(data, 'root', 'Root directory', data['name'].lower(),
                   out.is_path)

    out.section("Unit Tests", 25)
    out.prompt(data, 'tests', 'Enable unit tests', 'Yes', out.boolean)
    out.section("Documentation", 25)
    out.prompt(data, 'docs', 'Create documentation', 'Yes', out.boolean)
    if data['docs'] is True:
        out.select_list(data, 'doc-sys', 'Documentation Constructor',
                        ['Sphinx', 'None'], False)
    out.section("Continuous Integration", 25)
    out.prompt(data, 'ci', 'Enable continuous integration', 'Yes', out.boolean)
    if data['ci'] is True:
        out.select_list(data, 'ci-server', 'Continuous Integration Server',
                        ['Travis-CI'], False)
        out.prompt(data, 'deploy-pages', 'Auto deploy Github pages', 'Yes',
                   out.boolean)
        out.prompt(data, 'apt-install', 'Install from apt-get', '', out.is_list)
        out.prompt(data, 'pip-install', 'Install from pip', '', out.is_list)
        out.select_list(data, 'coverage', "Code Coverage", ['CodeCov', 'None'],
                        False)
        print()
    return load_files(data)


def default(data):
    """Creates project with default settings"""
    data['description'] = ''
    data['type'] = 'lib'
    data['git'] = True
    data['source_dir'] = 'source'
    data['include_dir'] = 'include'
    data['build_dir'] = 'build'
    data['ext_dir'] = 'external'
    data['tests'] = True
    data['test_dir'] = 'test'
    data['docs'] = True
    data['doc_dir'] = 'doc'
    data['doc-sys'] = 'MkDocs'
    data['comp'] = 'GNU Make'
    data['ci'] = True
    data['ci-server'] = 'Travis-CI'
    data['deploy-pages'] = True
    data['apt-install'] = []
    data['pip-install'] = []
    data['coverage'] = 'CodeCov'
    return main(data)
