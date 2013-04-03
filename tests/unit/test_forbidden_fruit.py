from forbiddenfruit import curse, reverse


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
