global_x = 280
global_y = 50 
text_labels = "Nimbus Sans Bold", 8

def update_oil_temp(self, value):
    self.oil_temp = int(value)
    self.repaint_oil_temp()
