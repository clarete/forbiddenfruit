from datetime import datetime
from forbiddenfruit import curse, reverse

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
