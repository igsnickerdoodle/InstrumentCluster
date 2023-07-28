
from PyQt5.QtCore import Qt, QPropertyAnimation, pyqtSignal
from PyQt5.QtWidgets import QSplashScreen, QProgressBar, QVBoxLayout, QLabel, QWidget, QGraphicsOpacityEffect
from PyQt5.QtGui import QPixmap, QPainter

class SplashScreen(QSplashScreen):
    finished = pyqtSignal()
    
    def __init__(self):
        super().__init__()

        # Set splash screen size
        self.setGeometry(0, 0, 680, 420)

        # Load image and set as background
        self.pixmap = QPixmap('resources/bmw_splash.jpg').scaled(self.size(), Qt.KeepAspectRatioByExpanding)
        self.setPixmap(self.pixmap)

        # Create a progress bar
        self.progress = QProgressBar()
        self.progress.setStyleSheet("""
            QProgressBar {
                border: none;
                text-align: center;
                color: white;
                font: 15pt "Impact";
                background: transparent;
            }
            QProgressBar::chunk {
                background-color: #81C4FFFF;
            }
        """)

        # Create a label
        self.label = QLabel("Initializing systems... Please wait...")
        self.label.setStyleSheet("""
            QLabel {
                color: white;
                font: 15pt "Impact";
            }
        """)

        # Create an opacity effect for the label
        self.opacity_effect = QGraphicsOpacityEffect(self.label)
        self.label.setGraphicsEffect(self.opacity_effect)

        # Create an animation to change the opacity
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.setDuration(1000)
        self.animation.setLoopCount(-1)  # Loop indefinitely
        self.animation.start()

        # Create a vertical layout
        layout = QVBoxLayout()
        layout.addWidget(self.label, alignment=Qt.AlignHCenter)
        layout.addWidget(self.progress, alignment=Qt.AlignHCenter)

        # Create a widget to hold the label and progress bar
        widget = QWidget()
        widget.setLayout(layout)

        # Create a main layout and add the widget to it
        main_layout = QVBoxLayout()
        main_layout.addWidget(widget, alignment=Qt.AlignBottom | Qt.AlignHCenter)

        # Set the layout to the splash screen
        self.setLayout(main_layout)

    def set_progress(self, progress):
        self.progress.setValue(progress)
        if progress >= 100:
            self.finish()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.pixmap)
    
    def finish(self):
        self.finished.emit()