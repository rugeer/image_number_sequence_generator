import numpy as np
import pytest
from script import generate_numbers_sequence
from script import InvalidCombinationOfParameters

image_width, spacing_range, digits = 100, (1, 3), [1, 2]
image = generate_numbers_sequence(digits, spacing_range, image_width)


def test_output_type():
    assert isinstance(image, np.ndarray)


def test_size():
    height = image.shape[0] == 28
    width = image.shape[1] == image_width
    assert all([height, width])


def test_image_too_large():
    """Error if the image is larger than the set width"""
    with pytest.raises(InvalidCombinationOfParameters):
        generate_numbers_sequence([1, 2, 3, 4, 5, 6, 7, 7], (1, 3), 50)