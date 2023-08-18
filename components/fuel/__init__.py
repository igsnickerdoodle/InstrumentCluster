global_x = 280
global_y = 50 
text_labels = "Nimbus Sans Bold", 8


def update_fuel(self, value):
    self.fuel_level = int(value)
    self.repaint_fuel()