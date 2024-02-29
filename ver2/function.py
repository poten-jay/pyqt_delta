
from geometry_msgs.msg import Point
import setting


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


    def publish_x(self):
        x = float(self.input_x)
        msg_x = Point()
        msg_x.x = x
        self.node.publisher_xyz.publish(msg_x)

    def publish_y(self):
        y = float(self.input_y)
        msg_y = Point()
        msg_y.y = y
        self.node.publisher_xyz.publish(msg_y)

    def publish_z(self):
        z = float(self.input_z)
        msg_z = Point()
        msg_z.z = z
        self.node.publisher_xyz.publish(msg_z)



    def x_up(self):
        if self.input_x < setting.x_max:
            self.input_x += 10
            self.publish_xyz()
            # self.publish_xyz()
        else:
            print("Caution : The Limit of Max X")
    
    def y_up(self):
        if self.input_y < setting.y_max:
            self.input_y += 10
            self.publish_xyz()
        else:
            print("Caution : The Limit of Max Y")

    def z_up(self):
        if self.input_z < setting.z_max:
            self.input_z += 5
            self.publish_xyz()
        else:
            print("Caution : The Limit of Max Z")

    def x_down(self):
        if self.input_x > setting.x_min:
            self.input_x -= 10
            self.publish_xyz()
        else:
            print("Caution : The Limit of Min X")

    def y_down(self):
        if self.input_y > setting.y_min:
            self.input_y -= 10
            self.publish_xyz()
        else:
            print("Caution : The Limit of Min Y")

    def z_down(self):
        if self.input_z > setting.z_min:
            self.input_z -= 5
            self.publish_xyz()
        else:
            print("Caution : The Limit of Min Z")
    