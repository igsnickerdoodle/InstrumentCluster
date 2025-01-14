import sys, os, json
from PyQt5.QtWidgets import ( 
    QApplication, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QSpinBox, QComboBox, QWidget, QCheckBox, QButtonGroup, QSlider 
    )
from PyQt5.QtCore import Qt

class Settings(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setGeometry(100, 100, 500, 500)
        self.setStyleSheet("background-color: grey")
        self.settings_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'cluster_settings.json'))
        self.settings = self.load_settings()

        # Color Definition Index for RPM Meter
        self.colors = [
            'rgb(255, 0, 0)',       # Red
            'rgb(0, 255, 0)',       # Green
            'rgb(0, 0, 255)',       # Blue
            'rgb(255, 255, 0)',     # Yellow
            'rgb(255, 192, 203)',   # Pink
            'rgb(255, 165, 0)',     # Orange
            'rgb(128, 0, 128)',     # Purple
            'rgb(165, 42, 42)',     # Brown
            'rgb(0, 0, 0)',         # Black
            'rgb(255, 255, 255)',   # White
            'rgb(128, 128, 128)',   # Grey
            'rgb(0, 255, 255)'      # Cyan
        ]
        self.colorDisplays = []
        self.current_color_indexes = [0, 0, 0]

        layout = QVBoxLayout()
        layout.setSpacing(10)  # Reduced the spacing between layouts
        layout.setContentsMargins(10, 10, 10, 10)  # Reduced the margins around the main layout

        # RPM settings
        layout.addLayout(self.setup_rpm_settings())
        # Redline settings
        layout.addLayout(self.setup_redline_settings())
        # Redline Color settings
        layout.addLayout(self.setup_redline_color_settings())

        # Boost Gauge / Max Boost Settings
        layout.addLayout(self.boost_active())
        self.max_boostWidget = self.set_max_boost() 
        layout.addWidget(self.max_boostWidget)  #
        self.max_boostWidget.setVisible(self.boostCheckBox.isChecked())  
        def max_boost_visibility(checked):
            self.max_boostWidget.setVisible(checked)
        self.boostCheckBox.stateChanged.connect(max_boost_visibility) 

        # Air Fuel Gauge Settings
        layout.addLayout(self.afr_active())
        # Design selection
        layout.addLayout(self.setup_design_selection())
        # Save / Close 
        layout.addLayout(self.setup_buttons())

        self.setLayout(layout)

    def setup_rpm_settings(self):
        rpmLayout = QHBoxLayout()
        rpmLayout.setSpacing(5)  # Reduce spacing between widgets in horizontal layout
        rpmLabel = QLabel("Max RPM:", self)
        rpmLayout.addWidget(rpmLabel)
        self.rpmSpinBox = QSpinBox(self)
        self.rpmSpinBox.setRange(5000, 12000)
        self.rpmSpinBox.setSingleStep(500)
        self.rpmSpinBox.setValue(5000)
        self.rpmSpinBox.setAlignment(Qt.AlignCenter)
        self.rpmSpinBox.setReadOnly(True)
        self.rpmSpinBox.setFocusPolicy(Qt.NoFocus)
        self.rpmSpinBox.setStyleSheet("QSpinBox::up-button, QSpinBox::down-button { width: 0; }")

        self.rpmleftButton = QPushButton('<', self)
        self.rpmleftButton.clicked.connect(lambda: self.rpmSpinBox.setValue(self.rpmSpinBox.value() - 500))
        self.rpmrightButton = QPushButton('>', self)
        self.rpmrightButton.clicked.connect(lambda: self.rpmSpinBox.setValue(self.rpmSpinBox.value() + 500))

        RpmbuttonWidth = 20
        self.rpmleftButton.setFixedWidth(RpmbuttonWidth)
        self.rpmrightButton.setFixedWidth(RpmbuttonWidth)

        rpmLayout.addWidget(self.rpmleftButton)
        rpmLayout.addWidget(self.rpmSpinBox)
        rpmLayout.addWidget(self.rpmrightButton)
        return rpmLayout

    def setup_redline_settings(self):
        redlineLayout = QHBoxLayout()
        redlineLayout.setSpacing(5)
        redlineLabel = QLabel("Red Line:", self)
        redlineLayout.addWidget(redlineLabel)
        self.redlineSpinBox = QSpinBox(self)
        self.redlineSpinBox.setRange(5000, 12000)
        self.redlineSpinBox.setSingleStep(500)
        self.redlineSpinBox.setValue(8000)
        self.redlineSpinBox.setAlignment(Qt.AlignCenter)
        self.redlineSpinBox.setReadOnly(True)
        self.redlineSpinBox.setFocusPolicy(Qt.NoFocus)
        self.redlineSpinBox.setStyleSheet("QSpinBox::up-button, QSpinBox::down-button { width: 0; }")

        self.redlineleftButton = QPushButton('<', self)
        self.redlineleftButton.clicked.connect(lambda: self.redlineSpinBox.setValue(self.redlineSpinBox.value() - 500))
        self.redlinerightButton = QPushButton('>', self)
        self.redlinerightButton.clicked.connect(lambda: self.redlineSpinBox.setValue(self.redlineSpinBox.value() + 500))

        RedlinebuttonWidth = 20
        self.redlineleftButton.setFixedWidth(RedlinebuttonWidth)
        self.redlinerightButton.setFixedWidth(RedlinebuttonWidth)

        redlineLayout.addWidget(self.redlineleftButton)
        redlineLayout.addWidget(self.redlineSpinBox)
        redlineLayout.addWidget(self.redlinerightButton)
        return redlineLayout

    def setup_redline_color_settings(self):
        self.redlineColorLayout = QHBoxLayout()

        # Integrated layout for label and checkboxes
        labelAndCheckboxes = QHBoxLayout()
        redlineColorLabel = QLabel("Redline Color:", self)
        labelAndCheckboxes.addWidget(redlineColorLabel)

        # Checkboxes for selecting the number of color boxes
        checkboxLayout = QVBoxLayout()
        self.checkBoxGroup = QButtonGroup(self)
        for i in range(3):
            checkBox = QCheckBox(str(i + 1), self)
            self.checkBoxGroup.addButton(checkBox, i)
            checkboxLayout.addWidget(checkBox)
            checkBox.toggled.connect(lambda checked, index=i: self.handle_checkbox(checked, index))
        labelAndCheckboxes.addLayout(checkboxLayout)

        self.redlineColorLayout.addLayout(labelAndCheckboxes)

        # Container for color displays
        self.colorContainer = QVBoxLayout()
        self.redlineColorLayout.addLayout(self.colorContainer)

        # Initialize with the first checkbox checked and display set up
        self.checkBoxGroup.buttons()[0].setChecked(True)  # This ensures the first checkbox is checked
        self.update_color_displays(1)  # Update the display with 1 color picker

        return self.redlineColorLayout
    
    def boost_active(self):
        boostLayout = QHBoxLayout()
        boostLayout.setSpacing(5)
        boostLabel = QLabel("Boost Gauge: ", self)
        boostLayout.addWidget(boostLabel)
        self.boostCheckBox = QCheckBox("Active", self)
        self.boostCheckBox.setChecked(False) 
        boostLayout.addWidget(self.boostCheckBox)
        return boostLayout

    def set_max_boost(self):
        # Create a QWidget to hold the layout
        self.max_boost_widget = QWidget(self)
        max_boost_layout = QHBoxLayout(self.max_boost_widget)
        self.max_boost_widget.setFixedHeight(45)  # Set a fixed height to reduce vertical space


        self.max_boost_slider = QSlider(Qt.Horizontal, self)
        self.max_boost_slider.setMinimum(5)
        self.max_boost_slider.setMaximum(40)
        self.max_boost_slider.setTickInterval(5)
        self.max_boost_slider.setTickPosition(QSlider.TicksBelow)
        self.max_boost_slider.setSingleStep(5) 
        self.max_boost_slider.setValue(5)
        # self.max_boost_slider.setFixedHeight(30)  # Reduce the height of the slider


        self.max_boost_label = QLabel(f"Max Boost:\n{self.max_boost_slider.value()} psi", self.max_boost_widget)
        self.max_boost_label.setAlignment(Qt.AlignCenter)
        max_boost_layout.addWidget(self.max_boost_label)
        
        def boost_label(value):
            self.max_boost_label.setText(f"Max Boost: \n{value} psi")
        
        self.max_boost_slider.valueChanged.connect(boost_label)
        max_boost_layout.addWidget(self.max_boost_slider)
        
        return self.max_boost_widget

    def afr_active(self):
        afrLayout = QHBoxLayout()
        afrLayout.setSpacing(5)
        afrLabel = QLabel("AFR Gauge: ", self)
        afrLayout.addWidget(afrLabel)
        self.afrCheckBox = QCheckBox("Active", self)
        self.afrCheckBox.setChecked(False) 
        afrLayout.addWidget(self.afrCheckBox)
        return afrLayout

    def setup_design_selection(self):
        designLayout = QHBoxLayout()
        designLayout.setSpacing(5)
        designLabel = QLabel("Select Design:", self)
        designLayout.addWidget(designLabel)
        self.designComboBox = QComboBox(self)
        self.populate_designs('designs')
        designLayout.addWidget(self.designComboBox)
        return designLayout

    def setup_buttons(self):
        buttonLayout = QHBoxLayout()
        buttonLayout.setSpacing(5)
        saveButton = QPushButton("Save", self)
        saveButton.clicked.connect(self.save_settings)
        buttonLayout.addWidget(saveButton)
        
        closeButton = QPushButton("Close", self)
        closeButton.clicked.connect(self.close)
        buttonLayout.addWidget(closeButton)
        return buttonLayout

    def save_settings(self):
        print("Settings saved!")

    def populate_designs(self, path):
        try:
            designs = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
            self.designComboBox.addItems(designs)
            if 'selected_design' in self.settings:
                index = self.designComboBox.findText(self.settings['selected_design'])
                if index != -1:
                    self.designComboBox.setCurrentIndex(index)
        except Exception as e:
            print("Failed to read designs from:", path, "Error:", str(e))

    def handle_checkbox(self, checked, index):
        if checked:
            self.update_color_displays(index + 1)

    def update_color_displays(self, count):
        # Clear existing color displays
        while self.colorContainer.count():
            item = self.colorContainer.takeAt(0)  # Take the layout item
            if item is not None:
                widget = item.widget()  # Get the widget from the layout item
                if widget:
                    widget.hide()  # Hide the widget
                    widget.deleteLater()  # Schedule the widget for deletion
                elif item.layout():  # Check if the layout item is a layout
                    sublayout = item.layout()
                    self.clear_layout(sublayout)  # Recursively clear the layout
                    sublayout.deleteLater()  # Delete the sublayout
        self.colorDisplays = []  # Reset the list to avoid indexing issues

        # Add new color displays for the number of selected
        for i in range(count):
            layout = self.create_color_display(i)
            self.colorContainer.addLayout(layout)

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.hide()
                widget.deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())
                item.layout().deleteLater()

    def create_color_display(self, index):
        layout = QHBoxLayout()
        label = QLabel(f"{index + 1}:", self)
        leftButton = QPushButton('<', self)
        leftButton.clicked.connect(lambda: self.change_color(index, -1))

        colorLabel = QLabel(self)
        colorLabel.setFixedWidth(100)
        colorLabel.setFixedHeight(20)
        colorLabel.setStyleSheet(f"background-color: {self.colors[self.current_color_indexes[index]]}")
        self.colorDisplays.append(colorLabel)  # Ensure the list matches the current display count

        rightButton = QPushButton('>', self)
        rightButton.clicked.connect(lambda: self.change_color(index, 1))

        layout.addWidget(label)
        layout.addWidget(leftButton)
        layout.addWidget(colorLabel)
        layout.addWidget(rightButton)

        return layout

    def change_color(self, index, delta):
        self.current_color_indexes[index] = (self.current_color_indexes[index] + delta) % len(self.colors)
        self.colorDisplays[index].setStyleSheet(f"background-color: {self.colors[self.current_color_indexes[index]]}")

    def save_settings(self):
        self.settings['max_rpm'] = self.rpmSpinBox.value()
        self.settings['redline_rpm'] = self.redlineSpinBox.value()
        self.settings['boost_active'] = self.boostCheckBox.isChecked()
        self.settings['max_boost'] = self.max_boost_slider.value()
        self.settings['afr_active'] = self.afrCheckBox.isChecked()
        self.settings['current_color_indexes'] = self.current_color_indexes
        self.settings['redline_color_count'] = sum(1 for btn in self.checkBoxGroup.buttons() if btn.isChecked())
        self.settings['selected_design'] = self.designComboBox.currentText() 
        with open(self.settings_file, 'w') as file:
            json.dump(self.settings, file, indent=4)
        print("Settings saved!")

    def load_settings(self):
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as file:
                    settings = json.load(file)
            except json.JSONDecodeError:
                settings = self.default_settings()
        else:
            settings = self.default_settings()

        # Load designs into the designComboBox
        if 'designs' in settings:
            self.designComboBox.clear()
            self.designComboBox.addItems(settings['designs'])

        return settings

    def default_settings(self):
        return {
            'max_rpm': 8000,
            'redline_rpm': 6400,
            'boost_active': False,
            'max_boost': 5,
            'afr_active': False,
            'current_color_indexes': [0, 0, 0],
            'redline_color_count': 1,
            'designs': []
        }

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = Settings()
    dialog.show()
    sys.exit(app.exec_())
