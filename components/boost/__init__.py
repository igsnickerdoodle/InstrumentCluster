def update_boost(self, value):
    self.boost_value = int(value)
    self.repaint_boost()

def config(self):
    self.global_x = 280
    self.global_y = 50 
    ## Text in "TextHere", TextSize
    self.text_labels = "Nimbus Sans Bold", 8