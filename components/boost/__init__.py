import importlib, json, sys
from pathlib import Path

root_directory = Path(__file__).resolve().parent
if str(root_directory) not in sys.path:
    sys.path.insert(0, str(root_directory))

global_x = 280
global_y = 50 
text_labels = "Nimbus Sans Bold", 8

def load_cluster_settings(self):
    with open('cluster_settings.json', 'r') as file:
        settings = json.load(file)
    max_boost = settings.get("max_boost")
    if max_boost:
        max_boost = importlib.import_module(f'{max_boost}')
        self.display = max_boost()

def update_boost(self, value):
    self.boost_value = int(value)
    self.repaint_boost()
