# forbiddenfruit - Patch built-in python objects
#
# Copyright (c) 2013  Lincoln de Sousa <lincoln@comum.org>
#
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

import os
from setuptools import setup, find_packages, Extension


ffruit = Extension('ffruit', sources=['tests/unit/ffruit.c'])

local_file = lambda f: \
    open(os.path.join(os.path.dirname(__file__), f)).read()

if __name__ == '__main__':
    setup(
        name='forbiddenfruit',
        version='0.1.1',
        description='Patch python built-in objects',
        long_description=local_file('README.md'),
        author='Lincoln de Sousa',
        author_email='lincoln@comum.org',
        url='https://github.com/clarete/forbiddenfruit',
        packages=find_packages(exclude=['*tests*']),
        ext_modules=[ffruit],
    )
