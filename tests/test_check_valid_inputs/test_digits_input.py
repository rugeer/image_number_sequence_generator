import pytest
from script import check_valid_inputs
from script import DigitsNotList, ValuesNotInteger, InvalidRange

spacing_range, image_width = (1, 3), 100

incorrect_object_types = [
    3, 3.1, '3', {2, 4, 4, 5}, dict([('3', 2)])
]

invalid_elements = [
    [3.1, 3], ['3', '5'], [[1], [2]]
]

invalid_range = [
    [-1, 3], [4, 10]
]


class TestIncorrectDigitInput:
    @pytest.mark.parametrize("digits", incorrect_object_types)
    def test_input_type(self, digits):
        """Error if not list"""
        with pytest.raises(DigitsNotList):
            check_valid_inputs(digits, spacing_range, image_width)

    @pytest.mark.parametrize("digits", invalid_elements)
    def test_each_element_type(self, digits):
        """Error if at least one element is not an integer"""
        with pytest.raises(ValuesNotInteger):
            check_valid_inputs(digits, spacing_range, image_width)

    @pytest.mark.parametrize("digits", invalid_range)
    def test_range(self, digits):
        """Error if elements not in range 0-9"""
        with pytest.raises(InvalidRange):
            check_valid_inputs(digits, spacing_range, image_width)

