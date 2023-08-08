def update_afr(self, value):
    self.afr_value = float(value) / 100
    self.repaint_afr()

def config(self):
    self.global_x = 280
    self.global_y = 50 
    ## Text in "TextHere", TextSize
    self.text_labels = "Nimbus Sans Bold", 8