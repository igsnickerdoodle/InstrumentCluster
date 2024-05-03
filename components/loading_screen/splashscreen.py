import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QGraphicsOpacityEffect
from PyQt5.QtCore import Qt, QPropertyAnimation
from PyQt5.QtGui import QPixmap

class LoadingScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.setGeometry(600, 600, 700, 600)
        self.setStyleSheet("""
        QWidget {
            background-color: transparent;
        }
        QLabel {
            background-color: transparent;
        }
        """)

    def initUI(self):
        # Create a label to hold the image
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        # self.label.setGeometry(50, 50, 200, 100)  # Adjust size and position as needed

        # Load an image into the label
        self.label.setPixmap(QPixmap(r"C:\Users\justc\github\InstrumentCluster\resources\mazda.png").scaled(405, 291, Qt.KeepAspectRatio))

        # Set up opacity effect
        self.opacity_effect = QGraphicsOpacityEffect(self.label)
        self.label.setGraphicsEffect(self.opacity_effect)

        # Set up the fade animation on the opacity effect
        self.anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.anim.setDuration(3000)  # Duration in milliseconds (5000 ms = 5 seconds)
        self.anim.setStartValue(0)  # Start fully transparent
        self.anim.setEndValue(1)  # End fully opaque
        self.anim.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = LoadingScreen()
    demo.setStyleSheet("background-color: black;")
    demo.show()
    sys.exit(app.exec_())
