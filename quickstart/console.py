"""Module controls input/output to terminal"""

import subprocess
from os import path
import sys, tty, termios


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


def is_list(x):
    x = [str(y) for y in x.split()]


def Title(text, size=-1):
    print(white(bold(text)))
    if size != -1:
        print(white(bold("=" * size)))
    else:
        print(white(bold("=" * len(text))))


def SubTitle(text, size=-1):
    print(white(text))
    if size != -1:
        print(white("-" * size))
    else:
        print(white("-" * len(text)))


def Section(text, size=-1):
    if size != -1 and size > len(text):
        width = int((size - len(text)) / 2)
        print(cyan("\n" + '=' * width + text + '=' * width + "\n"))
    else:
        print(cyan(text))


def term_input(prompt):
    print(prompt, end='')
    print('\033[1m', end='')
    out = input('')
    print('\033[21m', end='')
    return out


def Prompt(data, name, description, default=None, validator=nonempty, indent=0):
    if name in data:
        print(' ' * indent + bold(description + ': %s' % data[name]))
    else:
        while True:
            if default is not None:
                prompt = ' ' * indent + '%s [%s]: ' % (description, default)
            else:
                prompt = ' ' * indent + description + ': '
            prompt = prompt.encode('utf-8')
            prompt = magenta(prompt.decode("utf-8"))
            x = term_input(prompt).strip()
            if default and not x:
                x = default
            try:
                x = validator(x)
            except ValidationError as err:
                print(' ' * indent + bold(red('* ' + str(err))))
                continue
            break
        if x is default or x is True or x is False:
            print("\033[1A\r", end='')
            if default is not None:
                if x is True:
                    print(' ' * indent + magenta(
                        "%s [%s]: " % (description, default)) + bold("Yes"))
                elif x is False:
                    print(' ' * indent + magenta(
                        "%s [%s]: " % (description, default)) + bold("No"))
                else:
                    print(' ' * indent + magenta(
                        "%s [%s]: " % (description, default)) + bold("%s" % x))
            else:
                if x is True:
                    print(' ' * indent + magenta("%s: " % description) +
                          bold("True"))
                elif x is False:
                    print(' ' * indent + magenta("%s: " % description) +
                          bold("False"))
                else:
                    print(' ' * indent + magenta("%s: " % description) + bold(
                        "%s" % x))
        data[name] = x


def SelectList(data, name, title, options, show_title=True):
    select = 0
    if show_title is True:
        SubTitle(title, 25)
    if show_title is False:
        print(magenta(title))
    running = True
    while running is True:
        for i, x in enumerate(options):
            if i == select:
                print("  " + reverse(magenta("(%i) " % i + x)))
            else:
                print("  " + magenta("(%i) " % i + x))
        print(">>\033[1m", end='')
        key = input()
        print("\033[21m")
        if key == '':
            running = False
        elif int(key) < len(options) and int(key) >= 0:
            select = int(key)
        if running is True:
            for i in range(0, len(options) + 2):
                print("\033[1A\r" + ' ' * 25 + '\r', end='')
    if show_title is False:
        for i in range(0, len(options) + 3):
            print("\033[1A\r" + ' ' * 25 + '\r', end='')
        print(magenta("%s [%s]: " % (title, options[0])) +
              bold(white("%s" % options[select])))
    else:
        for i in range(0, len(options) + 2):
            print("\033[1A\r" + ' ' * 25 + '\r', end='')
        for i, x in enumerate(options):
            if i == select:
                print("  " + bold(white("(%i) %s" % (i, x))))
            else:
                print("  " + magenta("(%i) %s" % (i, x)))
    data[name] = options[select]


def SetCursor(line, col):
    print("\033[%i;%iH" % (line, col))


def Clear():
    subprocess.call("clear", shell=True)


def CreateAttr(name):

    def inner(text):
        return "\033[%s" % _attrs[name][0] + text + "\033[%s" % _attrs[name][1]

    globals()[name] = inner


def CreateColor(name):

    def inner(text):
        return "\033[%s" % _colors[name][0] + text + "\033[%s" % _colors[name][1]

    globals()[name] = inner


_attrs = {
    'bold': ('01m', '21m'),
    'dim': ('02m', '22m'),
    'underlined': ('03m', '24m'),
    'blink': ('05m', '25m'),
    'reverse': ('07m', '27m'),
    'hidden': ('08m', '28m')
}

_colors = {
    'red': ('31m', '39m'),
    'green': ('32m', '39m'),
    'yellow': ('33m', '39m'),
    'blue': ('34m', '39m'),
    'magenta': ('35m', '39m'),
    'cyan': ('36m', '39m'),
    'grey': ('27m', '39m'),
    'white': ('97m', '39m')
}

for _name in _attrs:
    CreateAttr(_name)
for _name in _colors:
    CreateColor(_name)


class _Getch:

    def __call__(self, count):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(count)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


getch = _Getch()
