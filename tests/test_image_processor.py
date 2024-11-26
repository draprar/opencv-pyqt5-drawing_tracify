import cv2
import numpy as np
import pytest
from image_processor import (
    convert_to_grayscale,
    apply_sketch_effect,
    apply_contour_effect,
    apply_tattoo_calc_effect,
)


@pytest.fixture
def sample_image():
    """Creates a sample BGR image for testing."""
    return np.array(
        [[[255, 0, 0], [0, 255, 0], [0, 0, 255]],  # Blue, Green, Red
         [[255, 255, 0], [0, 255, 255], [255, 0, 255]],  # Cyan, Yellow, Magenta
         [[0, 0, 0], [127, 127, 127], [255, 255, 255]]],  # Black, Gray, White
        dtype=np.uint8,
    )


def test_convert_to_grayscale(sample_image):
    """Test the grayscale conversion function."""
    gray_image = convert_to_grayscale(sample_image)
    assert gray_image.shape == (3, 3)  # Ensure grayscale has one channel
    assert gray_image.dtype == np.uint8


def test_apply_sketch_effect(sample_image):
    """Test the sketch effect."""
    sketch_image = apply_sketch_effect(sample_image)
    assert sketch_image.shape == (3, 3)  # Ensure output matches input dimensions
    assert sketch_image.dtype == np.uint8


def test_apply_contour_effect(sample_image):
    """Test the contour effect."""
    contour_image = apply_contour_effect(sample_image)
    assert contour_image.shape == (3, 3)  # Ensure output matches input dimensions
    assert contour_image.dtype == np.uint8


def test_apply_tattoo_calc_effect(sample_image):
    """Test the tattoo template effect."""
    tattoo_image = apply_tattoo_calc_effect(sample_image)
    assert tattoo_image.shape == (3, 3)  # Ensure output matches input dimensions
    assert tattoo_image.dtype == np.uint8
    assert np.all((tattoo_image == 0) | (tattoo_image == 255))  # Binary image
