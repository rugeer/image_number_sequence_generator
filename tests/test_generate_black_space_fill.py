import numpy as np
from script import generate_black_space_fill

image = generate_black_space_fill(3)


def test_height():
    assert image.shape[0] == 28


def test_width():
    assert image.shape[1] == 3


def test_black_image():
    """Test if image fully black"""
    assert np.all(image == 0)
