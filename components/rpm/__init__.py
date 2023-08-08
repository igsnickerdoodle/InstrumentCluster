def update_rpm(self, value):
    self.rpm = int(value)
    self.repaint_rpm()

def Config(self):
    self.global_x = 280
    self.global_y = 50 
    ## Text in "TextHere", TextSize
    self.text_labels = "Nimbus Sans Bold", 8