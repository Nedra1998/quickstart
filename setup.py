#!/usr/bin/python3

import json
import sys
import os
import subprocess

import pprint

# TODO: Test nested validation in file formatting.

def select(title, prompt, options, default=-1):
    print(title)
    id_len = int(len(options) / 10)
    options.append("quit")
    for i, opt in enumerate(options):
        print("\033[1;30m{:{}})\033[0m {}".format(i+1, id_len, opt))
    while True:
        try:
            num = input(prompt)
            if num == "" and default != -1:
                print("{}".format("\033[A\033[2K") * (len(options) + 2))
                if title.endswith(':'):
                    print("\033[A{}\033[0;1m{}\033[0m".format(title, options[default]))
                else:
                    print("\033[A{}\033[0;1m  {}\033[0m".format(title, options[default]))
                return options[default]
            num = int(num)
        except ValueError:
            continue
        except:
            sys.exit(0)
        if 0 < num < len(options):
            print("{}".format("\033[A\033[2K") * (len(options) + 2))
            if title.endswith(':'):
                print("\033[A{}\033[0;1m{}\033[0m".format(title, options[num-1]))
            else:
                print("\033[A{}\033[0;1m  {}\033[0m".format(title, options[num-1]))
            return options[num-1]
        elif num == len(options):
            sys.exit(0)

def get_val(key, vtype, attrs = [], default=None):
    while True:
        try:
            if default is not None:
                val = input("    \033[1;92m{}\033[1;95m[{}]\033[1;92m:\033[0;1m ".format(key, default))
            else:
                val = input("    \033[1;92m{}:\033[0;1m".format(key))
            if val == "" and default is not None:
                if 'REQUIRED' in attrs and default == "":
                    print("    This property is required")
                    continue
                return default
            return vtype(val)
        except ValueError:
            continue
        except:
            sys.exit(0)

def get_bool(key, default=None):
    while True:
        if default is not None:
            val = input("    \033[1;92m{}\033[1;95m[{}]\033[1;92m:\033[0;1m".format(key, "True" if default else "False"))
        else:
            val = input("    \033[1;92m{}:\033[0;1m".format(key))
        if val == "" and default is not None:
            return default
        elif val.lower() in ('no', 'n', 'f', 'false'):
            return False
        elif val.lower() in ('yes', 'y', 't', 'true'):
            return True

def extract_val(key, data, delim='@'):
    current = key.split(delim)[0]
    key = delim.join(key.split(delim)[1:])
    if current in data:
        if isinstance(data[current], dict) and key:
            return extract_val(key, data[current], delim)
        return data[current]
    return None

def set_val(key, data, val, delim='@'):
    current = key.split(delim)[0]
    key = delim.join(key.split(delim)[1:])
    if current in data and key and isinstance(data[current], dict):
        set_val(key, data[current], val, delim)
    elif key:
        data[current] = {}
        set_val(key, data[current], val, delim)
    else:
        data[current] = val


def verify(expression, data):
    terms = [x.split('||') for x in expression.split('&&')]
    res = []
    for term in terms:
        term_res = []
        for state in term:
            if '!=' in state:
                var, val = state.split('!=')
            else:
                var, val = state.split('=')
            var = extract_val(var, data, '.')
            if var and isinstance(var, bool):
                var = "true" if var else "false"
            if ('!=' in state and var and var != val) or ('=' in state and var and var == val):
                term_res.append(True)
                break
            term_res.append(False)
        res.append(any(term_res))
        return all(res)

def flatten_obj(key, data):
    if isinstance(data, list):
        res = {}
        for i in range(len(data)):
            if key == '':
                res = {**res, **flatten_obj("{}".format(i), data[i])}
            else:
                res = {**res, **flatten_obj("{}.{}".format(key, i), data[i])}
        return res
    elif isinstance(data, dict):
        res = {}
        for ky in data.keys():
            if key == '':
                res = {**res, **flatten_obj("{}".format(ky), data[ky])}
            else:
                res = {**res, **flatten_obj("{}.{}".format(key, ky), data[ky])}
        return res
    else:
        return {key: data}

def replace_str(key, data):
    flattend = flatten_obj('', data)
    for ids in flattend.keys():
        if '{{' + ids + '}}' in key:
            key = key.replace('{{' + ids + '}}', flattend[ids])
        if '{{ ' + ids + ' }}' in key:
            key = key.replace('{{ ' + ids + ' }}', flattend[ids])
    return key

def format_block(idx, src_lines, data):
    lines = []
    i = idx+1
    while i < len(src_lines):
        if src_lines[i].startswith("{%") and src_lines[i].endswith("%}"):
            if src_lines[i] == "{% end %}":
                return i, lines
            if verify(src_lines[i].strip("{%").strip("%}").strip(), data):
                i, tmp = format_block(i, src_lines, data)
                lines += tmp
            else:
                i, _ = format_block(i, src_lines, data)
        else:
            lines.append(src_lines[i])
        i += 1
    return len(src_lines), lines

def format_file(source, dest, data):
    with open(source, 'r') as in_file:
        src_lines = [x.rstrip('\n') for x in in_file.readlines()];
    lines = []
    i = 0;
    while i < len(src_lines):
        print(src_lines[i])
        if src_lines[i].startswith("{%") and src_lines[i].endswith("%}"):
            if verify(src_lines[i].strip("{%").strip("%}").strip(), data):
                i, tmp = format_block(i, src_lines, data)
                lines += tmp
            else:
                i, _ = format_block(i, src_lines, data)
        else:
            lines.append(src_lines[i])
        i += 1
    out_lines = "\n".join(lines)
    out_lines = replace_str(out_lines, data)
    with open(dest, 'w') as out_file:
        out_file.write(out_lines)

