"""SConsGnuVariables.AmUniformNames

**General Description**

This module provides a kind of 'Automake Uniform Naming', an idea similar to
that known from automake (see automake documentation, `The Uniform Naming
Scheme`_ and `What Gets Installed`_). An example of the 'Automake Uniform
Name' is ``nobase_include_HEADERS`` or ``bin_PROGRAMS``. This module keeps
standard primary names, prefixes, additional prefixes, and combinations of
these. The module also provides functions for filtering collections of uniform
names and extracting the names that should be handled by ``install-exec`` and
``install-data`` targets (see `The Two Parts of Install`_). There are also
several other functions that may be used to manipulate uniform names.

**Terminology**

Let's introduce few terms for clarity:
    
    - full uniform name
        A string in form ``[additional_prefix_]main_prefix_PRIMARY``.
        The ``additional_prefix_`` is optional. Whenever a uniform name
        is decomposed, the additional_prefix, main_prefix, and PRIMARY parts
        are extracted by matching appropriate pieces of uniform name to known
        predefined primary names and prefixes. The uniform name gets decomposed
        from right to left - primary name is extracted first, then the main
        prefix is determined from the remaining part and all that is left is
        treated as additional prefix.
    - uniform name
        A string formatted simillarly to full uniform name. The uniform name
        may be incomplete, i.e. some parts of full uniform name may be already
        stripped-out.
    - primary name
        Last piece of full uniform name.
        
        The list of standard primary names may be retrieved with
        `standard_primary_names()` or `StandardPrimaryNames()`. 
    - main prefix
        A prefix that goes just before primary name in full uniform name,
        it is usually interpreted as directory prefix (e.g. ``bin`` prefix 
        of ``bindir``) but we can find here also non-directory names 
        as ``noinst`` or ``check``.

        The list of standard main prefixes may be retrieved with
        `standard_main_prefixes()` or `StandardMainPrefixes()`.
    - additinal prefix
        The remaining part of full uniform name (after removing primary name
        and main prefix). 

        The list of standard additional prefixes may be retrieved with
        `standard_additional_prefixes()` or `StandardAdditionalPrefixes()`.

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

__am_additional_prefixes = [
    'dist',
    'nodist',
    'nobase',
    'notrans'
]

__am_main_prefixes = [
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
    'pkglibexec',
# not really directory prefixes, but they appear at the place
    'noinst',
    'check'
]

# directory prefixes that prohibit installation
__am_noinst_main_prefixes = [
    'noinst',
    'check'
]

__am_primary_names = [
    'PROGRAMS',
    'LIBRARIES',
    'LTLIBRARIES',
    'LISP',
    'PYTHON',
    'JAVA',
    'SCRIPTS',
    'DATA',
    'HEADERS',
    'MANS',
    'TEXINFOS'
]

__am_primary_main_prefixes = {
    'PROGRAMS'    : ['bin', 'sbin', 'libexec', 'pkglibexec'],
    'LIBRARIES'   : ['lib', 'pkglib'],
    'LTLIBRARIES' : ['lib', 'pkglib'],
    'LISP'        : ['lisp'],
    'PYTHON'      : ['python', 'pkgpython'],
    'JAVA'        : [],
    'SCRIPTS'     : ['bin', 'sbin', 'libexec', 'pkglibexec', 'pkgdata'],
    'DATA'        : ['data', 'sysconf', 'sharedstate', 'localstate', 'pkgdata'],
    'HEADERS'     : ['include', 'oldinclude', 'pkginclude'],
    'MANS'        : ['man'],
    'TEXINFOS'    : ['info']
}

# According to automake's "The Two Parts of Install"
# http://www.gnu.org/software/automake/manual/automake.html#The-Two-Parts-of-Install
__am_install_data_prefixes = [ 
    'data',
    'info',
    'man',
    'include',
    'oldinclude',
    'pkgdata',
    'pkginclude'
]

# According to automake's "The Two Parts of Install"
# http://www.gnu.org/software/automake/manual/automake.html#The-Two-Parts-of-Install
__am_install_exec_prefixes = [
    'bin',
    'sbin',
    'libexec',
    'sysconf',
    'localstate',
    'lib',
    'pkglib'
]

# generate manX directory prefixes
__am_man_sections = map(lambda x : str(x), range(0,10)) + ['n', 'l']
for sec in __am_man_sections:
    __am_primary_main_prefixes['MANS'].append('man%s' % sec)
    __am_main_prefixes.append('man%s' % sec)
    __am_install_data_prefixes.append('man%s' % sec)


# add noinst and check EXTRA prefixes where appropriate
for primary in __am_primary_main_prefixes.keys():
    __am_primary_main_prefixes[primary].append('noinst')
    __am_primary_main_prefixes[primary].append('check')

def standard_primary_names():
    """Return list of standard primary names as defined by GNU build system.

    This function returns the list of primary names defined in the automake
    documentation, see
    http://www.gnu.org/software/automake/manual/html_node/Uniform.html
    """
    return __am_primary_names

def standard_main_prefixes():
    """Return list of standard main prefixes.

    This function returns the list of standard prefixes that may go just before
    PRIMARY names. The list contains directory prefixes based on directory
    variables defined in GNU coding standards (see
    http://www.gnu.org/prep/standards/html_node/Directory-Variables.html#Directory-Variables)
    extended by pkgxxx directory variables defined in
    http://www.gnu.org/software/automake/manual/html_node/Uniform.html and few
    other prefixes.  The returned list also contains special prefixes such as
    ``noinst`` and ``check``.
    """
    return __am_main_prefixes

def standard_additional_prefixes():
    """Return list of standard additional prefixes

    This function returns the list of standard prefixes defined in the
    automake's documentation, i.e. ``nobase``, ``notrans`` and others. See
    http://www.gnu.org/software/automake/manual/html_node/Uniform.html
    for details.
    """
    return __am_additional_prefixes

def standard_primary_main_prefixes(primary = None):
    """Return list of standard prefixes that may go with particular primary
    name.
    
    The function returns, a list of main prefixes that may go together
    with the given ``primary`` name. So, if, for example, the ``primary`` is
    ``"PROGRAMS"``, the supported directory prefixes will be ``["bin", "sbin",
    "libexec", "pkglibexec", "noinst", "check"]``. If the ``primary`` is
    ``None``, then entire dictionary in form::

        { 'PROGRAMS' : ["bin","sbin","libexec","pkglibexec","noinst","check"],
          'LIBRARIES' : ["lib","pkglib","noinst","check"], ... },

    is returned

    The lists were developed according to automake's documentation, especially:

        - ``PROGRAMS`` : http://www.gnu.org/software/automake/manual/automake.html#Program-Sources
        - ``LIBRARIES`` : http://www.gnu.org/software/automake/manual/automake.html#A-Library
        - ``LTLIBRARIES`` : http://www.gnu.org/software/automake/manual/automake.html#Libtool-Libraries
        - ``LISP`` : http://www.gnu.org/software/automake/manual/automake.html#Emacs-Lisp
        - ``PYTHON`` : http://www.gnu.org/software/automake/manual/automake.html#Python
        - ``JAVA`` : http://www.gnu.org/software/automake/manual/automake.html#Java
        - ``SCRIPTS`` : http://www.gnu.org/software/automake/manual/automake.html#Scripts
        - ``DATA`` : http://www.gnu.org/software/automake/manual/automake.html#Data
        - ``HEADERS`` :  http://www.gnu.org/software/automake/manual/automake.html#Headers
        - ``MANS`` : http://www.gnu.org/software/automake/manual/automake.html#Man-Pages
        - ``TEXINFOS`` : http://www.gnu.org/software/automake/manual/automake.html#Texinfo
    """
    if primary is None:
        return __am_primary_main_prefixes
    elif primary in __am_primary_main_prefixes:
        return __am_primary_main_prefixes[primary]  
    else:
        return []

def standard_man_sections():
    """Return list of standard man sections (manpage sections)"""
    return __am_man_sections

def _prepare_main_prefixes_list(main_prefixes, use_std_main_prefixes):
    if main_prefixes is None:
        main_prefixes = []
    else:
        main_prefixes = list(main_prefixes)
    if use_std_main_prefixes:
        main_prefixes.extend(standard_main_prefixes())
    return list(set(main_prefixes))

def _prepare_primary_names_list(primary_names, use_std_primary_names):
    if primary_names is None:
        primary_names = []
    else:
        primary_names = list(primary_names)
    if use_std_primary_names:
        primary_names.extend(standard_primary_names())
    return list(set(primary_names))

# TODO: revise, test
def rsplit_longest_suffix(uname, suffixes):
    """Split-out longest matching suffix from uniform name string. 

    **Usage**::

        prefix, suffix = rsplit_longest_suffix(uname,suffixes)

    **Description**

    The ``uname`` argument is assumed to be a uniform name string (not
    necessary full) in form ``"foo_bar_geez"``. The ``suffixes`` is a list (or
    other sequence) of strings, e.g. ``["hi","geez","o_bar_geez","bar_geez"]``,
    being matched to the tail of ``uname`` string ``"foo_bar_geez"``. The
    longest matching suffix is then split out from the rest of ``uname`` and
    both pieces are returned as tuple. The splitting is allowed only at
    underscore ``"_"`` character, so in above example the ``"bar_geez"`` suffix
    wins and the result is ``("foo", "bar_geez")``.

    **How it works** - by examples (``*`` denotes the selected suffix)::

        uname:         nobase_include
        suffixes:                 foo   
                           se_include
                              include *
        ------------------------------
        result:       (nobase,include)

        uname:                foo_bar
        suffixes:                tuvw
                                  xyz
        -----------------------------
        result:              (foo_bar,None)

        uname:      nodist_my_fooexec
        suffixes:             fooexec
                           my_fooexec *
                        st_my_fooexec
        -----------------------------
        result:    (nodist,my_fooexec)

        uname:                foo_bar
        suffixes:                 bar
                              foo_bar *
        -----------------------------
        result:         (None,foo_bar)

        uname:               _foo_bar
        suffixes:                 bar
                              foo_bar *
        -----------------------------
        result:         (None,foo_bar)


    :Parameters:
        uname
            the uniform name string to be split
        suffixes
            list (or other sequence) of suffixes to be matched to ``uname``
    :Returns:
        returns tuple ``(prefix, suffix)`` where ``suffix`` is the best
        matching suffix and ``prefix`` is the part that remains on the left
        after splitting; if no suffix matches (or the ``uname`` can't be split)
        then the function returns ``(uname, None)``, which means "no suffix
        was split out"; if the longest suffix matches whole ``uname`` then
        returns ``(None, uname)`` what means "no prefix left after splitting";
    """
    minindex = len(uname)
    for suffix in suffixes:
        # FIXME: prevent suffix from starting with '_'?
        index = len(uname) - len(suffix)
        if index == 0 and uname == suffix:
            return None, suffix
        elif index > 0 and index < minindex and uname[index:] == suffix \
             and uname[index-1] == '_':
            minindex = index
    if minindex < len(uname):
        if minindex <= 1:
            return None, uname[minindex:]
        else:
            return uname[:minindex-1], uname[minindex:]
    else:
        return uname, None

def rsplit_primary_name(uname, user_primaries=None, use_std_primary_names=True):
    """Split uniform name into prefix and primary name.

    **Note**
    
    You may rather wish to use `RSplitPrimaryName()`.

    **Description**

    Example standard primaries are ``PROGRAMS`` or ``HEADERS``. If one of such
    (predefined and/or user-defined) words are present at the end of uniform
    name contained in ``uname``, it is going to be split-out from the
    ``uname``. The function works simillary to `rsplit_longest_suffix()`. The
    list of suffixes is taken from `standard_primary_names()` and is optionally
    augmented with user-defined primaries.

    :Parameters:
        uname : str
            the uniform name string to be split
        user_primaries : sequence
            user-defined list (or other sequence) of primary names; if ``None``
            (default) no user-defined primary names are provided
        use_std_primary_names : boolean
            if ``True`` (default), the standard primary names (see
            `standard_primary_names()`) are taken into account additionally to
            user-defined names
    :Returns:
        returns tuple ``(prefix,primary)``; if the ``uname`` doesn't end with
        a known primary name, the function returns ``(uname, None)`` what means
        "can't determine primary name"; if the  ``uname`` has no prefix and
        contains only primary part, the function returns ``(None, uname)``
    """
    names = _prepare_primary_names_list(user_primaries,use_std_primary_names)
    return rsplit_longest_suffix(uname, names)

def rsplit_main_prefix(uname, user_prefixes=None, use_std_main_prefixes=True):
    """Splits-out known main prefix from the end of uniform name.

    **Note**
    
    You may rather wish to use `RSplitMainPrefix()`

    **Description**

    Example main prefixes are ``bin``,  ``include`` or ``noinst``. If one of
    such (predefined or user-defined) strings is present at the end of
    ``uname`` string, it is going to be split-out. The function works simillary
    to `rsplit_longest_suffix()`. The list of suffixes is taken from
    `standard_main_prefixes()` and is optionally augmented with user-defined
    ``user_prefixes``.

    :Parameters:
        uname : str
            the uniform name string to be split
        user_prefixes : sequence
            user-defined list (or other sequence) of directory prefixes; if
            ``None`` (default) no user-defined directory prefixes are provided
        use_std_main_prefixes : boolean
            if ``True`` (default), the standard primary names (see
            `standard_main_prefixes()`) are taken into account additionally to
            user-defined directory prefixes
    :Returns:
        returns tuple (prefix,main_prefix); if the ``uname`` doesn't end with
        known directory prefix, returns (uname, None); if the  ``uname`` has no
        prefix and contains only known directory prefix, the function returns
        (None,uname)
    """
    prefixes = _prepare_main_prefixes_list(user_prefixes,use_std_main_prefixes)
    return rsplit_longest_suffix(uname, prefixes)

def is_noinst_main_prefix(prefix):
    return prefix in __am_noinst_main_prefixes

def is_install_exec_prefix2(prefix,prefixes):
    """Check if ``prefix`` belongs to ``prefixes`` and then if it looks like an
    install-exec directory prefix.
    
    :Parameters:
        prefix : str
            directory prefix to check, e.g. ``bin`` or ``pkglib``
        prefixes : sequence
            predefined (allowed) directory prefixes
    """
    if prefixes is None:         return False
    if prefix not in prefixes:   return False
    if is_noinst_main_prefix(prefix): return False
    return prefix.find('exec') >= 0

def is_install_data_prefix2(prefix,prefixes):
    """Check if ``prefix`` belongs to ``prefixes`` and then if it looks like an
    install-data directory prefix.
    
    :Parameters:
        prefix : str
            directory prefix to check, e.g. ``bin`` or ``pkglib``
        prefixes : sequence
            predefined (allowed) directory prefixes
    """
    if prefixes is None:         return False
    if prefix not in prefixes:   return False
    if is_noinst_main_prefix(prefix): return False
    return prefix.find('exec') < 0

def is_install_exec_prefix(prefix, prefixes=None, use_std_prefixes=True):
    """Check if the ``prefix`` should be clasified as intall-exec directory
    prefix.
    
    :Parameters:
        prefix : str
            directory prefix to check, e.g. ``bin`` or ``pkglib``
        prefixes : sequence
            additional user-defined directory prefixes
        use_std_prefixes : boolean
            if True, then standard directory prefixes are taken into account
    """
    if use_std_prefixes:
        if prefix in __am_install_exec_prefixes: return True
        if is_install_exec_prefix2(prefix,standard_main_prefixes()): return True
    return is_install_exec_prefix2(prefix,prefixes)

def is_install_data_prefix(prefix, prefixes=None, use_std_prefixes=True):
    """Check if the ``prefix`` should be clasified as install-data directory
    prefix
    
    :Parameters:
        prefix : str
            directory prefix to check, e.g. ``bin`` or ``pkglib``
        prefixes : sequence
            additional user-defined directory prefixes
        use_std_prefixes : boolean
            if True, then standard directory prefixes are taken into account
    """
    if use_std_prefixes:
        if prefix in __am_install_data_prefixes: return True
        if is_install_data_prefix2(prefix,standard_main_prefixes()): return True
    return is_install_data_prefix2(prefix,prefixes)


def StandardPrimaryNames(**kw):
    """Return standard PRIMARY names known from automake"""
    return standard_primary_names()

def StandardMainPrefixes(**kw):
    """Return standard directory prefixes known from automake"""
    return standard_main_prefixes()

def StandardAdditionalPrefixes(**kw):
    """Return standard additional prefixes known from automake"""
    return standard_additional_prefixes()

def StandardPrimaryMainPrefixes(primary=None,**kw):
    """Return allowed dir prefixes for given PRIMARY name"""
    return standard_primary_main_prefixes(primary)

def StandardManSections(**kw):
    """Interface to `standard_man_sections()`"""
    return standard_man_sections()

def RSplitPrimaryName(uname, **kw):
    """Interface to `rsplit_primary_name()`."""
    try:                primary_names = kw['am_primary_names']
    except KeyError:    primary_names = None
    try:                use_std_primary_names = kw['am_use_std_primary_names']
    except KeyError:    use_std_primary_names = True
    return rsplit_primary_name(uname, primary_names, use_std_primary_names)

def RSplitMainPrefix(uname, **kw):
    """Interface to `rsplit_main_prefix()`."""
    try:                main_prefixes = kw['am_main_prefixes']
    except KeyError:    main_prefixes = None
    try:                use_std_main_prefixes = kw['am_use_std_main_prefixes']
    except KeyError:    use_std_main_prefixes = True
    return rsplit_main_prefix(uname, main_prefixes, use_std_main_prefixes)

def IsInstallExecPrefix(prefix, **kw):
    """Interface to `is_install_exec_prefix()`."""
    try:                main_prefixes = kw['am_main_prefixes']
    except KeyError:    main_prefixes = None
    try:                use_std_main_prefixes = kw['am_use_std_main_prefixes']
    except KeyError:    use_std_main_prefixes = True
    return is_install_exec_prefix(prefix, main_prefixes, use_std_main_prefixes)

def IsInstallDataPrefix(prefix, **kw):
    """Interface to `is_install_data_prefix()`."""
    try:                main_prefixes = kw['am_main_prefixes']
    except KeyError:    main_prefixes = None
    try:                use_std_main_prefixes = kw['am_use_std_main_prefixes']
    except KeyError:    use_std_main_prefixes = True
    return is_install_data_prefix(prefix, main_prefixes, use_std_main_prefixes)

def IsInstallExecName(uname, **kw):
    """Check if the uniform name should be handled by ``install-exec``."""
    prefix, primary = RSplitPrimaryName(uname, **kw)
    prefix, main_prefix = RSplitMainPrefix(prefix, **kw)
    return IsInstallExecPrefix(main_prefix,**kw)

def IsInstallDataName(uname, **kw):
    """Check if the uniform name should be handled by ``install-data``."""
    prefix, primary = RSplitPrimaryName(uname, **kw)
    prefix, main_prefix = RSplitMainPrefix(prefix, **kw)
    return IsInstallDataPrefix(main_prefix,**kw)

def FilterInstallExecNames(unames,**kw):
    """Filter uniform names and return only these which are to be handled by
    ``install-exec`` target

    :Parameters:
        unames
            uniform variable names,

    :Keywords:
        kw['am_primary_names']
            user-defined primary names (default: None)
        kw['am_use_std_primary_names'] : boolean
            use standard predefined primary names (default: True)
        kw['am_main_prefixes']
            user-defined directory prefixes (default: None)
        kw['am_use_std_main_prefixes'] : boolean
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
        kw['am_use_std_primary_names'] : boolean
            use standard predefined primary names (default: True)
        kw['am_main_prefixes']
            user-defined directory prefixes (default: None)
        kw['am_use_std_main_prefixes'] : boolean
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
