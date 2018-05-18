import pytest
from script import generate_numbers_sequence
from script import SpacingNotTuple, SpacingInvalidSize, ValuesNotInteger
from script import MaxSpaceTooLarge, InvalidSpacingRange, InvalidSpacingValue

digits, image_width = [1, 2, 3], 250

incorrect_object_types = [
    [1, 2, 3], {2, 4, 4, 5}, dict([('3', 2)])
]

incorrect_size = [
    (1, 3, 4), (1,)
]

invalid_elements = [
    ('2', 3), ({1}, 3), (dict([('3', 2)]), 3)
]

invalid_range = [
    (4, 2)
]

negative_value = [
    (-3, -1), (-1, 1)
]

max_space_value = int(image_width / (len(digits) - 1))
invalid_max_space = [
    (1, max_space_value), (1, max_space_value + 1)
]


class TestIncorrectSpacingRangeInput:
    @pytest.mark.parametrize("spacing_range", incorrect_object_types)
    def test_input_type(self, spacing_range):
        """Error if wrong type, has to be tuple"""
        with pytest.raises(SpacingNotTuple):
            generate_numbers_sequence(digits, spacing_range, image_width)

    @pytest.mark.parametrize("spacing_range", incorrect_size)
    def test_input_size(self, spacing_range):
        """Error if input size not of correct size, has to be size 2"""
        with pytest.raises(SpacingInvalidSize):
            generate_numbers_sequence(digits, spacing_range, image_width)

    @pytest.mark.parametrize("spacing_range", invalid_elements)
    def test_each_element_type(self, spacing_range):
        """Error if at least one element is not integer"""
        with pytest.raises(ValuesNotInteger):
            generate_numbers_sequence(digits, spacing_range, image_width)

    @pytest.mark.parametrize("spacing_range", invalid_range)
    def test_range(self, spacing_range):
        """Error when max range not larger than min range"""
        with pytest.raises(InvalidSpacingRange):
            generate_numbers_sequence(digits, spacing_range, image_width)

    @pytest.mark.parametrize("spacing_range", negative_value)
    def test_negative_range(self, spacing_range):
        """Error when min range negative"""
        with pytest.raises(InvalidSpacingValue):
            generate_numbers_sequence(digits, spacing_range, image_width)

    @pytest.mark.parametrize("spacing_range", invalid_max_space)
    def test_max_range(self, spacing_range):
        """Spaces larger than the image."""
        with pytest.raises(MaxSpaceTooLarge):
            generate_numbers_sequence(digits, spacing_range, image_width)
