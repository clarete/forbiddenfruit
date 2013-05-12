[![Build Status](https://travis-ci.org/clarete/forbiddenfruit.png?branch=master)](https://travis-ci.org/clarete/forbiddenfruit)

# Forbidden Fruit

![Forbidden Fruit](logo.png)

This project aims to help you reach heaven while writing tests, but it
may lead you to hell if used on production code.

It basically allows you to patch built-in objects, declared in C through
python. Just like this:

```python
>>> from forbiddenfruit import curse
>>> def words_of_wisdom(self):
...     return self * "blah "
>>> curse(int, "words_of_wisdom", words_of_wisdom)
>>> assert (2).words_of_wisdom() == "blah blah "
```

Boom! That's it, your `int` class now has the `words_of_wisdom` method. Do
you want to add a `classmethod` to a built-in class? No problem, just do this:

```python
>>> from forbiddenfruit import curse
>>> def hello(self):
...     return "blah"
>>> curse(str, "hello", classmethod(hello))
>>> assert str.hello() == "blah"
```

### Reversing a curse

If you want to free your object from a curse, you can use the `reverse()`
function. Just like this:

```python
>>> from forbiddenfruit import curse, reverse
>>> curse(str, "test", "blah")
>>> assert 'test' in dir(str)
>>> # Time to reverse the curse
>>> reverse(str, "test")
>>> assert 'test' not in dir(str)
```

## Compatibility

Forbidden Fruit runs on all cpython versions I tested so far, which includes
the versions 2.5, 2.6, 2.7, 3.2 and 3.3. Since Forbidden Fruit is fundamentally
dependent on the C API, this library won't work on other python
implementations, such as Jython, pypy, etc.

I might add support for pypy in the future, but It's unlikely that I'll do it
for Jython. But I could happily accept patches for them.

## License

License (GPLv3)

Copyright (C) 2013  Lincoln Clarete <lincoln@comum.org>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

### Logo by

Kimberly Chandler, from The Noun Project

