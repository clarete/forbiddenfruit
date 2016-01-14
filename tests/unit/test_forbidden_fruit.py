import sys
from datetime import datetime
from forbiddenfruit import cursed, curses, curse, reverse
from types import FunctionType
from nose.tools import nottest, istest

# Our stub! :)
from . import ffruit



def almost_equal(a, b, e=0.001):
    """Helper method to compare floats"""
    return abs(a - b) < e


skip_legacy = nottest if sys.version_info < (3, 3) else istest

def test_cursing_a_builtin_class():

    # Given that I have a function that returns *blah*
    def words_of_wisdom(self):
        return self * "blah "

    # When I try to curse a built-in class with that function
    curse(int, "words_of_wisdom", words_of_wisdom)

    # Then I see that the class was cursed
    assert (2).words_of_wisdom() == "blah blah "
    assert 'words_of_wisdom' in dir(int)


def test_cursing_a_builtin_class_with_a_class_method():

    # Given that I have a function that returns *blah*
    def hello(self):
        return "blah"

    # When I try to curse a built-in class with that function
    curse(str, "hello", classmethod(hello))

    # Then I see that the class was cursed
    assert str.hello() == "blah"
    assert 'hello' in dir(str)


@skip_legacy
def test_cursing_a_builtin_class_dunder_with_a_random_callable():
    # Given that I have an object that returns *blah*
    class Twelver(object):
        def __call__(self, one, two):
            return 12

    # When I try to curse a built-in class's __sub__ with that function
    curse(str, "__sub__", Twelver())

    # Then I see that the class was cursed
    assert ("hello" - "world") == 12


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


def test_overriding_list_append():
    "The `curse` function should be able to curse existing symbols"

    # Given that I have an instance of a python class
    obj = []

    # When I curse an instance method
    fn =  lambda self, v: self._c_append(v) or self
    foo = curse(list, "append", fn)

    # Then I see that my object was cursed properly
    assert obj.append(1) == [1]
    assert obj.append(2) == [1, 2]
    assert 1 in obj
    assert 2 in obj


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


@skip_legacy
def test_dunder_func_chaining():
    """Overload * (mul) operator to to chaining between functions"""
    def matmul_chaining(self, other):
        if not isinstance(other, FunctionType):
            raise NotImplementedError()
        def wrapper(*args, **kwargs):
            res = other(*args, **kwargs)
            if hasattr(res, "__iter__"):
                return self(*res)
            return self(res)

        return wrapper

    curse(FunctionType, "__mul__", matmul_chaining)
    f = lambda x, y: x * y
    g = lambda x: (x, x)

    squared = f * g

    for i in range(0, 10, 2):
        assert squared(i) == i ** 2


@skip_legacy
def test_dunder_list_map():
    """Overload * (__mul__) operator to apply function to a list"""
    def map_list(func, list_):
        if not callable(func):
            raise NotImplementedError()
        return map(func, list_)

    curse(list, "__mul__", map_list)

    list_ = list(range(10))
    times_2 = lambda x: x * 2

    assert list(times_2 * list_) == list(range(0, 20, 2))


@skip_legacy
def test_dunder_unary():
    """Overload ~ operator to compute a derivative of function"""
    def derive_func(func):
        e = 0.001
        def wrapper(x):
            """Poor man's derivation"""
            x_0 = x - e
            x_1 = x + e
            y_delta = func(x_1) - func(x_0)
            return y_delta / (2 * e)
        return wrapper

    curse(FunctionType, "__inv__", derive_func)

    f = lambda x: x**2 + x
    # true derivation
    f_ = lambda x: 2*x + 1

    assert almost_equal((~f)(10), f_(10))


@skip_legacy
def test_sequence_dunder():
    def derive_func(func, deriv_grad):
        if deriv_grad == 0:
            return func

        e = 0.0000001
        def wrapper(x):
            return (func(x + e) - func(x - e)) / (2 * e)
        if deriv_grad == 1:
            return wrapper
        return wrapper[deriv_grad - 1]

    curse(FunctionType, "__getitem__", derive_func)

    # a function an its derivations
    f = lambda x: x ** 3 - 2 * x ** 2
    f_1 = lambda x: 3 * x ** 2 - 4 * x
    f_2 = lambda x: 6 * x - 4

    for x in range(0, 10):
        x = float(x) / 10.
        assert almost_equal(f(x), f[0](x))
        assert almost_equal(f_1(x), f[1](x))
        # our hacky derivation becomes numerically unstable here
        assert almost_equal(f_2(x), f[2](x), e=.01)


@skip_legacy
def test_dunder_list_revert():
    """Test reversion of a curse with dunders"""
    def map_list(func, list_):
        if not callable(func):
            raise NotImplementedError()
        return map(func, list_)

    curse(list, "__add__", map_list)

    list_ = list(range(10))
    times_2 = lambda x: x * 2

    assert list(times_2 + list_) == list(range(0, 20, 2))

    reverse(list, "__add__")
    try:
        times_2 + list_
    except TypeError:
        pass
    else:
        # should always raise an exception
        assert False


def test_cursing_a_reversed_curse():
    curse(str, 'one', 1)
    assert str.one == 1

    reverse(str, 'one')
    curse(str, 'one', 2)
    assert str.one == 2

@skip_legacy
def test_dunder_str():
    assert str(1) == "1"
    def always_one(self):
        return 'one'
    curse(int, '__str__', always_one)
    assert str(1) == "one"

@skip_legacy
def test_dunder_reverse():
    def type_error_str(self):
        return 'type error'
    curse(TypeError, '__str__', type_error_str)
    te = TypeError("testing")
    assert str(te) == "type error"

    reverse(TypeError, '__str__')
    assert str(te) == "testing"


def test_cursed_context_manager():
    "The `cursed` context manager should curse an existing symbols in a scope"

    # Given that I have an instance of a python class
    obj = {'a': 1, 'b': 2}

    # When I curse an instance method
    with cursed(dict, "open_box", lambda self: 'surprise'):
        # Then I see that my object was cursed properly
        assert obj.open_box() == 'surprise'

    # And it was reversed
    assert "open_box" not in dir(obj)
    assert "open_box" not in dir(dict)


@skip_legacy
def test_cursed_decorator():
    "The `cursed` decorator should curse an existing symbols during a function"

    # Given that I have an instance of a python class
    obj = {'a': 1, 'b': 2}

    # When I curse an instance method using the decorator form of `cursed`
    @cursed(dict, "open_box", lambda self: 'surprise')
    def function():
        # Then I see that my object was cursed properly
        assert obj.open_box() == 'surprise'

    function()

    # And it was reversed
    assert "open_box" not in dir(obj)
    assert "open_box" not in dir(dict)
