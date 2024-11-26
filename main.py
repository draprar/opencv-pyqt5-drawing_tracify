import sys
import cv2
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QLabel,
    QFileDialog,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
    QComboBox,
)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from image_processor import (
    convert_to_grayscale,
    apply_sketch_effect,
    apply_contour_effect,
    apply_tattoo_calc_effect,
)


class ImageApp(QMainWindow):
    """
    Main application window for image processing.
    GUI for loading images, applying effects, and saving the results.
    """

    def __init__(self):
        """
        Initializes the main application window and UI components.
        """
        super().__init__()
        self.image_label = QLabel("No Image Loaded")
        self.load_button = QPushButton("Load Image")
        self.effect_combo = QComboBox()
        self.save_button = QPushButton("Save Image")
        self.apply_button = QPushButton("Apply Effect")
        self.original_image = None  # Original loaded image (OpenCV format)
        self.processed_image = None  # Image after applying selected effects
        self.init_ui()  # Set up the UI

    def init_ui(self):
        """
        Sets up the user interface.
        """
        self.setWindowTitle("Tracify")
        self.setGeometry(100, 100, 800, 600)

        # Main layout setup
        main_layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        # Image display label
        self.image_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.image_label)

        # Buttons and combo box for functionalities
        self.load_button.clicked.connect(self.load_image)
        button_layout.addWidget(self.load_button)

        # Dropdown to select effects
        self.effect_combo.addItems(
            ["Grayscale", "Sketch Effect", "Contour Effect", "Tattoo Calc Effect"]
        )
        button_layout.addWidget(self.effect_combo)

        # Button to apply the selected effect
        self.apply_button.clicked.connect(self.apply_effect)
        self.apply_button.setEnabled(False)  # Initially disabled
        button_layout.addWidget(self.apply_button)

        # Button to save the processed image
        self.save_button.clicked.connect(self.save_image)
        self.save_button.setEnabled(False)  # Initially disabled
        button_layout.addWidget(self.save_button)

        # Add button layout to the main layout
        main_layout.addLayout(button_layout)

        # Set the central widget with the main layout
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def load_image(self):
        """
        Opens a file dialog to load an image from the file system.
        Enables the 'Apply Effect' button if an image is successfully loaded.
        """
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_name:
            self.original_image = cv2.imread(file_name)
            if self.original_image is not None:
                self.display_image(self.original_image)
                self.apply_button.setEnabled(True)  # Enable the effect button

    def apply_effect(self):
        """
        Applies the selected effect to the loaded image.
        Enables the 'Save Image' button if processing is successful.
        """
        if self.original_image is not None:
            # Retrieve the selected effect from the dropdown
            effect = self.effect_combo.currentText()
            if effect == "Grayscale":
                self.processed_image = convert_to_grayscale(self.original_image)
            elif effect == "Sketch Effect":
                self.processed_image = apply_sketch_effect(self.original_image)
            elif effect == "Contour Effect":
                self.processed_image = apply_contour_effect(self.original_image)
            elif effect == "Tattoo Calc Effect":
                self.processed_image = apply_tattoo_calc_effect(self.original_image)

            # Display the processed image
            self.display_image(self.processed_image)
            self.save_button.setEnabled(True)  # Enable the save button

    def save_image(self):
        """
        Opens a file dialog to save the processed image to the file system.
        """
        if self.processed_image is not None:
            save_path, _ = QFileDialog.getSaveFileName(
                self, "Save Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)"
            )
            if save_path:
                cv2.imwrite(save_path, self.processed_image)

    def display_image(self, image):
        """
        Converts an OpenCV image to QPixmap and displays it in the QLabel widget.

        Args:
            image (np.ndarray): The image to display (OpenCV format).
        """
        if len(image.shape) == 2:  # Grayscale image
            height, width = image.shape
            q_image = QImage(image.data, width, height, width, QImage.Format_Grayscale8)
        else:  # Color image
            height, width, channel = image.shape
            bytes_per_line = channel * width
            q_image = QImage(
                image.data, width, height, bytes_per_line, QImage.Format_RGB888
            ).rgbSwapped()

        # Convert QImage to QPixmap and display it
        pixmap = QPixmap.fromImage(q_image)
        self.image_label.setPixmap(
            pixmap.scaled(
                self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageApp()
    window.show()
    sys.exit(app.exec_())
