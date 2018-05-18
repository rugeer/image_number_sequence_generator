import pytest
from script import generate_numbers_sequence
from script import ImageWidthNotInteger, InvalidImageWidth

digits, spacing_range = [1, 2, 3], (1, 3)

incorrect_object_types = [
    '250', 250.0, {250}, [250], dict([('3', 2)])
]

invalid_value = [
    -1, 0
]


class TestIncorrectImageWidthInput:
    @pytest.mark.parametrize("image_width", incorrect_object_types)
    def test_input_type(self, image_width):
        """Error if not integer"""
        with pytest.raises(ImageWidthNotInteger):
            generate_numbers_sequence(digits, spacing_range, image_width)

    @pytest.mark.parametrize("image_width", invalid_value)
    def test_invalid_value(self, image_width):
        """Error if negative or zero"""
        with pytest.raises(InvalidImageWidth):
            generate_numbers_sequence(digits, spacing_range, image_width)
