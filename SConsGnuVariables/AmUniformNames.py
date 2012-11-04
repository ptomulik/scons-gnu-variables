"""SConsGnuVariables.AmUniformNames

This module provides a kind of 'Automake Uniform Naming', an idea similar to
that known from automake (see automake documentation, `The Uniform Naming
Scheme`_ and `What Gets Installed`_). An example of the 'Automake Uniform
Name' is ``nobase_include_HEADERS`` or ``bin_PROGRAMS``. This module keeps
standard primary names, directory prefixes, additional prefixes, and
combinations of these. The module also provides functions for filtering
collections of variable names and extracting the names that should be handled
by ``install-exec`` and ``install-data`` targets (see `The Two Parts of
Install`_). There are also several other functions that may be used to 
manipulate uniform names.

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


__docformat__ = 'restructuredText'

_am_additional_prefixes = [
    'dist',
    'nodist',
    'nobase',
    'notrans'
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

def standard_primary_names():
    return _am_primary_dir_prefixes.keys()

def standard_dir_prefixes():
    return _am_dir_prefixes

def standard_additional_prefixes():
    return _am_additional_prefixes

def standard_primary_dir_prefixes(primary = None):
    if primary is None:
        return _am_primary_dir_prefixes
    elif primary in _am_primary_dir_prefixes:
        return _am_primary_dir_prefixes[primary]  
    else:
        return []

def standard_uniform_names():
    variables = []
    priprefixes = standard_primary_dir_prefixes()
    addprefixes = standard_additional_prefixes()
    for primary, dirprefixes in priprefixes.items():
        for dirprefix in dirprefixes:
            variables.append('%s_%s' % (dirprefix, primary))
            for addprefix in addprefixes:
                variables.append('%s_%s_%s' % (addprefix, dirprefix, primary))
    return variables

def _prepare_dir_prefixes_list(dir_prefixes, use_std_dir_prefixes):
    if dir_prefixes is None:
        dir_prefixes = []
    else:
        dir_prefixes = list(dir_prefixes)
    if use_std_dir_prefixes:
        dir_prefixes.extend(standard_dir_prefixes())
    return list(set(dir_prefixes))

def _prepare_primary_names_list(primary_names, use_std_primary_names):
    if primary_names is None:
        primary_names = []
    else:
        primary_names = list(primary_names)
    if use_std_primary_names:
        primary_names.extend(standard_primary_names())
    return list(set(primary_names))

def rsplit_known_suffix(uname, suffixes):
    try:
        prefix, suffix = uname.rsplit('_',1)
    except ValueError:
        if uname in suffixes:
            return None, uname
        else:
            return uname, None
    if suffix in suffixes:
        return prefix, suffix
    else:
        return uname, None

def rsplit_unknown_suffix(uname, suffixes):
    try:
        prefix, suffix = uname.rsplit('_',1)
    except ValueError:
        if uname not in suffixes:
            return None, uname
        else:
            return uname, None
    if suffix not in suffixes:
        return prefix, suffix
    else:
        return uname, None

def rsplit_primary_name(uname, primary_names=None, use_std_primary_names=True):
    pnames = _prepare_primary_names_list(primary_names,use_std_primary_names)
    return rsplit_known_suffix(uname, pnames)

def rsplit_dir_prefix(uname, dir_prefixes=None, use_std_dir_prefixes=True):
    dprefixes = _prepare_dir_prefixes_list(dir_prefixes,use_std_dir_prefixes)
    return rsplit_known_suffix(uname, dprefixes)

def extract_dir_prefix(uname, dir_prefixes=None, use_std_dir_prefixes=True):
    pfx, dirpfx = rsplit_dir_prefix(uname,dir_prefixes,use_std_dir_prefixes)
    return dirpfx
    
def is_user_defined_exec_dir_prefix(prefix, user_prefixes):
    if user_prefixes is None:
        return False
    if prefix not in user_prefixes:
        return False
    return prefix.find('exec') >= 0

def is_exec_dir_prefix(prefix, prefixes=None, use_std_prefixes=True):
    if use_std_prefixes and (prefix in standard_dir_prefixes()):
        return (prefix in _am_install_exec_prefixes)
    else:
        return is_user_defined_exec_dir_prefix(prefix,prefixes)

def is_data_dir_prefix(prefix, prefixes=None, use_std_prefixes=True):
    if use_std_prefixes and (prefix in standard_dir_prefixes()):
        return (prefix in _am_install_data_prefixes)
    else:
        return (not is_user_defined_exec_dir_prefix(prefix,prefixes))

def is_noinst_prefix(prefix):
    if not prefix.endswith('_'):
        prefix = prefix + '_'
    return (prefix.find('noinst_') >=0) or (prefix.find('check_') >= 0)

def StandardPrimaryNames(**kw):
    """Return standard PRIMARY names known from automake"""
    return standard_primary_names()

def StandardDirPrefixes(**kw):
    """Return standard directory prefixes known from automake"""
    return standard_dir_prefixes()

def StandardAdditionalPrefixes(**kw):
    """Return standard additional prefixes known from automake"""
    return standard_additional_prefixes()

def StandardPrimaryDirPrefixes(primary=None,**kw):
    """Return allowed dir prefixes for given PRIMARY name"""
    return standard_primary_dir_prefixes(primary)

def StandardUniformNames(**kw):
    """Return supported install variables (all possible compinations of
    prefixes and PRIMARY names)"""
    return standard_uniform_names()

def RSplitPrimaryName(uname, **kw):
    try:                primary_names = kw['am_primary_names']
    except KeyError:    primary_names = None
    try:                use_std_primary_names = kw['am_std_primary_names']
    except KeyError:    use_std_primary_names = True
    return rsplit_primary_name(uname, primary_names, use_std_primary_names)

def RSplitDirPrefix(uname, **kw):
    try:                dir_prefixes = kw['am_dir_prefixes']
    except KeyError:    dir_prefixes = None
    try:                use_std_dir_prefixes = kw['am_std_dir_prefixes']
    except KeyError:    use_std_dir_prefixes = True
    return rsplit_dir_prefix(uname, dir_prefixes, use_std_dir_prefixes)

def IsUserDefinedExecDirPrefix(prefix, **kw):
    try:                user_prefixes = kw['am_dir_prefixes']
    except KeyError:    user_prefixes = None
    return is_user_defined_exec_dir_prefix(prefix, user_prefixes)

def IsExecDirPrefix(prefix, **kw):
    try:                dir_prefixes = kw['am_dir_prefixes']
    except KeyError:    dir_prefixes = None
    try:                use_std_dir_prefixes = kw['am_std_dir_prefixes']
    except KeyError:    use_std_dir_prefixes = True
    return is_exec_dir_prefix(prefix, dir_prefixes, use_std_dir_prefixes)

def IsDataDirPrefix(prefix, **kw):
    try:                dir_prefixes = kw['am_dir_prefixes']
    except KeyError:    dir_prefixes = None
    try:                use_std_dir_prefixes = kw['am_std_dir_prefixes']
    except KeyError:    use_std_dir_prefixes = True
    return is_data_dir_prefix(prefix, dir_prefixes, use_std_dir_prefixes)

def IsInstallExecName(uname, **kw):
    prefix, primary = RSplitPrimaryName(uname, **kw)
    prefix, dir_prefix = RSplitDirPrefix(prefix, **kw)
    if (prefix is not None) and is_noinst_prefix(prefix):
        return False
    return IsExecDirPrefix(dir_prefix,**kw)

def IsInstallDataName(uname, **kw):
    prefix, primary = RSplitPrimaryName(uname, **kw)
    prefix, dir_prefix = RSplitDirPrefix(prefix, **kw)
    if (prefix is not None) and is_noinst_prefix(prefix):
        return False
    return IsDataDirPrefix(dir_prefix,**kw)

def FilterInstallExecNames(unames,**kw):
    """Filter uniform names and return only these which are to be handled by
    ``install-exec`` target

    :Parameters:
        unames
            uniform variable names,

    :Keywords:
        kw['am_primary_names']
            user-defined primary names (default: None)
        kw['am_std_primary_names'] : boolean
            use standard predefined primary names (default: True)
        kw['am_dir_prefixes']
            user-defined directory prefixes (default: None)
        kw['am_std_dir_prefixes'] : boolean
            use standard predefined directory prefixes (default: True)

    :Return:
        returns list of variable names that should be handled by
        ``install-exec``

    **Example usage:**

    .. python::
        from SConsGnuVariables.AmUniformNames import FilterInstallExecNames
        unames =  ['bin_PROGRAMS', 'lib_LIBRARIES', 'nobase_include_HEADERS',
                   'sysconf_DATA']
        exec_names = FilterInstallExecNames(unames)
        # exec_names is [ 'bin_PROGRAMS', 'lib_LIBRARIES', 'sysconf_DATA' ]
    """
    return [uname for uname in unames if IsInstallExecName(uname,**kw)]
  
def FilterInstallDataNames(unames,**kw):
    """Filter uniform names and return only these which are to be handled by
    ``install-data`` target

    :Parameters:
        unames
            uniform variable names,

    :Keywords:
        kw['am_primary_names']
            user-defined primary names (default: None)
        kw['am_std_primary_names'] : boolean
            use standard predefined primary names (default: True)
        kw['am_dir_prefixes']
            user-defined directory prefixes (default: None)
        kw['am_std_dir_prefixes'] : boolean
            use standard predefined directory prefixes (default: True)
    
    :Return:
        returns list of variable names that should be handled by
        ``install-data``

    **Example usage:**

    .. python::
        from SConsGnuVariables.AmUniformNames import FilterInstallDataNames
        unames =  ['bin_PROGRAMS', 'lib_LIBRARIES', 'nobase_include_HEADERS',
                   'sysconf_DATA']
        data_names = FilterInstallDataNames(unames)
        # data_names is [ 'nobase_include_HEADERS' ]
    """
    return [uname for uname in unames if IsInstallDataName(uname,**kw)]

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
