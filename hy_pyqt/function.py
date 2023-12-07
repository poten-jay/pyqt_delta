
from geometry_msgs.msg import Point


class xyz_button():
    def __init__(self, node, input_x, input_y, input_z):
        self.node = node
        self.input_x = input_x
        self.input_y = input_y
        self.input_z = input_z

    def publish_xyz(self):
        msg = Point()
        msg.x = float(self.input_x)
        msg.y = float(self.input_y)
        msg.z = float(self.input_z)
        self.node.publisher_xyz.publish(msg)

    def x_up(self):
        self.input_x += 10
        self.publish_xyz()
        # self.publish_xyz()
    
    def y_up(self):
        self.input_y += 10
        self.publish_xyz()

    def z_up(self):
        self.input_z += 10
        self.publish_xyz()

    def x_down(self):
        self.input_x -= 10
        self.publish_xyz()

    def y_down(self):
        self.input_y -= 10
        self.publish_xyz()

    def z_down(self):
        self.input_z -= 10
        self.publish_xyz()
    