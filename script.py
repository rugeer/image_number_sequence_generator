import mnist
import numpy as np
import sys
from skimage import img_as_float
from scipy.misc import imsave
# from skimage.transform import resize


train_images = mnist.train_images()
train_labels = mnist.train_labels()


def generate_numbers_sequence(digits, spacing_range, image_width):
    """
    Generate an image that contains the sequence of given numbers, spaced
    randomly using an uniform distribution.

    Parameters
    ----------
    digits:
        A list-like containing the numerical values of the digits from which
        the sequence will be generated (for example [3, 5, 0]).
    spacing_range:
        a (minimum, maximum) pair (tuple), representing the min and max spacing
        between digits. Unit should be pixel.
    image_width:
        specifies the width of the image in pixels.

    Returns
    -------
    The image containing the sequence of numbers. Images should be represented
    as floating point 32bits numpy arrays with a scale ranging from 0 (black) to
    1 (white), the first dimension corresponding to the height and the second
    dimension to the width.
    """
    # Test whether all inputs ale valid
    check_valid_inputs(digits, spacing_range, image_width)

    # For each digit, get the indexes of the images from the MNIST dataset
    indexes_of_images = get_indexes_digits(digits)

    # Select a random image for each digit from the MNIST dataset by index
    images_index = select_images_for_digits(digits, indexes_of_images)

    # Generate an image representing the sequences of the digits
    final_image = generate_final_image(images_index, spacing_range)

    # Calculate remaining space in the image
    horizontal_width = image_width - final_image.shape[1]
    # Error if final image does not fit
    if horizontal_width < 0:
        raise InvalidCombinationOfParameters('The sequence of the digits does not fit the image. '
                                             'The size of the digits with spaces is too large. ')
    # Fill remaining space on the right hand side from the last digit with black colour
    if horizontal_width > 0:
        black_space_fill = generate_black_space_fill(horizontal_width)
        final_image = np.concatenate((final_image, black_space_fill), axis=1)

    return img_as_float(final_image).astype(np.float32)


def generate_black_space_fill(horizontal_width):
    """
    Generate a black image 28 pixels high with a specified width.

    Parameters
    ----------
    horizontal_width:
        int, number of pixels remaining horizontally
    Returns
    -------
    numpy.ndarray image
    """
    return np.full((28, horizontal_width), 0)


def generate_final_image(images_index, spacing_range):
    """
    Generate the final image of sequences of digits spaced randomly using uniform distribution with the specified
    range.

    Parameters
    ----------
    images_index:
        list, indexes of images for each digit
    spacing_range:
        a (minimum, maximum) pair (tuple), representing the min and max spacing
        between digits. Unit should be pixel.

    Returns
    -------
    numpy.ndarray, an image containing the sequences of numbers separated by the space image.
    """
    final_image = crop_image(train_images[images_index[0]])
    for image_index in images_index[1:]:
        new_image = crop_image(train_images[image_index])
        space_between_digits = get_space_between_digits(spacing_range)
        image_of_space = generate_black_space_fill(space_between_digits)
        final_image = np.concatenate((final_image, image_of_space, new_image), axis=1)

    return final_image


def select_images_for_digits(digits, indexes_of_images):
    """
    For each digit select a random image.

    Parameters
    ----------
    digits:
        A list-like containing the numerical values of the digits from which
        the sequence will be generated (for example [3, 5, 0]).
    indexes_of_images:
        dict, dictionary with the indexes of images for each digit

    Returns
    -------
    list with indexes of the randomly selected images for each digit.
    """
    images_index = []
    for digit in digits:
        images_index.append(np.random.choice(indexes_of_images[str(digit)], size=1)[0])

    return images_index


def get_space_between_digits(spacing_range):
    """
    Generate a value representing the size of the space between each two digits in pixels.
    
    Parameters
    ----------
    spacing_range:
        a (minimum, maximum) pair (tuple), representing the min and max spacing
        between digits. Unit should be pixel.

    Returns
    -------
    int, space between any two digits.
    """
    space_between_images = int(np.random.uniform(low=spacing_range[0], high=spacing_range[1], size=1).round(0))
    
    return space_between_images


