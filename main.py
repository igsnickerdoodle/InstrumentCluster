import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout
from PyQt5.QtGui import QPalette, QColor, QCursor
from PyQt5.QtCore import Qt, QObject
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import json
import importlib

# Ensure the root directory is in the system path
root_directory = Path(__file__).resolve().parent
if str(root_directory) not in sys.path:
    sys.path.insert(0, str(root_directory))

# Import your settings and other components here
from components.settingsmenu.settings import Settings

class SettingsChangeHandler(QObject, FileSystemEventHandler):
    def __init__(self, window):
        super().__init__()
        self.window = window

    def on_modified(self, event):
        if "cluster_settings.json" in event.src_path:
            print(f"Configuration change detected in {event.src_path}, reloading application")
            self.window.restart_application()

class MainWindow(QMainWindow):
    restart_code = 1000
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        print("Application is initializing...")
        self.setGeometry(0, 0, 1024, 600)
        self.settings_window = Settings()
        self.settings_window.setGeometry(0, 0, 1024, 600)
        self.settings_window.hide()

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QGridLayout(self.central_widget)

        palette = QPalette()
        palette.setColor(QPalette.Background, QColor('black'))
        self.central_widget.setPalette(palette)

        self.load_cluster_settings()
        self.start_watching_settings()

    def load_cluster_settings(self):
        try:
            with open('cluster_settings.json', 'r') as file:
                settings = json.load(file)
            selected_design = settings.get("selected_design")
            if selected_design:
                design_module = importlib.import_module(f'designs.{selected_design}.app')
                self.display = design_module.instrumentcluster()
                self.layout.addWidget(self.display, 0, 0)
                self.display.show()
        except Exception as e:
            print("Failed to load settings or design:", e)

    def start_watching_settings(self):
        event_handler = SettingsChangeHandler(self)
        self.observer = Observer()
        self.observer.schedule(event_handler, path='.', recursive=False)
        self.observer.start()

    def restart_application(self):
        QApplication.exit(MainWindow.restart_code)

    def closeEvent(self, event):
        self.observer.stop()
        self.observer.join()
        super().closeEvent(event)

if __name__ == "__main__":
    exit_code = MainWindow.restart_code
    while exit_code == MainWindow.restart_code:
        app = QApplication(sys.argv) 
        palette = QPalette()
        palette.setColor(QPalette.Window, Qt.black)
        app.setPalette(palette)
        QApplication.setOverrideCursor(QCursor(Qt.BlankCursor))
        mainWindow = MainWindow()
        mainWindow.show()
        exit_code = app.exec_()
        app = None
