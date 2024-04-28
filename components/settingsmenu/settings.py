import sys
import os
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSpinBox, QComboBox
from PyQt5.QtCore import Qt
class Settings(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setGeometry(100, 100, 300, 300)
        self.setStyleSheet("background-color: grey")

        layout = QVBoxLayout()
        
        # RPM settings
        rpmLayout = QHBoxLayout()
        rpmLabel = QLabel("Max RPM:", self)

        rpmLayout.addWidget(rpmLabel)
        self.rpmSpinBox = QSpinBox(self)
        self.rpmSpinBox.setRange(5000, 12000)
        self.rpmSpinBox.setSingleStep(500)
        self.rpmSpinBox.setValue(5000)  # Minimum RPM Value
        self.rpmSpinBox.setAlignment(Qt.AlignCenter)
        self.rpmSpinBox.setReadOnly(True)
        self.rpmSpinBox.setFocusPolicy(Qt.NoFocus)
        self.rpmSpinBox.setStyleSheet("QSpinBox::up-button, QSpinBox::down-button { width: 0; }")

        self.leftButton = QPushButton('<', self)
        self.leftButton.clicked.connect(lambda: self.rpmSpinBox.setValue(self.rpmSpinBox.value() - 500))
        self.rightButton = QPushButton('>', self)
        self.rightButton.clicked.connect(lambda: self.rpmSpinBox.setValue(self.rpmSpinBox.value() + 500))

        RpmbuttonWidth = 30
        self.leftButton.setFixedWidth(RpmbuttonWidth)
        self.rightButton.setFixedWidth(RpmbuttonWidth)

        rpmLayout.addWidget(self.leftButton)
        rpmLayout.addWidget(self.rpmSpinBox)
        rpmLayout.addWidget(self.rightButton)
        layout.addLayout(rpmLayout)
        
        # Design selection
        designLayout = QHBoxLayout()
        designLabel = QLabel("Select Design:", self)
        designLayout.addWidget(designLabel)

        self.designComboBox = QComboBox(self)
        self.populate_designs('designs')
        designLayout.addWidget(self.designComboBox)

        layout.addLayout(designLayout)
        
        # Buttons
        buttonLayout = QHBoxLayout()
        saveButton = QPushButton("Save", self)
        saveButton.clicked.connect(self.save_settings)
        buttonLayout.addWidget(saveButton)
        
        closeButton = QPushButton("Close", self)
        closeButton.clicked.connect(self.close)
        buttonLayout.addWidget(closeButton)

        layout.addLayout(buttonLayout)
        
        self.setLayout(layout)
    
    def save_settings(self):
        print("Settings saved! Max RPM:", self.rpmSpinBox.value())
        print("Selected design:", self.designComboBox.currentText())

    def populate_designs(self, path):
        try:
            designs = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
            self.designComboBox.addItems(designs)
        except Exception as e:
            print("Failed to read designs from:", path, "Error:", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = Settings()
    dialog.show()
    sys.exit(app.exec_())
