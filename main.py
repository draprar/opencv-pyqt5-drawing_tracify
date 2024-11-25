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
)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from image_processor import convert_to_grayscale


class ImageApp(QMainWindow):
    def __init__(self):
        """
        Initializes the main application window and UI components.
        """
        super().__init__()
        self.original_image = None
        self.grayscale_button = None
        self.load_button = None
        self.image_label = None
        self.init_ui()

    def init_ui(self):
        """
        Sets up the user interface, including buttons and labels.
        """
        self.setWindowTitle("Image Processor")
        self.setGeometry(100, 100, 800, 600)

        # Layout setup
        main_layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        # Image display label
        self.image_label = QLabel("No Image Loaded")
        self.image_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.image_label)

        # Buttons
        self.load_button = QPushButton("Load Image")
        self.load_button.clicked.connect(self.load_image)
        button_layout.addWidget(self.load_button)

        self.grayscale_button = QPushButton("Convert to Grayscale")
        self.grayscale_button.clicked.connect(self.apply_grayscale)
        self.grayscale_button.setEnabled(False)  # Disabled initially
        button_layout.addWidget(self.grayscale_button)

        # Add button layout to the main layout
        main_layout.addLayout(button_layout)

        # Set the central widget
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Internal attributes
        self.original_image = None

    def load_image(self):
        """
        Loads an image from the file system and displays it in the application.

        Opens a file dialog to choose an image file.
        """
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_name:
            self.original_image = cv2.imread(file_name)
            if self.original_image is not None:
                self.display_image(self.original_image)
                self.grayscale_button.setEnabled(True)

    def apply_grayscale(self):
        """
        Applies the grayscale effect to the loaded image and displays the result.
        """
        if self.original_image is not None:
            grayscale_image = convert_to_grayscale(self.original_image)
            self.display_image(grayscale_image)

    def display_image(self, image):
        """
        Displays an image in the QLabel widget.

        Args:
            image (np.ndarray): The image to be displayed (OpenCV format).
        """
        if len(image.shape) == 2:  # Grayscale image
            height, width = image.shape
            q_image = QImage(
                image.data, width, height, width, QImage.Format_Grayscale8
            )
        else:  # Color image
            height, width, channel = image.shape
            bytes_per_line = channel * width
            q_image = QImage(
                image.data, width, height, bytes_per_line, QImage.Format_RGB888
            ).rgbSwapped()

        pixmap = QPixmap.fromImage(q_image)
        self.image_label.setPixmap(
            pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageApp()
    window.show()
    sys.exit(app.exec_())
