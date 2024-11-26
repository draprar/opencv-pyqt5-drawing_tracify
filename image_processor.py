import cv2
import numpy as np


def convert_to_grayscale(image):
    """
    Converts the input image to grayscale.

    Args:
        image (np.ndarray): Input image in BGR format.

    Returns:
        np.ndarray: Grayscale image.
    """
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def apply_sketch_effect(image):
    """
    Converts the input image into a sketch-like image.

    Args:
        image (np.ndarray): Input image in BGR format.

    Returns:
        np.ndarray: Sketch-like image.
    """
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    inverted_image = cv2.bitwise_not(gray_image)
    blurred_image = cv2.GaussianBlur(inverted_image, (21, 21), 0)
    sketch_image = cv2.divide(gray_image, 255 - blurred_image, scale=256)
    return sketch_image


def apply_contour_effect(image):
    """
    Extracts the contours from the input image.

    Args:
        image (np.ndarray): Input image in BGR format.

    Returns:
        np.ndarray: Contour image.
    """
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray_image, 50, 150)
    return edges


def apply_tattoo_calc_effect(image):
    """
    Generates a high-contrast image suitable for creating tattoo templates.

    Args:
        image (np.ndarray): Input image in BGR format.

    Returns:
        np.ndarray: High-contrast binary image.
    """
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY)
    return binary_image
