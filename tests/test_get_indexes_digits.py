import mnist
from script import get_indexes_digits
from collections import Counter

train_images = mnist.train_images()
train_labels = mnist.train_labels()
digits = [1, 3]

indexes = get_indexes_digits(digits)


def test_output_type():
    assert isinstance(indexes, dict)


def test_keys():
    """Test whether all and only the selected digits are in the dictionary keys"""
    keys_in_dict = all([str(digit) in indexes for digit in digits])
    n_keys = len(indexes.keys()) == len(digits)
    assert all([keys_in_dict, n_keys])


def test_correct_indexes():
    """Test whether all indexes for each key correspond to the correct label"""
    correct = []
    for digit in digits:
        correct.append(all(train_labels[indexes[str(digit)]] == digit))
    assert all(correct)


def test_correct_size():
    """Test that all indexes add up to the size of the dataset"""
    unique_values = dict(Counter(train_labels.tolist()))
    size = []
    for digit in digits:
        size.append(len(indexes[str(digit)]) == unique_values[digit])
    assert all(size)
