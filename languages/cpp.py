import console as out
import os
from os import path


def load_files(data):
    source_dir = path.join(data['root'], data['source_dir'])
    include_dir = path.join(data['root'], data['include_dir'])
    build_dir = path.join(data['root'], data['build_dir'])
    ext_dir = path.join(data['root'], data['ext_dir'])
    folders = [data['root'], source_dir, include_dir, build_dir, ext_dir]
    files = [('cpp/source/main.cpp', path.join(source_dir, 'main.cpp'))]
    commands = []
    replace = [("project_name", data['name']), ("project_title",
                                                data['name'].title()),
               ("project_description",
                data['description']), ("project_type",
                                       data['type']), ("project_source_dir",
                                                       data['source_dir']),
               ("project_include_dir",
                data['include_dir']), ("project_build_dir",
                                       data['build_dir']), ("project_ext_dir",
                                                            data['ext_dir'])]
    if data['git'] is True:
        commands.append("cd %s && git init" % data['root'])
        files.append(("cpp/.gitignore", path.join(data['root'], ".gitignore")))
        if data['tests'] is True:
            commands.append(
                "git submodule add https://github.com/google/googletest %s/googletest"
                % ext_dir)

    if data['tests'] is True:
        test_dir = path.join(data['root'], data['test_dir'])
        folders.append(test_dir)
        files.append(("cpp/test/tmp.cpp", path.join(test_dir, "tmp.cpp")))
        files.append(("cpp/external/Makefile_t", path.join(ext_dir,
                                                           "Makefile")))
        replace.append(("project_test_dir", data['test_dir']))
    else:
        files.append(("cpp/external/Makefile", path.join(ext_dir, "Makefile")))

    if data['docs'] is True:
        doc_dir = path.join(data['root'], data['doc_dir'])
        folders.append(doc_dir)
        replace.append(("project_doc_dir", data['doc_dir']))
        if data['doc-sys'] == "MkDocs":
            files.append(('cpp/mkdocs.yml', path.join(data['root'],
                                                      'mkdocs.yml')))
            files.append(('cpp/docs/index.md', path.join(doc_dir, 'index.md')))
        elif data['doc-sys'] == "Sphinx":
            pass

    if data['comp'] == "GNU Make":
        files.append(("cpp/Makefile", path.join(data['root'], "Makefile")))
        files.append(("cpp/source/Makefile", path.join(source_dir, "Makefile")))
        if data['tests'] is True:
            files.append(("cpp/test/Makefile", path.join(
                data['root'], data['test_dir'], "Makefile")))

    if data['ci'] is True:
        ciFile = ["cpp/", ""]
        if data['ci-server'] == "Travis-CI":
            ciFile[0] += "travis"
            ciFile[1] = path.join(data['root'], ".travis.yml")

        if data['deploy-pages'] is True:
            ciFile[0] += "_dp"

        if data['coverage'] == "CodeCov":
            ciFile[0] += "_cc"
            files.append(("cpp/.codecov.yml", path.join(data['root'],
                                                        ".codecov.yml")))
        ciFile[0] += ".yml"
        files.append(ciFile)

    return folders, files, commands, replace


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
