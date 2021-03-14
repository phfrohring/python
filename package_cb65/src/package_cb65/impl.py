"""
package_cb65
============

Problem
-------

1. A brief informal statement of the problem

  - give examples

2. The precise correctness conditions required of a solution


Solution
--------

3. Describe the solution

  - Whenever needed, explain the "why" of the design

"""


# Imports

import argparse as _argparse
import os as _os
import logging as _logging
import subprocess as _sp
from toolz.functoolz import pipe as _pipe
from uuid import uuid4 as _uuid
from pathlib import Path as _Path
import re as _re
import pprint as _pprint
_pf = _pprint.PrettyPrinter(indent=4).pformat
from program_9ef5 import Program, Instruction
_logger = _logging.getLogger(__name__)



# Implementation

def _mkdir(path):
    path.mkdir(mode=0o700, parents=True, exist_ok=False)
    return path


def _mkfile(path, content):
    with path.open(mode='w', encoding='utf-8') as a_file:
        a_file.write(content)
        path.chmod(0o600)

    return path


@Instruction
def _get_deps_path(deps_path):
    return _Path(_os.environ['deps_path'])

@Instruction
def _get_name(name):
    parser = _argparse.ArgumentParser(description='Install user defined packages.')
    arg_name = "component_name"
    parser.add_argument(
        arg_name,
        help="name of the component. Example: a_component",
    )
    return vars(parser.parse_args())[arg_name]

@Instruction
def _get_id(id):
    return str(_uuid()).split('-')[1]

@Instruction
def _get_identifier(name, id, identifier):
    return f"{name}_{id}"


@Instruction
def _build_container(deps_path, identifier, container):
    return _mkdir(deps_path / identifier)


@Instruction
def _build_src(container, src):
    return _mkdir(container / 'src')

@Instruction
def _build_pkg(src, identifier, pkg):
    return _mkdir(src / identifier)

@Instruction
def _build_test(container, test):
    return _mkdir(container / 'test')


@Instruction
def _build_impl(identifier, pkg, impl):
    path = pkg / 'impl.py'
    content = f'''"""
{identifier}
{_re.sub('.', '=', identifier)}

Problem
-------

1. A brief informal statement of the problem

  - give examples

2. The precise correctness conditions required of a solution


Solution
--------

3. Describe the solution

  - Whenever needed, explain the "why" of the design

"""


# Imports

import logging as _logging
_logger = _logging.getLogger(__name__)


# Implementation

def _somethingelse():
    """docstring"""
    return 1


# Interface

def something():
    """docstring"""
    return _somethingelse()
'''

    return _mkfile(path,content)




@Instruction
def _build_init(pkg, init):
    path = pkg / '__init__.py'
    content = f'''"""
__init__
========
"""
__version__ = "1.0.0"

from .impl import *
'''

    return _mkfile(path, content)


@Instruction
def _build_main(identifier, pkg, main):
    path = pkg / '__main__.py'
    content = f'''
# -*- coding: utf-8 -*-


# Import

from {identifier} import something


def main():
    print(something())

# Execution

if __name__ == "__main__":
    main()
'''

    return _mkfile(path, content)



@Instruction
def _build_pyproject(container, pyproject):
    path = container / 'pyproject.toml'
    content = f'''[build-system]
# gives a list of packages that are needed to build your package. Listing something
# here will only make it available during the build, not after it is installed.
requires = [
    "setuptools>=42",
    "wheel"
]
build-backend = "setuptools.build_meta"
'''
    return _mkfile(path, content)



@Instruction
def _build_requirements(container, requirements):
    path = container / 'requirements.txt'
    content = f'''# https://caremad.io/posts/2013/07/setup-vs-requirement/
# -e https://github.com/foo/bar.git#egg=bar
-e .
'''
    return _mkfile(path, content)




@Instruction
def _build_impl_test(identifier, test, impl_test):
    path = test / 'impl_test.py'
    content = f'''# -*- coding: utf-8 -*-

# Imports

from {identifier} import something


# Implementation

def test_impl():
    """docstring"""
    assert something() == 1

'''
    return _mkfile(path, content)


@Instruction
def _build_readme(container, readme):
    path = container / 'README'
    content = 'README'
    return _mkfile(path, content)


@Instruction
def _build_license(container, license):
    path = container / 'LICENSE'
    content = 'https://www.mozilla.org/en-US/MPL/2.0/'
    return _mkfile(path, content)



@Instruction
def _build_setup_cfg(container, identifier, setupcfg):
    path = container / 'setup.cfg'
    content = f'''[metadata]
name = {identifier}
version = 0.0.1
author = Pierre-Henry Fröhring
author_email = contact@phfrohring.com
description = A small example package
long_description = _mkfile: README
long_description_content_type = text/x-rst
url = https://github.com/phfrohring/python
project_urls =
    Bug Tracker = https://github.com/phfrohring/python/issues
classifiers =
    Programming Language :: Python :: 3
    License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)
    Operating System :: OS Independent

[options]
package_dir=
    =src
packages = find:
python_requires = >=3.6
install_requires=

[options.packages.find]
where=src

[options.entry_points]
console_scripts =
    {identifier} = {identifier}.__main__:main
'''

    return _mkfile(path, content)


@Instruction
def _build_setup_py(container, identifier, setuppy):
    path = container / 'setup.py'
    content = f'''import setuptools
setuptools.setup()
'''

    return _mkfile(path, content)

_program = Program(Instruction.all())

# Interface

def build():
    """docstring"""
        # Context of execution
    debug = _os.environ.get('debug') == 'true'
    if debug:
        _logging.basicConfig(level=_logging.DEBUG, force=True, format='%(levelname)s: %(message)s')

    _program.execute()
