import numpy as np
import mnist
from script import crop_image

train_images = mnist.train_images()

image = train_images[1]
image_cropped = crop_image(image)


def test_output_type():
    assert isinstance(image_cropped, np.ndarray)


def test_size():
    height = image_cropped.shape[0] == 28
    width = image_cropped.shape[1] <= image.shape[1]
    assert all([height, width])
