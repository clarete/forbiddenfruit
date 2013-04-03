Forbidden Fruit
===============

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
