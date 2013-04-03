# Forbidden Fruit

This project aims to give you the way to find heaven in tests, but it might
lead you to hell if you use it on production code.

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

