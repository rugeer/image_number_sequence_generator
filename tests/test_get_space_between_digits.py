from script import get_space_between_digits

spacing_range = (1, 5)

space = get_space_between_digits(spacing_range)


def test_answer_type():
    assert isinstance(space, int)


def test_range():
    """Range has to be between the upper and lower limit"""
    upper = space <= spacing_range[1]
    lower = space >= spacing_range[0]
    assert all([upper, lower])
