# Cli #

---

[![GitHub
Tag](https://img.shields.io/github/tag/LuxAtrumStudio/cli.svg)](https://github.com/LuxAtrumStudio/cli)
[![Github
Release](https://img.shields.io/github/downloads/LuxAtrumStudio/cli/latest/total.svg)](https://github.com/LuxAtrumStudio/cli)

[![Build
Status](https://img.shields.io/travis/LuxAtrumStudio/cli.svg)](https://travis-ci.org/LuxAtrumStudio/cli)
[![Code
Coverage](https://img.shields.io/codecov/c/github/LuxAtrumStudio/cli/development.svg)](https://codecov.io/gh/LuxAtrumStudio/cli)
[![Code
Quality](https://img.shields.io/codacy/grade/7d61e50c1bf64718af41de3e04d6dff9.svg)](https://www.codacy.com/app/LuxAtrumStudio.cli)

---

## Introduction ##

[**CLI**](index.md) (Command line interface) is a group of header only files, that
are designed create a simpler interface for `C++` with the terminal. Each
portion is separated into individual header files, so only the desired
functionalities are included, through including the associated header file.

The different modules included are:

* [`any_type.hpp`](ref/any.md): A class that can be used to represent
    most basic types including `bool`, `int`, `double`, `float`, `char`, `const
    char*`, and `std::string`.
* [`parser.hpp`](ref/parser.md): A class that can be used to read and parse the
    input arguments provided by the command line (**Note:** [`Any`](ref/any.md)
    is required).
