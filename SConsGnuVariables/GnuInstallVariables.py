"""SConsGnuVariables.GnuInstallVariables

This module provides 'GNU Install Variables' similar to these known from
automake (see automake documentation, `The Uniform Naming Scheme`_ and `What
Gets Installed`_). An example of the 'GNU Install Variable' is
``nobase_include_HEADERS`` or ``bin_PROGRAMS``. This module keeps standard
primary names, directory prefixes, additional prefixes, and combinations of
these. The module also provides functions for filtering collections of variable
names and extracting the names that should be handled by ``install-exec`` and
``install-data`` targets (see `The Two Parts of Install`_).

For related automake information see
<http://www.gnu.org/software/automake/manual/html_node/Uniform.html>

.. _The Uniform Naming Scheme: http://www.gnu.org/software/automake/manual/automake.html#Uniform
.. _What Gets Installed: http://www.gnu.org/software/automake/manual/automake.html#Install
.. _The Two Parts of Install: http://www.gnu.org/software/automake/manual/automake.html#The-Two-Parts-of-Install
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

import re

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

_am_install_data_prefixes = [ 
  'data',
  'info',
  'man',
  'include',
  'oldinclude',
  'pkgdata',
  'pkginclude'
]

_am_install_exec_prefixes = [
  'bin',
  'sbin',
  'libexec',
  'sysconf',
  'localstate',
  'lib',
  'pkglib'
]

_am_user_defined_dir_prefixes = [ ]

for i in range(1,9):
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

def extract_dir_prefix(var):
    parts = var.split('_')
    if len(parts) == 2:
        prefix = parts[0]
    elif len(parts) == 3:
        prefix = parts[1]
    else:
        raise RuntimeError('malformed install variable name: %s' % var)
    return prefix
    
__re_exec_dirprefix = re.compile('^(?:[a-zA-Z][a-zA-Z0-9]*)?exec[a-zA-Z0-9]*$')
def is_user_defined_exec_dir_prefix(prefix,**kw):
    try:
        if not (prefix in kw['dir_prefixes']):
            return False
    except KeyError:
        return False 
    return (__re_exec_dirprefix.match(prefix) is not None)

def is_exec_dir_prefix(prefix,**kw):
    if prefix in SupportedDirPrefixes():
        return (prefix in _am_install_exec_prefixes)
    else:
        return is_user_defined_exec_dir_prefix(prefix,**kw)
        
def is_data_dir_prefix(prefix,**kw):
    if prefix in SupportedDirPrefixes():
        return (prefix in _am_install_data_prefixes)
    else:
        return (not is_user_defined_exec_dir_prefix(prefix,**kw))

def is_exec_install_var(amvar,**kw):
    return is_exec_dir_prefix(extract_dir_prefix(amvar,**kw))

def is_data_install_var(amvar,**kw):
    return is_data_dir_prefix(extract_dir_prefix(amvar,**kw))

def FilterExecInstallVars(amvars,**kw):
    """Extract GNU install variable names that should go to ``install-exec``

    :Parameters:
        amvars
            collection of GNU install variable names,

    :Keywords:
        kw['dir_prefixes']
            collection of  user-defined directory prefixes
    
    :Return:
        returns list of variable names that should be handled by
        ``install-exec``

    **Example usage:**

    .. python::
        exec_vars = FilterExecInstallVars(['bin_PROGRAMS', 'lib_LIBRARIES',
                                           'nobase_include_HEADERS',
                                           'sysconf_DATA'])
        # exec_vars is now [ 'bin_PROGRAMS', 'lib_LIBRARIES' ]
    """
    return [amvar for amvar in amvars if is_exec_install_var(amvar,**kw)]
  
def FilterDataInstallVars(amvars,**kw):
    """Extract GNU install variable names that should go to ``install-data``

    :Parameters:
        amvars
            collection of GNU install variable names,

    :Keywords:
        kw['dir_prefixes']
            collection of user-defined directory prefixes
    
    :Return:
        returns list of variable names that should be handled by
        ``install-data``

    **Example usage:**

    .. python::
        data_vars = FilterDataInstallVars(['bin_PROGRAMS', 'lib_LIBRARIES',
                                           'nobase_include_HEADERS',
                                           'sysconf_DATA'])
        # data_vars is now [ 'nobase_include_HEADERS', 'sysconf_DATA' ]
    """
    return [amvar for amvar in amvars if is_data_install_var(amvar,**kw)]

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
