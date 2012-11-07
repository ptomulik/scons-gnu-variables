"""SConsGnuVariables.AmUniformNames

**General Description**

This module provides a kind of 'Automake Uniform Naming', an idea similar to
that known from automake (see automake's `The Uniform Naming Scheme`_ section).
An example of the 'Automake Uniform Name' is ``nobase_include_HEADERS`` or
``bin_PROGRAMS``. This module keeps standard primary names, prefixes,
additional prefixes, and combinations of these. The module also provides
functions for filtering collections of uniform names and extracting the names
that should be handled by certain Makefile's targets (e.g. ``install-exec`` or
``install-data`` defined in `The Two Parts of Install`_). There are also
several other functions that may be used to manipulate uniform names and check
their sanity.

**Terminology**

Let's introduce few terms for clarity:
    
    - full uniform name
        A string in form ``[add_prefix_]main_prefix_PRIMARY``.
        The ``add_prefix_`` is optional. Whenever a uniform name
        is decomposed, the add_prefix, main_prefix, and PRIMARY parts
        are extracted by matching appropriate pieces of uniform name to known
        predefined primary names and prefixes. The uniform name gets
        decomposed from right to left - primary name is extracted first, then
        the main prefix is determined from the remaining part and all that is
        left is treated as additional prefix.
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
    - additional prefix
        The remaining part of full uniform name (after removing primary name
        and main prefix). 

        The list of standard additional prefixes may be retrieved with
        `standard_add_prefixes()` or `StandardAddPrefixes()`.

For related automake information see
<http://www.gnu.org/software/automake/manual/html_node/Uniform.html>

.. _The Uniform Naming Scheme: http://www.gnu.org/software/automake/manual/automake.html#Uniform
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

#############################################################################
__std_add_prefixes = [
    'dist',
    'nodist',
    'nobase',
    'notrans'
]

#############################################################################
__std_main_prefixes = [
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
# not directory prefixes,
    'noinst',
    'check'
]

# main prefixes that prohibit installation
#############################################################################
__std_noinst_main_prefixes = [
    'noinst',
    'check'
]

#############################################################################
__std_primary_names = [
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

#############################################################################
__std_primary_main_prefixes = {
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

# certain forbidden combinations
#############################################################################
__std_forbid_primary_main_prefixes = {
    'PROGRAMS'      : [],
    'LIBRARIES'     : [],
    'LTLIBRARIES'   : [],
    'LISP'          : [],
    'PYTHON'        : [],
    'JAVA'          : [],
    'SCRIPTS'       : [],
    'DATA'          : [],
    'HEADERS'       : [],
    'MANS'          : [],
    'TEXINFOS'      : [],
}

#############################################################################
__std_forbid_primary_add_prefixes = {
    'PROGRAMS'      : [],
    'LIBRARIES'     : [],
    'LTLIBRARIES'   : [],
    'LISP'          : [],
    'PYTHON'        : [],
    'JAVA'          : [],
    'SCRIPTS'       : [],
    'DATA'          : [],
    'HEADERS'       : [],
    'MANS'          : [],
    'TEXINFOS'      : [],
}

#############################################################################
__std_forbid_main_add_prefixes = {
    'bin'           : [],
    'sbin'          : [],
    'libexec'       : [],
    'dataroot'      : [],
    'data'          : [],
    'sysconf'       : [],
    'sharedstate'   : [],
    'localstate'    : [],
    'include'       : [],
    'oldinclude'    : [],
    'doc'           : [],
    'info'          : [],
    'html'          : [],
    'dvi'           : [],
    'pdf'           : [],
    'ps'            : [],
    'lib'           : [],
    'lisp'          : [],
    'locale'        : [],
    'man'           : ['nobase'],
    'pkgdata'       : [],
    'pkginclude'    : [],
    'pkglib'        : [],
    'pkglibexec'    : [],
#
    'noinst'        : ['nobase'],
    'check'         : []
}

# According to automake's "The Two Parts of Install"
# http://www.gnu.org/software/automake/manual/automake.html#The-Two-Parts-of-Install
#############################################################################
__std_install_data_prefixes = [ 
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
#############################################################################
__std_install_exec_prefixes = [
    'bin',
    'sbin',
    'libexec',
    'sysconf',
    'localstate',
    'lib',
    'pkglib'
]

__std_man_sections = map(lambda x : str(x), range(0,10)) + ['n', 'l']

#############################################################################
def __init_module_vars():
    # generate manX directory prefixes
    for sec in __std_man_sections:
        __std_primary_main_prefixes['MANS'].append('man%s' % sec)
        __std_main_prefixes.append('man%s' % sec)
        __std_install_data_prefixes.append('man%s' % sec)
        __std_forbid_main_add_prefixes['man%s' % sec] = \
            __std_forbid_main_add_prefixes['man']
    # add 'noinst' and 'check' prefixes where appropriate
    for primary in __std_primary_main_prefixes.keys():
        __std_primary_main_prefixes[primary].append('noinst')
        __std_primary_main_prefixes[primary].append('check')

__init_module_vars()


#############################################################################
def standard_primary_names():
    """Return list of standard primary names as defined by GNU build system.

    **Note**
    
    You may wish to use `StandardPrimaryNames()` instead.
    
    **Description**

    This function returns the list of primary names defined in the automake
    documentation, see `The Uniform Naming Scheme`_ section of automake
    documentation.

    .. _The Uniform Naming Scheme: http://www.gnu.org/software/automake/manual/html_node/Uniform.html
    """
    return __std_primary_names

#############################################################################
def standard_main_prefixes():
    """Return list of standard main prefixes.

    **Note**
    
    You may wish to use `StandardMainPrefixes()` instead.
    
    **Description**

    This function returns the list of standard prefixes that may go just before
    PRIMARY names. The list contains directory prefixes based on directory
    variables defined in GNU coding standards (see `Variables for Installation
    Directories`_) extended by pkgxxx directory variables defined by `The
    Uniform Naming Scheme`_  (automake) and few other prefixes.  The returned
    list also contains special prefixes such as ``noinst`` and ``check``.

    .. _The Uniform Naming Scheme: http://www.gnu.org/software/automake/manual/html_node/Uniform.html
    .. _Variables for Installation Directories: http://www.gnu.org/prep/standards/html_node/Directory-Variables.html#Directory-Variables
    """
    return __std_main_prefixes

#############################################################################
def standard_add_prefixes():
    """Return list of standard additional prefixes

    **Note**
    
    You may wish to use `StandardAddPrefixes()` instead.
    
    **Description**

    This function returns the list of standard prefixes defined in the
    automake's documentation, i.e. ``nobase``, ``notrans`` and others. See
    `The Uniform Naming Scheme`_ (automake) for details.

    .. _The Uniform Naming Scheme: http://www.gnu.org/software/automake/manual/html_node/Uniform.html
    """
    return __std_add_prefixes

#############################################################################
def standard_primary_main_prefixes(primary = None):
    """Return list of standard prefixes that may go with particular primary
    name.

    **Note**
    
    You may wish to use `StandardPrimaryMainPrefixes()` instead.
    
    **Description**

    The function returns, a list of main prefixes that may go together
    with the given ``primary`` name. So, if, for example, the ``primary`` is
    ``"PROGRAMS"``, the supported main prefixes will be ``["bin", "sbin",
    "libexec", "pkglibexec", "noinst", "check"]``. If the ``primary`` is
    ``None``, then entire dictionary describing allowed combinations is
    returned. The dictionary has form::

        { 'PROGRAMS' : ["bin","sbin","libexec","pkglibexec","noinst","check"],
          'LIBRARIES' : ["lib","pkglib","noinst","check"], ... },

    is returned.

    The lists were developed according to automake's documentation, especially:

        - ``PROGRAMS`` : `Defining program sources`_ section,
        - ``LIBRARIES`` : `Building a library`_ section,
        - ``LTLIBRARIES`` : `Building Libtool Libraries`_ section,
        - ``LISP`` : `Emacs Lisp`_ section,
        - ``PYTHON`` : `Python`_ section,
        - ``JAVA`` :  `Java bytecode compilation`_ section,
        - ``SCRIPTS`` : `Executable scripts`_ section,
        - ``DATA`` : `Architecture-independent data files`_ section,
        - ``HEADERS`` : `Header files`_ secition,
        - ``MANS`` : `Man pages`_ section,
        - ``TEXINFOS`` : `Texinfo`_ section

    .. _Defining program sources: http://www.gnu.org/software/automake/manual/automake.html#Program-Sources
    .. _Building a library: http://www.gnu.org/software/automake/manual/automake.html#A-Library
    .. _Building Libtool Libraries: http://www.gnu.org/software/automake/manual/automake.html#Libtool-Libraries
    .. _Emacs Lisp: http://www.gnu.org/software/automake/manual/automake.html#Emacs-Lisp
    .. _Python: http://www.gnu.org/software/automake/manual/automake.html#Python
    .. _Java bytecode compilation: http://www.gnu.org/software/automake/manual/automake.html#Java
    .. _Executable scripts: http://www.gnu.org/software/automake/manual/automake.html#Scripts
    .. _Architecture-independent data files: http://www.gnu.org/software/automake/manual/automake.html#Data
    .. _Header files:  http://www.gnu.org/software/automake/manual/automake.html#Headers
    .. _Man pages: http://www.gnu.org/software/automake/manual/automake.html#Man-Pages
    .. _Texinfo: http://www.gnu.org/software/automake/manual/automake.html#Texinfo
    """
    if primary is None:
        return __std_primary_main_prefixes
    elif primary in __std_primary_main_prefixes:
        return __std_primary_main_prefixes[primary]  
    else:
        return []

#############################################################################
def standard_man_sections():
    """Return list of standard man sections (manpage sections)

    **Note**
    
    You may wish to use `StandardManSections()` instead.
    
    **Description**

    The function returns a list of man page sections as defined in the section
    `Man pages`_ of automake documentation.

    .. _Man pages: http://www.gnu.org/software/automake/manual/automake.html#Man-Pages
    """
    return __std_man_sections

#############################################################################
def _prepare_primary_names_list(primary_names, use_std_primary_names):
    if primary_names is None:
        primary_names = []
    else:
        primary_names = list(primary_names)
    if use_std_primary_names:
        primary_names.extend(standard_primary_names())
    return list(set(primary_names))

#############################################################################
def _prepare_main_prefixes_list(main_prefixes, use_std_main_prefixes):
    if main_prefixes is None:
        main_prefixes = []
    else:
        main_prefixes = list(main_prefixes)
    if use_std_main_prefixes:
        main_prefixes.extend(standard_main_prefixes())
    return list(set(main_prefixes))

#############################################################################
def _prepare_add_prefixes_list(add_prefixes, use_std_add_prefixes):
    if add_prefixes is None:
        add_prefixes = []
    else:
        add_prefixes = list(add_prefixes)
    if use_std_add_prefixes:
        add_prefixes.extend(standard_add_prefixes())
    return list(set(add_prefixes))


#############################################################################
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

#############################################################################
def rsplit_primary_name(uname, primary_names=None, use_std_primary_names=True):
    """Split uniform name into prefix and primary name.

    **Note**
    
    You may wish to use `RSplitPrimaryName()` instead.

    **Description**

    Example standard primaries are ``PROGRAMS`` or ``HEADERS``. If one of such
    (predefined and/or user-defined) words are present at the end of uniform
    name contained in ``uname``, it is going to be split-out from the
    ``uname``. The function works simillary to `rsplit_longest_suffix()`. The
    list of suffixes is taken from `standard_primary_names()` and is
    optionally augmented with user-defined primaries.

    :Parameters:
        uname : str
            the uniform name string to be split
        primary_names : sequence
            user-defined list (or other sequence) of primary names; if ``None``
            (default) no user-defined primary names are provided
        use_std_primary_names : boolean
            if ``True`` (default), the standard primary names (see
            `standard_primary_names()`) are (also) taken into account
    :Returns:
        returns tuple ``(prefix,primary)``; if the ``uname`` doesn't end with
        a known primary name, the function returns ``(uname, None)`` what means
        "can't determine primary name"; if the ``uname`` has no prefix and
        contains only primary part, the function returns ``(None, uname)``
    """
    names = _prepare_primary_names_list(primary_names,use_std_primary_names)
    return rsplit_longest_suffix(uname, names)

#############################################################################
def rsplit_main_prefix(uname, main_prefixes=None, use_std_main_prefixes=True):
    """Splits-out known main prefix from the end of uniform name.

    **Note**
    
    You may wish to use `RSplitMainPrefix()` instead.

    **Description**

    Example main prefixes are ``bin``,  ``include`` or ``noinst``. If one of
    such (predefined or user-defined) strings is present at the end of
    ``uname`` string, it is going to be split-out. The function works simillary
    to `rsplit_longest_suffix()`. The list of suffixes is taken from
    `standard_main_prefixes()` and is optionally augmented with user-defined
    ``main_prefixes``.

    :Parameters:
        uname : str
            the uniform name string to be split
        main_prefixes : sequence
            user-defined list (or other sequence) of main prefixes; if
            ``None`` (default) no user-defined main prefixes are provided
        use_std_main_prefixes : boolean
            if ``True`` (default), the standard main prefixes (see
            `standard_main_prefixes()`) are (also) taken into account
    :Returns:
        returns tuple (prefix,main_prefix); if the ``uname`` doesn't end with
        known directory prefix, returns (uname, None); if the ``uname``
        contains no additional prefix, the function returns (None,uname)
    """
    prefixes = _prepare_main_prefixes_list(main_prefixes,use_std_main_prefixes)
    return rsplit_longest_suffix(uname, prefixes)

#############################################################################
def rsplit_add_prefix(uname, add_prefixes=None, use_std_add_prefixes=True):
    """Splits-out known additional prefix from the end of uniform name.

    **Note**
    
    You may wish to use `RSplitAddPrefix()` instead.

    **Description**

    Example additional prefixes are ``nobase`` or ``nodist``. If one of
    such (predefined or user-defined) strings is present at the end of
    ``uname`` string, it is going to be split-out. The function works simillary
    to `rsplit_longest_suffix()`. The list of suffixes is taken from
    `standard_add_prefixes()` and is optionally augmented with
    user-defined ``add_prefixes``.

    :Parameters:
        uname : str
            the uniform name string to be split
        add_prefixes : sequence
            user-defined list (or other sequence) of additional prefixes; if
            ``None`` (default) no user-defined additional prefixes are provided
        use_std_add_prefixes : boolean
            if ``True`` (default), the standard additional prefixes (see
            `standard_add_prefixes()`) are (also) taken into account
    :Returns:
        returns tuple (prefix,add_prefix); if the ``uname`` doesn't end
        with known additional prefix, returns (uname, None); if the  ``uname``
        is composed solely of single additional prefix, the function returns
        (None,uname)
    """
    prefixes = _prepare_add_prefixes_list(add_prefixes,
                                                 use_std_add_prefixes)
    return rsplit_longest_suffix(uname, prefixes)

#############################################################################
def decompose_name(funame, primary_names=None, main_prefixes=None,
                           add_prefixes=None,
                           use_std_primary_names=True,
                           use_std_main_prefixes=True,
                           use_std_add_prefixes=True):
    """Decomposes full uniform name into three parts.

    **Note**

    You may wish to use `DecomposeName()` instead.

    **Description**

    The function decomposes full uniform name into three parts:

        - (possibly empty) list of additional prefixes,
        - main prefix,
        - primary name.

    The function returns a tuple ``(prefix_list, main_prefix, primary)``, where
    ``prefix_list`` is a list, ``main_prefix`` is a string and ``primary`` is
    also string.

    If the function is unable to decompose ``funame`` (e.g. ``funame``
    contains malformed name), a ``ValueError`` exception is raised.

    **Few examples**:

        >>> def dun(*args):
        ...     from SConsGnuVariables.AmUniformNames import decompose_name
        ...     try: return decompose_name(*args)
        ...     except ValueError, e:
        ...         print 'ValueError:', e
        ...         return None
        ... 
        >>> dun('PROGRAMS')
        ValueError: malformed uniform name 'PROGRAMS'
        >>> dun('bin_PROGRAMS')
        ([], 'bin', 'PROGRAMS')
        >>> dun('nodist_bin_PROGRAMS')
        (['nodist'], 'bin', 'PROGRAMS')
        >>> dun('notrans_nodist_bin_PROGRAMS')
        (['notrans','nodist'], 'bin', 'PROGRAMS')
        >>> dun('bin_FOO')
        ValueError: can't recognize primary name in 'bin_FOO'
        >>> dun('bin_FOO', ['FOO','FOO1'])
        ([], 'bin', 'FOO')
        >>> dun('bar_FOO', ['FOO','FOO1'])
        ValueError: can't recognize main prefix in 'bar_FOO'
        >>> dun('bar_FOO', ['FOO','FOO1'], ['bar','bar1'])
        ([], 'bar', 'FOO')
        >>> dun('geez_bar_FOO', ['FOO','FOO1'], ['bar','bar1'])
        ValueError: unknown prefix 'geez' in uniform name 'geez_bar_FOO'
        >>> dun('geez_bar_FOO', ['FOO','FOO1'], ['bar','bar1'], ['geez', 'geez1'])
        (['geez'], 'bar', 'FOO')

    :Parameters:
        funame : str
            full uniform name to be decomposed
        primary_names : sequence | None
            used-defined primary names (default: None)
        main_prefixes : sequence | None
            used-defined main prefixes (default: None)
        add_prefixes : sequence | None
            used-defined additional prefixes (default: None)
        use_std_primary_names : boolean
            if ``True`` (default), standard primary names are taken into
            account when recognizing primary part of uniform name ``funame``
        use_std_main_prefixes : boolean
            if ``True`` (default), standard main prefixes are taken into
            account when recognizing main_prefix part of uniform name
            ``funame``
        use_std_add_prefixes : boolean
            if ``True`` (default), standard additional prefixes are taken into
            account when recognizing additional prefixes in uniform name
            ``funame``

    :Returns:
        returns tuple ``(prefix_list, main_prefix, primary)``, where
        ``prefix_list`` is possibly empty list of additional prefixes
        recognized in ``funame``, the ``main_prefix`` is a string containing
        main prefix recognized in ``funame`` and ``primary`` is a string
        containing the primary name recognized in ``funame``.
    """
    prefix, primary = rsplit_primary_name(funame, primary_names,
                                          use_std_primary_names)
    if primary is None:
        raise ValueError("can't recognize primary name in %r" % funame)
    if prefix is None:
        raise ValueError("malformed uniform name %r" % funame)
    prefix, main_prefix = rsplit_main_prefix(prefix, main_prefixes,
                                             use_std_main_prefixes)
    if main_prefix is None:
        raise ValueError("can't recognize main prefix in %r" % funame)
    prefix_list = []
    while prefix is not None:
        prefix, add_prefix = rsplit_add_prefix(prefix, add_prefixes,
                                               use_std_add_prefixes)
        if add_prefix is None:
            raise ValueError("unknown prefix %r in uniform name %r" \
                             % (prefix, funame))
        prefix_list.insert(0,add_prefix)
    return prefix_list, main_prefix, primary

#############################################################################
def _ensure_not_forbidden(prefixes, main_prefix, primary,
                          forbid_primary_main_prefixes=None,
                          forbid_primary_add_prefixes=None,
                          forbid_main_add_prefixes=None,
                          use_std_forbid_primary_main_prefixes=True,
                          use_std_forbid_primary_add_prefixes=True,
                          use_std_forbid_main_add_prefixes=True):
    """Ensure that given combination of additional prefixes, main prefix and
    primary name is not forbidden

    If the combination of ``prefixes``, ``main_prefix`` and
    ``primary`` is disallowed in uniform name, the function throws
    ``ValueError`` with explanation.

    **Examples**

        >>> def enf(*args):
        ...     from SConsGnuVariables.AmUniformNames import _ensure_not_forbidden
        ...     try: return _ensure_not_forbidden(*args)
        ...     except ValueError, e:
        ...         print 'ValueError:', e
        ...         return None
        ...
        >>> enf([],'bin','PROGRAMS')
        True
        >>> enf(['nobase'], 'man1', 'MANS')
        ValueError: fobidden combination of additional prefix 'nobase' and main prefix 'man1' in uniform name 'nobase_man1_MANS'

    :Parameters:
        prefixes : sequence
            sequence of additional prefixes extracted from uniform name
        main_prefix : str
            main prefix extracted from uniform name
        primary : str
            primary name extracted from uniform name
        forbid_primary_main_prefixes : dict | None
            user-defined dictionary of disallowed combinations of primary
            names and main prefixes. The dictionary has form::

                {'PRIM1' : [ 'main1', 'main2', ... ],
                 'PRIM2' : [ 'main3', 'main3', ... ], ... }

            where ``PRIM1``, ``PRIM2``, ... (keys) are primary names, and
            for each primary name there is a list of disallowed main prefixes
        forbid_primary_add_prefixes : dict | None
            user-defined dictionary of disallowed combinations of primary
            names and additional prefixes. The dictionary has form::

                {'PRIM1' : [ 'prefix1', 'prefix2', ... ],
                 'PRIM2' : [ 'prefix3', 'prefix3', ... ], ... }

            where ``PRIM1``, ``PRIM2``, ... (keys) are primary names, and
            for each primary name there is a list of disallowed additional
            prefixes
        forbid_main_add_prefixes : dict | None
            user-defined dictionary of disallowed combinations of main prefix
            and additional prefixes. The dictionary has form::

                {'main1' : [ 'prefix1', 'prefix2', ... ],
                 'main2' : [ 'prefix3', 'prefix3', ... ], ... }

            where ``main1``, ``main2``, ... (keys) are main prefixes, and
            for each such prefix there is a list of disallowed additional
            prefixes
        use_std_forbid_primary_main_prefixes : boolean
            if ``True`` (default), take into account also standard forbid
            definitions for primary name + main prefix combinations
        use_std_forbid_primary_add_prefixes : boolean
            if ``True`` (default), take into account also standard forbid
            definitions for primary name + additional prefix combinations
        use_std_forbid_main_add_prefixes : boolean
            if ``True`` (default), take into account also standard forbid
            definitions for main prefix + additional prefix combinations
    """
    funame = '_'.join(list(prefixes) + [main_prefix, primary])
    # Assert main_prefix + primary is not forbidden
    if forbid_primary_main_prefixes is not None:
        try:
            if main_prefix in forbid_primary_main_prefixes[primary]:
                raise ValueError("fobidden combination of prefix %r " \
                    "and primary name %r in uniform name %r" 
                    % (main_prefix, primary, funame) )
        except KeyError:
            pass
    if use_std_forbid_primary_main_prefixes:
        try:
            if main_prefix in __std_forbid_primary_main_prefixes[primary]:
                raise ValueError("fobidden combination of prefix %r " \
                    "and primary name %r in uniform name %r" 
                    % (main_prefix, primary, funame) )
        except KeyError:
            pass
    # Assert add_prefix + primary is not forbidden
    if forbid_primary_add_prefixes is not None:
        for prefix in prefixes:
            try:
                if prefix in forbid_primary_add_prefixes[primary]:
                    raise ValueError("fobidden combination of additional " \
                        "prefix %r and primary name %r in uniform name %r" 
                        % (prefix, primary, funame) )
            except KeyError:
                pass
    if use_std_forbid_primary_add_prefixes:
        for prefix in prefixes:
            try:
                if prefix in __std_forbid_primary_add_prefixes[primary]:
                    raise ValueError("fobidden combination of additional " \
                        "prefix %r and primary name %r in uniform name %r" 
                        % (prefix, primary, funame) )
            except KeyError:
                pass
    # Assert add_prefix + main prefix is not forbidden
    if forbid_main_add_prefixes is not None:
        for prefix in prefixes:
            try:
                if prefix in forbid_main_add_prefixes[main_prefix]:
                    raise ValueError("fobidden combination of additional " \
                        "prefix %r and main prefix %r in uniform name %r" 
                        % (prefix, main_prefix, funame) )
            except KeyError:
                pass
    if use_std_forbid_main_add_prefixes:
        for prefix in prefixes:
            try:
                if prefix in __std_forbid_main_add_prefixes[main_prefix]:
                    raise ValueError("fobidden combination of additional " \
                        "prefix %r and main prefix %r in uniform name %r" 
                        % (prefix, main_prefix, funame) )
            except KeyError:
                pass
    return True

#############################################################################
def _ensure_predefined(prefixes, main_prefix, primary,
                       primary_main_prefixes=None,
                       use_std_primary_main_prefixes=True):
    """Ensure that given combination of main prefix and primary name is
    predefined.
    """
    funame = '_'.join(list(prefixes) + [main_prefix, primary])
    if use_std_primary_main_prefixes:
        try:
            if main_prefix in __std_primary_main_prefixes[primary]:
                return True
        except KeyError:
            pass
    if primary_main_prefixes is not None:
        try:
            if main_prefix in primary_main_prefixes[primary]:
                return True
        except KeyError:
            pass
    raise ValueError("unsupported combination of main prefix %r and " \
                     "primary name %r in uniform name %r" \
                     % (main_prefix, primary, funame))

#############################################################################
def ensure_name_sanity(funame, primary_names=None, 
                      main_prefixes=None,
                      add_prefixes=None, 
                      primary_main_prefixes=None,
                      forbid_primary_main_prefixes=None,
                      forbid_primary_add_prefixes=None,
                      forbid_main_add_prefixes=None,
                      use_std_primary_names=True,
                      use_std_main_prefixes=True,
                      use_std_add_prefixes=True,
                      use_std_primary_main_prefixes=True,
                      use_std_forbid_primary_main_prefixes=True,
                      use_std_forbid_primary_add_prefixes=True,
                      use_std_forbid_main_add_prefixes=True):
    """Perform sanity checks on the full uniform name ``funame``.

    **Note**

    You may wish to use `EnsureNameSanity()` instead.

    **Description**

    This function performs sanity checks on full uniform name contained in 
    ``funame`` and throws ``ValueError`` if the sanity check fails. The
    sanity check fails if the combination of additional prefixes, main prefix
    and primary name contained in the full uniform name is known to be
    forbidden or is not predefined by standard (and user).

    The sanity checks include:

        - checks performed by `decompose_name()` function,
        - checks performed by `_ensure_not_forbidden()` function,
        - checks performed by `_ensure_predefined()` function.

    The arguments are passed to each of the above functions without
    modification.
    """
    prefixes, main_prefix, primary = decompose_name(funame,
        primary_names, main_prefixes, add_prefixes,
        use_std_primary_names, use_std_main_prefixes,
        use_std_add_prefixes)
    _ensure_not_forbidden(prefixes, main_prefix, primary,
        forbid_primary_main_prefixes, forbid_primary_add_prefixes,
        forbid_main_add_prefixes,
        use_std_forbid_primary_main_prefixes,
        use_std_forbid_primary_add_prefixes,
        use_std_forbid_main_add_prefixes)
    _ensure_predefined(prefixes, main_prefix, primary, primary_main_prefixes,
        use_std_primary_main_prefixes)
    return True

#############################################################################
def is_noinst_main_prefix(prefix):
    return prefix in __std_noinst_main_prefixes

#############################################################################
def is_install_exec_prefix2(prefix, main_prefixes):
    """Check if ``prefix`` belongs to ``main_prefixes`` and then if it
    looks like an install-exec directory prefix.
    
    :Parameters:
        prefix : str
            main prefix to check, e.g. ``bin`` or ``pkglib``
        main_prefixes : sequence
            predefined (allowed) directory main prefixes
    """
    if main_prefixes is None:               return False
    if prefix not in main_prefixes:    return False
    if is_noinst_main_prefix(prefix):  return False
    return prefix.find('exec') >= 0

#############################################################################
def is_install_data_prefix2(prefix, main_prefixes):
    """Check if ``prefix`` belongs to ``main_prefixes`` and then if it
    looks like an install-data directory prefix.
    
    :Parameters:
        prefix : str
            main prefix to check, e.g. ``bin`` or ``pkglib``
        main_prefixes : sequence
            predefined (allowed) main prefixes
    """
    if main_prefixes is None:               return False
    if prefix not in main_prefixes:    return False
    if is_noinst_main_prefix(prefix):  return False
    return prefix.find('exec') < 0

#############################################################################
def is_install_exec_prefix(prefix, main_prefixes=None,
                           use_std_main_prefixes=True):
    """Check if the ``prefix`` should be clasified as intall-exec
    directory prefix.

    **Note**

    You may wish to use `IsInstallExecPrefix()` instead.

    :Parameters:
        prefix : str
            directory prefix to check, e.g. ``bin`` or ``pkglib``
        main_prefixes : sequence
            additional user-defined main prefixes
        use_std_main_prefixes : boolean
            if True, then standard main prefixes are taken into account
    """
    if use_std_main_prefixes:
        if prefix in __std_install_exec_prefixes: return True
        if prefix in __std_install_data_prefixes: return False
        if is_install_exec_prefix2(prefix,standard_main_prefixes()):
            return True
    return is_install_exec_prefix2(prefix,main_prefixes)

#############################################################################
def is_install_data_prefix(prefix, main_prefixes=None,
                           use_std_main_prefixes=True):
    """Check if the ``prefix`` should be clasified as install-data directory
    prefix

    **Note**

    You may wish to use `IsInstallDataPrefix()` instead.
    
    :Parameters:
        prefix : str
            directory prefix to check, e.g. ``bin`` or ``pkglib``
        main_prefixes : sequence
            additional user-defined directory prefixes
        use_std_main_prefixes : boolean
            if True, then standard directory prefixes are taken into account
    """
    if use_std_main_prefixes:
        if prefix in __std_install_data_prefixes: return True
        if prefix in __std_install_exec_prefixes: return False
        if is_install_data_prefix2(prefix,standard_main_prefixes()): 
            return True
    return is_install_data_prefix2(prefix,main_prefixes)

#############################################################################
def is_install_exec_name(funame, primary_names=None, main_prefixes=None,
                         use_std_primary_names=True,
                         use_std_main_prefixes=True):
    """Check if the ``funame`` should be handled by ``install-exec`` target

    **Note**

    You may wish to use `IsInstallExecName()` instead.

    **Examples**:

        >>> from SConsGnuVariables.AmUniformNames import is_install_exec_name
        >>> is_install_exec_name('bin_PROGRAMS')
        True
        >>> is_install_exec_name('data_DATA')
        False
        >>> is_install_exec_name('noinst_PROGRAMS')
        False
        >>> is_install_exec_name('foo_PROGRAMS', None, ['foo','fooexecbar'])
        False
        >>> is_install_exec_name('fooexecbar_PROGRAMS', None, ['foo','fooexecbar'])
        True

    :Parameters:
        funame : str
            full uniform name to be checked
        primary_names : sequence | None
            used-defined primary names (default: None)
        main_prefixes : sequence | None
            used-defined main prefixes (default: None)
        use_std_primary_names : boolean
            if ``True`` (default), standard primary names are taken into
            account when recognizing primary part of uniform name ``funame``
        use_std_main_prefixes : boolean
            if ``True`` (default), standard main prefixes are taken into
            account when recognizing main_prefix part of uniform name
            ``funame``
    """
    prefix, primary = rsplit_primary_name(funame, primary_names,
                                          use_std_primary_names)
    if primary is None:
        raise ValueError("can't recognize primary name in %r" % funame)
    if prefix is None:
        raise ValueError("malformed uniform name %r" % funame)
    prefix, main_prefix = rsplit_main_prefix(prefix, main_prefixes,
                                             use_std_main_prefixes)
    if main_prefix is None:
        raise ValueError("can't recognize main prefix in %r" % funame)
    return is_install_exec_prefix(main_prefix, main_prefixes,
                                  use_std_main_prefixes)

#############################################################################
def is_install_data_name(funame, primary_names=None, main_prefixes=None,
                         use_std_primary_names=True,
                         use_std_main_prefixes=True):
    """Check if the ``funame`` should be handled by ``install-data`` target

    **Note**

    You may wish to use `IsInstallDataName()` instead.

    **Examples**:

        >>> from SConsGnuVariables.AmUniformNames import is_install_data_name
        >>> is_install_data_name('bin_PROGRAMS')
        False
        >>> is_install_data_name('data_DATA')
        True
        >>> is_install_data_name('noinst_TEXINFOS')
        False
        >>> is_install_data_name('foo_PROGRAMS', None, ['foo','fooexecbar'])
        True
        >>> is_install_data_name('fooexecbar_PROGRAMS', None, ['foo','fooexecbar'])
        False

    :Parameters:
        funame : str
            full uniform name to be checked
        primary_names : sequence | None
            used-defined primary names (default: None)
        main_prefixes : sequence | None
            used-defined main prefixes (default: None)
        use_std_primary_names : boolean
            if ``True`` (default), standard primary names are taken into
            account when recognizing primary part of uniform name ``funame``
        use_std_main_prefixes : boolean
            if ``True`` (default), standard main prefixes are taken into
            account when recognizing main_prefix part of uniform name
            ``funame``
    """
    prefix, primary = rsplit_primary_name(funame, primary_names,
                                          use_std_primary_names)
    if primary is None:
        raise ValueError("can't recognize primary name in %r" % funame)
    if prefix is None:
        raise ValueError("malformed uniform name %r" % funame)
    prefix, main_prefix = rsplit_main_prefix(prefix, main_prefixes,
                                             use_std_main_prefixes)
    if main_prefix is None:
        raise ValueError("can't recognize main prefix in %r" % funame)
    return is_install_data_prefix(main_prefix, main_prefixes,
                                  use_std_main_prefixes)

#############################################################################
def StandardPrimaryNames(**kw):
    """Return standard PRIMARY names known from automake"""
    return standard_primary_names()

#############################################################################
def StandardMainPrefixes(**kw):
    """Return standard directory prefixes known from automake"""
    return standard_main_prefixes()

#############################################################################
def StandardAddPrefixes(**kw):
    """Return standard additional prefixes known from automake"""
    return standard_add_prefixes()

#############################################################################
def StandardPrimaryMainPrefixes(primary=None,**kw):
    """Return allowed dir prefixes for given PRIMARY name"""
    return standard_primary_main_prefixes(primary)

#############################################################################
def StandardManSections(**kw):
    """Interface to `standard_man_sections()`"""
    return standard_man_sections()

def RSplitPrimaryName(uname, **kw):
    """Interface to `rsplit_primary_name()`."""
    args = ()
    try:                args += (kw['primary_names'],)
    except KeyError:    args += (None,)
    try:                args += (kw['use_std_primary_names'],)
    except KeyError:    args += (True,)
    return rsplit_primary_name(uname, *args)
        
#############################################################################
def DecomposeName(funame,**kw):
    """Interface to `decompose_name()`."""
    args = ()
    try:                args += (kw['primary_names'],)
    except KeyError:    args += (None,)
    try:                args += (kw['main_prefixes'],)
    except KeyError:    args += (None,)
    try:                args += (kw['add_prefixes'],)
    except KeyError:    args += (None,)
    try:                args += (kw['use_std_primary_names'],)
    except KeyError:    args += (True,)
    try:                args += (kw['use_std_main_prefixes'],)
    except KeyError:    args += (True,)
    try:                args += (kw['use_std_add_prefixes'],)
    except KeyError:    args += (True,)
    return decompose_name(funame, *args)

#############################################################################
def EnsureNameSanity(funame,**kw):
    """Interface to `ensure_name_sanity()`"""
    args = ()
    try:             args += (kw['primary_names'],)
    except KeyError: args +=(None,) 
    try:             args += (kw['main_prefixes'],)
    except KeyError: args +=(None,)
    try:             args += (kw['add_prefixes'],)
    except KeyError: args +=(None,) 
    try:             args += (kw['primary_main_prefixes'],)
    except KeyError: args +=(None,)
    try:             args += (kw['forbid_primary_main_prefixes'],)
    except KeyError: args +=(None,)
    try:             args += (kw['forbid_primary_add_prefixes'],)
    except KeyError: args +=(None,)
    try:             args += (kw['forbid_main_add_prefixes'],)
    except KeyError: args +=(None,)
    try:             args += (kw['use_std_primary_names'],)
    except KeyError: args +=(True,)
    try:             args += (kw['use_std_main_prefixes'],)
    except KeyError: args +=(True,)
    try:             args += (kw['use_std_add_prefixes'],)
    except KeyError: args +=(True,)
    try:             args += (kw['use_std_primary_main_prefixes'],)
    except KeyError: args +=(True,)
    try:             args += (kw['use_std_forbid_primary_main_prefixes'],)
    except KeyError: args +=(True,)
    try:             args += (kw['use_std_forbid_primary_add_prefixes'],)
    except KeyError: args +=(True,)
    try:             args += (kw['use_std_forbid_main_add_prefixes'],)
    except KeyError: args +=(True,)
    return ensure_name_sanity(funame, *args)

#############################################################################
def RSplitMainPrefix(uname, **kw):
    """Interface to `rsplit_main_prefix()`."""
    args = ()
    try:                args += (kw['main_prefixes'],)
    except KeyError:    args += (None,)
    try:                args += (kw['use_std_main_prefixes'],)
    except KeyError:    args += (True,)
    return rsplit_main_prefix(uname, *args)

#############################################################################
def RSplitAddPrefix(uname, **kw):
    """Interface to `rsplit_add_prefix()`."""
    args = ()
    try:                args += (kw['add_prefixes'],)
    except KeyError:    args += (None,)
    try:                args += (kw['use_std_add_prefixes'],)
    except KeyError:    args += (True,)
    return rsplit_add_prefix(uname, *args)

#############################################################################
def IsInstallExecPrefix(prefix, **kw):
    """Interface to `is_install_exec_prefix()`."""
    args = ()
    try:                args += (kw['main_prefixes'],)
    except KeyError:    args += (None,)
    try:                args += (kw['use_std_main_prefixes'],)
    except KeyError:    args += (True,)
    return is_install_exec_prefix(prefix, *args)

#############################################################################
def IsInstallDataPrefix(prefix, **kw):
    """Interface to `is_install_data_prefix()`."""
    args = ()
    try:                args += (kw['main_prefixes'],)
    except KeyError:    args += (None,)
    try:                args += (kw['use_std_main_prefixes'],)
    except KeyError:    args += (True,)
    return is_install_data_prefix(prefix, *args)

#############################################################################
def IsInstallExecName(funame, **kw):
    """Interface to `is_install_exec_name()`."""
    args = ()
    try:                args += (kw['primary_names'],)
    except KeyError:    args += (None,)
    try:                args += (kw['main_prefixes'],)
    except KeyError:    args += (None,)
    try:                args += (kw['use_std_primary_names'],)
    except KeyError:    args += (True,)
    try:                args += (kw['use_std_main_prefixes'],)
    except KeyError:    args += (True,)
    return is_install_exec_name(funame, *args)

#############################################################################
def IsInstallDataName(funame, **kw):
    """Interface to `is_install_data_name()`."""
    args = ()
    try:                args += (kw['primary_names'],)
    except KeyError:    args += (None,)
    try:                args += (kw['main_prefixes'],)
    except KeyError:    args += (None,)
    try:                args += (kw['use_std_primary_names'],)
    except KeyError:    args += (True,)
    try:                args += (kw['use_std_main_prefixes'],)
    except KeyError:    args += (True,)
    return is_install_data_name(funame, *args)

#############################################################################
def FilterInstallExecNames(funames,**kw):
    """Filter uniform names and return only these which are to be handled by
    ``install-exec`` target

    **Example usage:**

    .. python::
        >>> from SConsGnuVariables.AmUniformNames import FilterInstallExecNames
        >>> funames = ['bin_PROGRAMS', 'lib_LIBRARIES', 'nobase_include_HEADERS', 'sysconf_DATA']
        >>> FilterInstallExecNames(funames)
        ['bin_PROGRAMS', 'lib_LIBRARIES', 'sysconf_DATA']
        
    :Parameters:
        funames
            uniform variable names,

    :Keywords:
        primary_names : sequence
            user-defined primary names (default: None)
        main_prefixes : sequence
            user-defined directory prefixes (default: None)
        use_std_primary_names : boolean
            use also standard predefined primary names (default: True)
        use_std_main_prefixes : boolean
            use also standard predefined directory prefixes (default: True)

    :Return:
        returns list of variable names that should be handled by
        ``install-exec``
    """
    return [funame for funame in funames if IsInstallExecName(funame,**kw)]
  
#############################################################################
def FilterInstallDataNames(funames,**kw):
    """Filter uniform names and return only these which are to be handled by
    ``install-data`` target

    :Parameters:
        funames
            uniform variable names,

    :Keywords:
        primary_names : sequence 
            user-defined primary names (default: None)
        main_prefixes : sequence
            user-defined directory prefixes (default: None)
        use_std_primary_names : boolean
            use also standard predefined primary names (default: True)
        use_std_main_prefixes : boolean
            use also standard predefined directory prefixes (default: True)
    
    :Return:
        returns list of variable names that should be handled by
        ``install-data``

    **Example usage:**

    .. python::
        >>> from SConsGnuVariables.AmUniformNames import FilterInstallDataNames
        >>> funames =  ['bin_PROGRAMS', 'lib_LIBRARIES', 'nobase_include_HEADERS', 'sysconf_DATA']
        >>> FilterInstallDataNames(funames)
        ['nobase_include_HEADERS']
    """
    return [funame for funame in funames if IsInstallDataName(funame,**kw)]

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