def get_props(data, root, section, base):
    print("  \033[1;36m{}\033[0m".format(section))
    data_dict = extract_val(root, base)
    keys = list(data_dict.keys())
    for key in keys:
        if "=" in key:
            expression, name = key.split(':')
            if verify(expression, base):
                if isinstance(data_dict[key], dict):
                    set_val(data + '@' + name, base, get_props(data + '@' + name, root + '@' + key, section + '.' + name, base))
                elif isinstance(data_dict[key], list):
                    set_val(data + '@' + name, base, select('    \033[1;92m{}\033[1;95m[{}]\033[1;92m:\033[0m'.format(key, data_dict[key][0]), "\033[90m>>\033[0m ", data_dict[key], 0))
                elif isinstance(data_dict[key], bool):
                    set_val(data + '@' + name, base, get_bool(name, data_dict[key]))
                else:
                    attrs = []
                    if ';' in name:
                        attrs = name.split(';')[:-1]
                        name = name.split(';')[-1]
                    set_val(data + '@' + name, base, get_val(name, type(data_dict[key]), attrs, data_dict[key]))
        else:
            if isinstance(data_dict[key], dict):
                set_val(data + '@' + key, base, get_props(data + '@' + key, data + '@' + key, section + '.' + key, base))
            elif isinstance(data_dict[key], list):
                set_val(data + '@' + key, base, select('    \033[1;92m{}\033[1;95m[{}]\033[1;92m:\033[0m'.format(key, data_dict[key][0]), "\033[90m>>\033[0m ", data_dict[key], 0))
            elif isinstance(data_dict[key], bool):
                set_val(data + '@' + key, base, get_bool(key, data_dict[key]))
            else:
                if ';' in key:
                    attrs = key.split(';')[:-1]
                    dest = key.split(';')[-1]
                    set_val(data + '@' + dest, base, get_val(dest, type(data_dict[key]), attrs, data_dict[key]))
                else:
                    set_val(data + '@' + key, base, get_val(key, type(data_dict[key]), [], data_dict[key]))
    return extract_val(data, base)

def exec_cmds(data, title, base):
    if isinstance(data, list):
        for cmd in data:
            if isinstance(cmd, str):
                cmd =replace_str(cmd, base)
                print("\033[92m  Executing {}...\033[0m".format(cmd))
                subprocess.run(['cd {} && {}'.format(title, cmd)], shell=True)
            elif isinstance(cmd, dict):
                exec_cmds(cmd, title, base)
    elif isinstance(data, dict):
        for key in data.keys():
            if '=' in key and verify(key, base):
                if isinstance(data[key], str):
                    cmd = replace_str(data[key], base)
                    print("\033[92m  Executing {}...\033[0m".format(cmd))
                    subprocess.run(['cd {} && {}'.format(title, cmd)], shell=True)
                elif isinstance(data[key], dict) or isinstance(data[key], list):
                    exec_cmds(data[key], title, base)

def copy_files(data, title, root_dir, base):
    keys = list(data.keys())
    for key in keys:
        if "=" in key:
            expression, name = key.split(':')
            if verify(expression, base):
                if isinstance(data[key], dict):
                    copy_files(data[key], title, root_dir, base)
                else:
                    dest = replace_str(name, base)
                    print("\033[92m  Creating {}...\033[0m".format(dest))
                    format_file("{}/{}".format(root_dir, data[key]), "{}/{}".format(title, dest), base)
        else:
            if isinstance(data[key], dict):
                copy_files(data[key], title, root_dir, base)
            else:
                dest = replace_str(key, base)
                print("\033[92m  Creating {}...\033[0m".format(dest))
                format_file("{}/{}".format(root_dir, data[key]), "{}/{}".format(title, dest), base)



def main():
    templates = list(os.listdir('./templates/'))
    if len(sys.argv) >= 2 and sys.argv[1] in templates:
        template = sys.argv[1]
    else:
        template=select("\033[1;36mSelect template\033[0m", "\033[90m>>\033[0m ", templates)
    with open('./templates/{}/cfg.json'.format(template), 'r') as load:
        data=json.load(load)
    print("\033[0;34mOptions\033[0m")
    data['props'] = get_props('props', 'props', 'Properties', data)
    pprint.pprint(data)
    os.mkdir('./{}/'.format(data['props']['NAME'].lower()))
    if 'pre_cmds' in data:
        print("\033[0;34mPre Commands\033[0m")
        exec_cmds(data['pre_cmds'], data['props']['NAME'], data)
    if 'cmds' in data:
        print("\033[0;34mCommands\033[0m")
        exec_cmds(data['cmds'], data['props']['NAME'], data)
    if 'files' in data:
        print("\033[0;34mFiles\033[0m")
        copy_files(data['files'], data['props']['NAME'], './templates/{}'.format(template), data)
    if 'post_cmds' in data:
        print("\033[0;34mPost Commands\033[0m")
        exec_cmds(data['post_cmds'], data['props']['NAME'], data)

if __name__ == "__main__":
    main()
