import numpy as np
from script import select_images_for_digits

digits = [1, 3]

indexes_of_images = {
    '1': np.array([1, 3, 4]),
    '3': np.array([2, 5, 6])
}

images = select_images_for_digits(digits, indexes_of_images)


def test_output_type():
    assert isinstance(images, list)


def test_elements_integers():
    assert [isinstance(index_, np.int64) for index_ in images]


def test_size():
    assert len(images) == len(digits)


def test_correct_indexes():
    """Test that the indices were selected for the correct digit"""
    index_0 = images[0] in indexes_of_images[str(digits[0])]
    index_1 = images[1] in indexes_of_images[str(digits[1])]
    assert all([index_0, index_1])
