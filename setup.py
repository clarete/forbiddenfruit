# forbiddenfruit - Patch built-in python objects
#
# Copyright (c) 2013,2019  Lincoln de Sousa <lincoln@clarete.li>
#
# This program is dual licensed under GPLv3 and MIT.
#
# GPLv3
# -----
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# MIT
# ---
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import os
from setuptools import setup, find_packages, Extension

if os.environ.get('FFRUIT_EXTENSION', '') == 'true':
    ext_modules = [Extension('ffruit', sources=['tests/unit/ffruit.c'])]
else:
    ext_modules = []


local_file = lambda f: \
    open(os.path.join(os.path.dirname(__file__), f)).read()

if __name__ == '__main__':
    setup(
        name='forbiddenfruit',
        version='0.1.4',
        description='Patch python built-in objects',
        long_description=local_file('README.md'),
        long_description_content_type='text/markdown',
        author='Lincoln de Sousa',
        author_email='lincoln@clarete.li',
        url='https://github.com/clarete/forbiddenfruit',
        packages=find_packages(exclude=['*tests*']),
        ext_modules=ext_modules,
        classifiers=[
            'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
            'License :: OSI Approved :: MIT License',
        ],
    )
