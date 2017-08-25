"""Quickstart to create frameworks for projects"""

import console as out

__display_version__ = "v2.0"

_lang = ["C++", "Python", "Bash", "Zsh"]

_options = [('root_path', 'Root Directory', '.',
             out.is_path), ('name', 'Project Name', None, out.nonempty),
            ('git', 'Create Git Repository', 'Yes', out.boolean)]


def SelectLang():
    select = 0
    out.SetCursor(3, 1)
    out.SubTitle("Language", 25)
    for i, x in enumerate(_lang):
        if i == select:
            print("  " + out.reverse(out.magenta("(%i) " % i + x)))
        else:
            print("  " + out.magenta("(%i) " % i + x))
    print(">>\033[1m", end='')
    key = input()
    print("\033[21m")
    if key == '':
        pass
    elif int(key) < len(_lang) and int(key) >= 0:
        select = int(key)
    return _lang[select]


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
        folders, files = languages.cpp.main(data)
    elif data['lang'] == "Python":
        import languages.python
        folders, files = languages.python.main(data)
    else:
        print(out.red("Not a valid type \"%s\"" % lang))
    print(folders)
    print(files)


if __name__ == "__main__":
    main()
