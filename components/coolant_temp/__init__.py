def Config(self):
    global_x = 280
    global_y = 50 
    ## Text in "TextHere", TextSize
    self.text_labels = "Nimbus Sans Bold", 8

def update_coolant(self, value):
    self.coolant = int(value)
    self.repaint_coolant() 
