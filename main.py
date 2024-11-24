import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QVBoxLayout, QWidget, QComboBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)


class PhotoToDrawingProcessor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Photo to Drawing Processor")
        self.setGeometry(100, 100, 800, 600)

        # Main container
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Widgets
        self.image_label = QLabel("Load an image to start processing")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.image_label)

        self.effect_combo = QComboBox()
        self.effect_combo.addItems(["Select Effect", "Grayscale", "Edge Detection"])
        self.layout.addWidget(self.effect_combo)

        self.load_button = QPushButton("Load Image")
        self.load_button.clicked.connect(self.load_image)
        self.layout.addWidget(self.load_button)

        self.apply_button = QPushButton("Apply Effect")
        self.apply_button.clicked.connect(self.apply_effect)
        self.layout.addWidget(self.apply_button)

        # Image data
        self.loaded_image = None
        self.processed_image = None

    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
        if file_path:
            logging.info(f"Image loaded: {file_path}")
            self.loaded_image = cv2.imread(file_path)
            self.display_image(self.loaded_image)

    def apply_effect(self):
        if self.loaded_image is None:
            logging.warning("No image loaded to apply effect.")
            self.image_label.setText("Please load an image first!")
            return

        selected_effect = self.effect_combo.currentText()
        if selected_effect == "Select Effect":
            logging.warning("No effect selected.")
            self.image_label.setText("Please select an effect!")
            return

        try:
            logging.info(f"Applying effect: {selected_effect}")
            if selected_effect == "Grayscale":
                self.processed_image = self.to_grayscale(self.loaded_image)
            elif selected_effect == "Edge Detection":
                self.processed_image = self.edge_detection(self.loaded_image)

            self.display_image(self.processed_image)
            logging.info("Effect applied successfully.")

        except Exception as e:
            logging.error(f"Error while applying effect: {e}")
            self.image_label.setText("Error applying effect. Check logs.")

    def to_grayscale(self, image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def edge_detection(self, image):
        gray = self.to_grayscale(image)
        return cv2.Canny(gray, 100, 200)

    def display_image(self, image):
        try:
            if len(image.shape) == 2:  # Grayscale
                height, width = image.shape
                q_image = QImage(image.data, width, height, QImage.Format_Grayscale8)
            else:  # Color
                height, width, channels = image.shape
                bytes_per_line = channels * width
                q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_BGR888)

            pixmap = QPixmap.fromImage(q_image)
            self.image_label.setPixmap(pixmap.scaled(self.image_label.width(), self.image_label.height(), Qt.KeepAspectRatio))

        except Exception as e:
            logging.error(f"Error displaying image: {e}")
            self.image_label.setText("Failed to display image. Check logs.")


# Main execution
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = PhotoToDrawingProcessor()
    main_window.show()
    sys.exit(app.exec_())
