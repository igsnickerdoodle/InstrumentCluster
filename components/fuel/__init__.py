def update_fuel(self, value):
    self.fuel_level = int(value)
    self.repaint_fuel()

def Config(self):
    self.global_x = 280
    self.global_y = 50 
    ## Text in "TextHere", TextSize
    self.text_labels = "Nimbus Sans Bold", 8