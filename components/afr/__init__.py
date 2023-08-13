global_x = 280
global_y = 50 
text_labels = "Nimbus Sans Bold", 8


def update_afr(self, value):
    self.afr_value = float(value) / 100
    self.repaint_afr()