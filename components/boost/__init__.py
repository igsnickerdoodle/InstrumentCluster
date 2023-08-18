global_x = 280
global_y = 50 
text_labels = "Nimbus Sans Bold", 8

def update_boost(self, value):
    self.boost_value = int(value)
    self.repaint_boost()
