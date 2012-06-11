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

env = Environment()
Export(['env'])

# Run requested examples (we have 4 of them now)
for n in range(1,5):
  exN = 'ex%d' % n 
  if exN in COMMAND_LINE_TARGETS:
      SConscript('examples/%s/SConscript' % exN)
      AlwaysBuild(Alias(exN))

epydoc = env.Detect(['epydoc'])
if epydoc:
   epydocflags = '-v --html --css grayscale --inheritance listed'
   epydoccom = ' '.join([epydoc,'-o $TARGET.dir', epydocflags,
                         'SConsGnuVariables'])
   source =  env.Glob('SConsGnuVariables/*.py')
   target = 'doc/api/index.html'
   api_doc = env.Command(target, source, epydoccom)
   AlwaysBuild(Alias('api-doc', api_doc))


