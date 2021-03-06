"""Install

The install command creates the .excenturyrc file. This file
is autogenerated and should not be modified manually.

"""

import sys
import site
import textwrap
import os.path as pth
from excentury.command import disp, make_dir, append_variable

DESC = """
Create the excenturyrc file and source it in your .bash_profile or
.bashrc file. This will make sure that you can use the excentury
script and that the excentury libraries are all available to the g++
compiler and the other languages.

"""


def add_parser(subp, raw):
    """Add a parser to the main subparser. """
    subp.add_parser('install', help='install excentury',
                    formatter_class=raw,
                    description=textwrap.dedent(DESC))


def source_excenturyrc():
    """Source the .excenturyrc file in the .bashrc file. """
    make_dir(pth.expandvars('$HOME/.excentury'))
    if sys.platform in ['Darwin', 'darwin']:
        bashrc_path = pth.expandvars('$HOME/.bash_profile')
    else:
        bashrc_path = pth.expandvars('$HOME/.bashrc')
    disp('checking %s ... ' % bashrc_path)
    if pth.exists(bashrc_path):
        expr = [
            'source ~/.excentury/excenturyrc\n',
            'source $HOME/.excentury/excenturyrc\n',
            pth.expandvars('source $HOME/.excentury/excenturyrc\n'),
        ]
        for content_line in open(bashrc_path, 'r'):
            for line in expr:
                if line == content_line:
                    disp('ok\n')
                    return
    with open(bashrc_path, 'a') as content_file:
        disp('\n    including excenturyrc\n')
        content_file.write('source ~/.excentury/excenturyrc\n')


def make_dirs():
    """Creates standard directories to place binaries and libraries
    created by excentury. """
    root = site.getuserbase()
    make_dir(root+'/lib')
    make_dir(root+'/lib/excentury')
    make_dir(root+'/lib/excentury/bin')
    make_dir(root+'/lib/excentury/lib')
    make_dir(root+'/lib/excentury/cpp')
    make_dir(root+'/lib/excentury/matlab')
    make_dir(root+'/lib/excentury/python')
    make_dir(root+'/lib/excentury/tmp')


def excenturyrc_str():
    """Create the excenturyrc file contents. """
    userbase = site.getuserbase()
    content = append_variable('PATH', '%s/bin' % sys.prefix)
    content += append_variable('PATH', '%s/bin' % userbase)
    # include
    path = pth.abspath(pth.dirname(__file__)+'/../extern/include')
    content += append_variable('C_INCLUDE_PATH', path)
    content += append_variable('CPLUS_INCLUDE_PATH', path)
    # matlab
    path = pth.abspath(pth.dirname(__file__)+'/../extern/matlab')
    content += append_variable('MATLABPATH', path)
    # excentury/bin
    content += append_variable('PATH',
                               '%s/lib/excentury/bin' % userbase)
    # excentury/lib
    content += append_variable('LD_LIBRARY_PATH',
                               '%s/lib/excentury/lib' % userbase)
    # excentury/matlab
    content += append_variable('MATLABPATH',
                               '%s/lib/excentury/matlab' % userbase)
    # excentury/python
    content += append_variable('PYTHONPATH',
                               '%s/lib/excentury/python' % userbase)
    return content


def excenturyrc():
    """Create the excenturyrc file. """
    rc_path = pth.expandvars('$HOME/.excentury/excenturyrc')
    disp('writing %s ... ' % rc_path)
    with open(rc_path, 'w') as rcfile:
        rcfile.write(excenturyrc_str())
    disp('done\n')


def run(_):
    """Run the command. """
    source_excenturyrc()
    make_dirs()
    excenturyrc()
