from datetime import datetime
from forbiddenfruit import curses, curse, reverse

# Our stub! :)
from . import ffruit


def test_cursing_a_builting_class():

    # Given that I have a function that returns *blah*
    def words_of_wisdom(self):
        return self * "blah "

    # When I try to curse a built-in class with that function
    curse(int, "words_of_wisdom", words_of_wisdom)

    # Then I see that the class was cursed
    assert (2).words_of_wisdom() == "blah blah "
    assert 'words_of_wisdom' in dir(int)


def test_cursing_a_builting_class_with_a_class_method():

    # Given that I have a function that returns *blah*
    def hello(self):
        return "blah"

    # When I try to curse a built-in class with that function
    curse(str, "hello", classmethod(hello))

    # Then I see that the class was cursed
    assert str.hello() == "blah"
    assert 'hello' in dir(str)


def test_reversing_a_builtin():
    # Given that I have a cursed object
    curse(str, 'stuff', property(lambda s: s * 2))

    # When I bless it
    reverse(str, 'stuff')

    # Then I see that str won't contain
    assert 'stuff' not in dir(str)


def test_dir_filtering():
    # Given that I curse the `str` built-in asking the curse to hide it from
    # the built-in `dir()` function
    curse(str, "my_stuff", "blah", hide_from_dir=True)

    # Then I see that my new stuff is installed but without appearing on dir
    assert str.my_stuff == "blah"
    assert "my_stuff" not in dir(str)


def test_dir_filtering_same_symbol_different_type():
    # Given that I curse both `str` and `int` built-ins but only hide the new
    # attribute from the one installed on `str`
    curse(str, "attr_x", "blah", hide_from_dir=True)
    curse(int, "attr_x", "blah")

    # Then I see that both attributes were installed, but only one is filtered
    # by dir
    assert str.attr_x == "blah"
    assert "attr_x" not in dir(str)

    assert int.attr_x == "blah"
    assert "attr_x" in dir(int)


def test_dir_filtering_same_symbol_different_instance():
    # Given that I curse both `str` and `int` built-ins
    curse(str, "attr_y", "stuff", hide_from_dir=True)
    curse(int, "attr_y", "stuff")

    # Then I see that the dir() thing also works for instances
    assert "Hello".attr_y == "stuff"
    assert "attr_y" not in dir("hello")

    assert (1).attr_y == "stuff"
    assert "attr_y" in dir(1)


def test_overriding_class_method():
    # Given that I have a cursed object
    curse(datetime, 'now', classmethod(lambda *p: False))

    # Then I see that the method was replaced, but we still have the original
    # method set as `_c_apppend`
    assert '_c_now' in dir(datetime)
    assert datetime.now() is False
    assert datetime(2013, 4, 5).now() is False


def test_overriding_instance_method():
    # Given that I have an instance of a `Dummy` object
    obj = ffruit.Dummy()

    # When I curse an instance method
    curse(ffruit.Dummy, "my_method", lambda *a, **k: "Yo!")

    # Then I see that my object was cursed properly
    assert obj.my_method() == "Yo!"


def test_overriding_non_c_things():
    "The `curse` function should not blow up on non-c python objs"

    # Given that I have an instance of a python class
    class Yo(object):
        pass

    obj = Yo()

    # When I curse an instance method
    curse(Yo, "my_method", lambda *a, **k: "Yo" * 2)

    # Then I see that my object was cursed properly
    assert obj.my_method() == "YoYo"


def test_overriding_dict_pop():
    "The `curse` function should be able to curse existing symbols"

    # Given that I have an instance of a python class
    obj = {'a': 1, 'b': 2}

    # When I curse an instance method
    curse(dict, "pop", lambda self, key: self[key])

    # Then I see that my object was cursed properly
    assert obj.pop('a') == 1
    assert obj.pop('b') == 2
    assert 'a' in obj
    assert 'b' in obj


def test_curses_decorator():
    "curses() should curse a given klass with the decorated function"

    # Given that I have a decorated func
    @curses(str, 'md_title')
    def markdown_title(self):
        return '# %s' % self.title()

    # Then I see the `str` class was patched
    assert "lincoln".md_title() == "# Lincoln"


def test_dir_without_args_returns_names_in_local_scope():
    """dir() without arguments should return the names from the local scope
    of the calling frame, taking into account any indirection added
    by __filtered_dir__
    """

    # Given that I have a local scope with some names bound to values
    z = 1
    some_name = 42

    # Then I see that `dir()` correctly returns a sorted list of those names
    assert 'some_name' in dir()
    assert dir() == sorted(locals().keys())
