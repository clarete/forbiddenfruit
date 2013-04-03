from forbiddenfruit import curse


def test_cursing_a_builting_class():

    # Given that I have a function that returns *blah*
    def words_of_wisdom(self):
        return self * "blah "

    # When I try to curse a built-in class with that function
    curse(int, "words_of_wisdom", words_of_wisdom)

    # Then I see that the class was cursed
    assert (2).words_of_wisdom() == "blah blah "


def test_cursing_a_builting_class_with_a_class_method():

    # Given that I have a function that returns *blah*
    def hello(self):
        return "blah"

    # When I try to curse a built-in class with that function
    curse(str, "hello", classmethod(hello))

    # Then I see that the class was cursed
    assert str.hello() == "blah"
