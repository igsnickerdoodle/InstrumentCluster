global_x = 280
global_y = 50 
text_labels = "Nimbus Sans Bold", 8

max_rpm_value = 8000

def update_rpm(self, value):
    self.rpm = int(value)
    self.repaint_rpm()
