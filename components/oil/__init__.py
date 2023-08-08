def update_oil_temp(self, value):
    self.oil_temp = int(value)
    self.repaint_oil_temp()

def Config(self):
    self.global_x = 280
    self.global_y = 50 
    ## Text in "TextHere", TextSize
    self.text_labels = "Nimbus Sans Bold", 8