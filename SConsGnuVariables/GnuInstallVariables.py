"""SConsGnuVariables.GnuInstallVariables

This module provides 'GNU Install Variables', known from automake as a combination
of PRIMARY names, directory prefixes and additional prefixes (the *Uniform
Naming Scheme*). An example of the thing termed here as 'GNU Install Variable'
is ``nobase_include_HEADERS`` or ``bin_PROGRAMS``. This module keeps standard
primary names, directory prefixes, additional prefixes, and combinations of
these in organised fashion.

For related automake information see
<http://www.gnu.org/software/automake/manual/html_node/Uniform.html>
"""
#
# Copyright (c) 2012 by Pawel Tomulik
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE


__docformat__ = 'restructuredText'

_am_additional_prefixes = [
    'dist_',
    'nodist_',
    'nobase_',
    'notrans_'
]

_am_dir_prefixes = [
    'bin',
    'sbin',
    'libexec',
    'dataroot',
    'data',
    'sysconf',
    'sharedstate',
    'localstate',
    'include',
    'oldinclude',
    'doc',
    'info',
    'html',
    'dvi',
    'pdf',
    'ps',
    'lib',
    'lisp',
    'locale',
    'man',
    'pkgdata',
    'pkginclude',
    'pkglib',
    'pkglibexec'
]

_am_primary_dir_prefixes = {
    'PROGRAMS'    : ['bin', 'sbin', 'libexec', 'pkglibexec'],
    'LIBRARIES'   : ['lib', 'pkglib'],
    'LTLIBRARIES' : ['lib'],
    'LISP'        : ['lisp'],
    'PYTHON'      : ['python', 'pkgpython'],
    'JAVA'        : [],
    'SCRIPTS'     : ['bin', 'sbin', 'libexec', 'pkglibexec', 'pkgdata'],
    'DATA'        : ['data', 'sysconf', 'sharedstate', 'localstate', 'pkgdata'],
    'HEADERS'     : ['include', 'oldinclude', 'pkginclude'],
    'MANS'        : ['man'],
    'TEXINFOS'    : ['info'],
    'LOCALES'     : ['locale']
}

for i in range(1,8):
    _am_primary_dir_prefixes['MANS'].append('man%d' % i)

def SupportedPrimaryNames():
    """Return supported GNU PRIMARY install names"""
    return _am_primary_dir_prefixes.keys()

def SupportedDirPrefixes():
    """Return supported GNU directory prefixes"""
    return _am_dir_prefixes

def SupportedAdditionalPrefixes():
    """Return supported additional GNU install prefixes"""
    return _am_additional_prefixes

def SupportedPrimaryDirPrefixes(primary = None):
    """Return allowed dir prefixes for given PRIMARY name"""
    if primary is None:
        return _am_primary_dir_prefixes
    elif primary in _am_primary_dir_prefixes:
        return _am_primary_dir_prefixes[primary]  
    else:
        return []

def SupportedInstallVariables():
    """Return supported install variables (all possible compinations of
    prefixes and PRIMARY names)"""
    variables = []
    priprefixes = SupportedPrimaryDirPrefixes()
    addprefixes = SupportedAdditionalPrefixes()
    for primary, dirprefixes in priprefixes.items():
        for dirprefix in dirprefixes:
            variables.append('%s_%s' % (dirprefix, primary))
            for addprefix in addprefixes:
                variables.append('%s%s_%s' % (addprefix, dirprefix, primary))
    return variables
