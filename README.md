SConsGnuVariables
=================

Welcome to SConsGnuVariables.

This package provides SCons with GNU variables (e.g. direcory wariables)
commonly used by GNU Makefiles. You may easilly add to your command line
variables or options such as $prefix or $bindir.

INSTALLATION
------------

Just copy entire directory SConsGnuVariables to your local ``site_scons``.

    cp -r scons-gnu-variables/SConsGnuVariables your/project/site_scons/

USAGE
-----

See API documentation (you may need to generate it, see *DOCUMENTATION*).
Here is an example of what may be put to ``SConsctruct`` in order to add
all supported GNU directory variables to your scons command line variables

```python
    # SConstruct #
    from SConsGnuVariables import GnuDirVariables
    env = Environment()
    gnuvars = GnuDirVariables.AsSConsVariables()
    gnuvars.Update(env, ARGUMENTS)
    print "${prefix}: ", env.subst('${prefix}')
    print "${bindir}: ", env.subst('${bindir}')
``` 

The result of ``scons -Q`` will be

    ${prefix}:  /usr/local
    ${bindir}:  /usr/local/bin
    scons: `.' is up to date.

The result of ``scons -Q prefix=/usr`` will be

    ${prefix}:  /usr
    ${bindir}:  /usr/bin
    scons: `.' is up to date.


DOCUMENTATION
-------------

API documentation can be generated from top level directory with the following
command

  scons api-doc

To generate documentation, you may need following packages on your system:

  * epydoc <http://epydoc.sourceforge.net/>
  * python-docutils <http://pypi.python.org/pypi/docutils>
  * python-pygments <http://pygments.org/>

The generated documentation is located within ``doc/api`` directory.


RUNNING EXAMPLES
----------------

Each example consists of its `SConscript' file located under examples/exN,
and ocassionally may involve other files within same directory.
The examples should be run from top-level directory by invoking 
    
  scons ex1           # For example/ex1
  scons ex1 --help    # It may be worth to see help message
  ...
 
LICENSE
-------
Copyright &copy; 2012 by Paweł Tomulik

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE
