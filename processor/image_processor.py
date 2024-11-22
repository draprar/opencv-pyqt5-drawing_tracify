import cv2
import numpy as np
from tkinter import Tk, filedialog


def load_image():
    """Prompt the user to load an image file."""
    Tk().withdraw()
    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")]
    )
    if file_path:
        return cv2.imread(file_path)
    else:
        raise FileNotFoundError("No file selected.")


def save_image(image, file_name="output.jpg"):
    """Save the processed image to disk."""
    cv2.imwrite(file_name, image)
    print(f"Image saved as {file_name}")


def edge_detection(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    return edges


def pencil_sketch(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    inverted = 255 - gray
    blurred = cv2.GaussianBlur(inverted, (21, 21), 0)
    sketch = cv2.divide(gray, 255 - blurred, scale=256)
    return sketch


def thresholding(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    return thresh


def posterization(image, levels=4):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    poster = (gray // (256 // levels)) * (256 // levels)
    return poster


def contour_highlight(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contour_image = np.zeros_like(image)
    cv2.drawContours(contour_image, contours, -1, (255, 255, 255), 1)
    return contour_image
