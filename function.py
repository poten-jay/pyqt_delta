class xyz_button():
    def __init__(self, input_x, input_y, input_z):
        self.input_x = input_x
        self.input_y = input_y
        self.input_z = input_z

    def x_up(self):
        self.input_x += 1
    
    def y_up(self):
        self.input_y += 1

    def z_up(self):
        self.input_z += 1

    def x_down(self):
        self.input_x -= 1

    def y_down(self):
        self.input_y -= 1

    def z_down(self):
        self.input_z -= 1
    