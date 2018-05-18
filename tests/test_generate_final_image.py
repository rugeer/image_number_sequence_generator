import mnist
import numpy as np
from script import generate_final_image


train_images = mnist.train_images()
train_labels = mnist.train_labels()
digits = [5, 0]
images_indexes = [0, 1]
final_image = generate_final_image(digits, images_indexes)


def test_output_type():
    assert isinstance(final_image, np.ndarray)


def test_output_height():
    assert final_image.shape[0] == 28