def get_indexes_digits(digits):
    """
    Get indexes of images for each digit from the MNIST dataset
    
    Parameters
    ----------
    digits:
        A list-like containing the numerical values of the digits from which
        the sequence will be generated (for example [3, 5, 0]).

    Returns
    -------
    A dictionary with keys representing different digits and values representing the indexes of the images in the MNIST
    dataset for each of the digits.
    """
    indexes_of_images = {}
    for digit in set(digits):
        indexes_of_images[str(digit)] = np.array(range(0, train_labels.shape[0]))[train_labels == digit]
        
    return indexes_of_images


def crop_image(img):
    """
    Crop the image by removing columns that are all black, i.e., value 0.

    Parameters
    ----------
    img:
        numpy.ndarray, an image to crop.

    Returns
    -------
    The cropped image as a numpy.ndarray.
    """
    mask = img > 0
    return img[:, mask.any(0)]


# def resize_image(img, horizontal_size):
#     """
#     Resize the image horizontally.
#
#     Parameters
#     ----------
#     img:
#         numpy.ndarray, an image to crop.
#     horizontal_size:
#         int, horizontal size of the final image in pixels
#
#     Returns
#     -------
#     The resized image as a numpy.ndarray.
#     """
#
#     return resize(img.astype(np.uint8), output_shape=(28, horizontal_size), mode='reflect')


def check_valid_inputs(digits, spacing_range, image_width):
    """
    Test whether parameters have valid format and values.

    Parameters
    ----------
    digits:
        A list-like containing the numerical values of the digits from which
        the sequence will be generated (for example [3, 5, 0]).
    spacing_range:
        a (minimum, maximum) pair (tuple), representing the min and max spacing
        between digits. Unit should be pixel.
    image_width:
        specifies the width of the image in pixels.

    Returns
    -------
    None if all inputs are valid, otherwise an error is raised with an explanation.
    """
    # Ensure all input is valid
    if not isinstance(digits, list):
        raise DigitsNotList("Only digits in a list can be provided")
    if not all([isinstance(digit, int) for digit in digits]):
        raise ValuesNotInteger("Each element of the digits list has to be an integer")
    if any([digit not in range(0, 10) for digit in digits]):
        raise InvalidRange("Only digits (integers) in range 0-9 can be selected")
    if not isinstance(spacing_range, tuple):
        raise SpacingNotTuple("Spacing range can only be provided as a tuple")
    if len(spacing_range) != 2:
        raise SpacingInvalidSize("Spacing range has to be a tuple of size 2")
    if not all([isinstance(space, int) for space in spacing_range]):
        raise ValuesNotInteger("The maximum and minimum spacing range values have to be integers")
    if not spacing_range[1] >= spacing_range[0]:
        raise InvalidSpacingRange("Maximum spacing has to be larger or equal to the minimum spacing")
    if spacing_range[0] < 0:
        raise InvalidSpacingValue("Spacing have to be a positive numbers")
    if not isinstance(image_width, int):
        raise ImageWidthNotInteger("Image width has to be an integer")
    if image_width <= 0:
        raise InvalidImageWidth("Image width has to be a positive")
    if image_width - spacing_range[1] * (len(digits) - 1) <= 0:
        raise MaxSpaceTooLarge("Maximum is too large. Spaces between digits might be larger than the final image.")

    pass


class InvalidCombinationOfParameters(Exception):
    pass


class DigitsNotList(Exception):
    pass


class InvalidRange(Exception):
    pass


class SpacingNotTuple(Exception):
    pass


class InvalidSpacingRange(Exception):
    pass


class InvalidSpacingValue(Exception):
    pass


class ImageWidthNotInteger(Exception):
    pass


class InvalidImageWidth(Exception):
    pass


class MaxSpaceTooLarge(Exception):
    pass


class ValuesNotInteger(Exception):
    pass


class SpacingInvalidSize(Exception):
    pass


if __name__ == "__main__":
    digits_list = list(map(int, sys.argv[1].strip('[]').split(',')))
    image = generate_numbers_sequence(digits=digits_list, spacing_range=(int(sys.argv[2]), int(sys.argv[3])),
                                      image_width=int(sys.argv[4]))
    imsave('generated_image.png', image)
