global_x = 280
global_y = 50 
text_labels = "Nimbus Sans Bold", 8


def update_coolant(self, value):
    self.coolant = int(value)
    self.repaint_coolant() 
