import pytest
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import Qt
from main import ImageApp
import cv2
import numpy as np
import os


@pytest.fixture
def app(qtbot):
    """Sets up the GUI application for testing."""
    test_app = ImageApp()
    qtbot.addWidget(test_app)
    return test_app


@pytest.fixture
def mock_image(tmpdir):
    """Creates a temporary test image."""
    test_image_path = str(tmpdir / "test_image.png")
    cv2.imwrite(test_image_path, 255 * np.ones((100, 100, 3), dtype=np.uint8))  # White image
    return test_image_path


def test_gui_load_image(qtbot, app, mocker, mock_image):
    """Test if an image can be loaded into the GUI."""
    # Mock the file dialog to return the test image path
    mocker.patch.object(QFileDialog, "getOpenFileName", return_value=(mock_image, ""))

    # Simulate loading the image
    with qtbot.waitSignal(app.load_button.clicked):
        app.load_button.click()

    assert app.original_image is not None  # Check image is loaded


def test_gui_apply_effect(qtbot, app, mock_image, mocker):
    """Test if effects can be applied and displayed in the GUI."""
    # Mock the file dialog to return the test image path
    mocker.patch.object(QFileDialog, "getOpenFileName", return_value=(mock_image, ""))

    # Load the image
    with qtbot.waitSignal(app.load_button.clicked):
        app.load_button.click()

    # Simulate effect selection and application
    app.effect_combo.setCurrentIndex(1)  # Select "Sketch Effect"
    with qtbot.waitSignal(app.apply_button.clicked):
        app.apply_button.click()

    assert app.processed_image is not None  # Check processing happened
    assert app.processed_image.shape == (100, 100)  # Verify output is grayscale/sketch


def test_gui_save_image(qtbot, app, mocker, tmpdir):
    """Test if processed images can be saved."""
    # Mock a processed image
    app.processed_image = 255 * np.ones((100, 100), dtype=np.uint8)

    # Mock the save file dialog to return a test path
    save_path = str(tmpdir / "saved_image.png")
    mocker.patch.object(QFileDialog, "getSaveFileName", return_value=(save_path, ""))

    # Simulate saving the image directly
    app.save_image()

    # Check if the image was saved correctly
    saved_image = cv2.imread(save_path, cv2.IMREAD_GRAYSCALE)
    assert saved_image is not None, "Image was not saved"
    assert np.array_equal(saved_image, app.processed_image), "Saved image does not match the processed image"
