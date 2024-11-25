import cv2
import numpy as np


def convert_to_grayscale(image):
    """
    Converts the input image to grayscale.

    Args:
        image (np.ndarray): The input image in BGR format.

    Returns:
        np.ndarray: The grayscale version of the input image.
    """
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
