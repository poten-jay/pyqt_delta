# import rclpy
# from rclpy.node import Node
# from geometry_msgs.msg import Point
# from std_msgs.msg import String

# class GUI_Node(Node):
#     def __init__(self):
#         super().__init__('gui_node')
#         # Publisher 생성
#         self.publisher_xyz = self.create_publisher(Point, 'input_xyz', 10)



# def main(args=None):
#     rclpy.init(args=args)
#     gui_node = GUI_Node()
#     exit_code = gui_node.app.exec_()
#     gui_node.destroy_node()
#     rclpy.shutdown()
#     sys.exit(exit_code)
# ####################################################

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point

class GUI_Node(Node):
    # print('gui_node')
    def __init__(self):
        super().__init__('gui_node')
        # Publisher 생성
        self.publisher_xyz = self.create_publisher(Point, 'input_xyz', 10)
        self.publisher_x = self.create_publisher(Point, 'input_x', 10)
        self.publisher_y = self.create_publisher(Point, 'input_y', 10)
        self.publisher_z = self.create_publisher(Point, 'input_z', 10)



    def publish_xyz(self, x, y, z):
        msg = Point()
        msg.x = x
        msg.y = y
        msg.z = z
        self.publisher_xyz.publish(msg)

    # def publish_x(self, x):
    #     # x = float(self.input_x)
    #     msg_x = Point()
    #     msg_x.x = x
    #     self.publisher_xyz.publish(msg_x)

    # def publish_y(self, y):
    #     # y = float(self.input_y)
    #     msg_y = Point()
    #     msg_y.y = y
    #     self.publisher_xyz.publish(msg_y)

    # def publish_z(self, z):
    #     # z = float(self.input_z)
    #     msg_z = Point()
    #     msg_z.z = z
    #     self.publisher_xyz.publish(msg_z)

def main():
    rclpy.init(args=None)
    gui_node = GUI_Node()
    rclpy.spin(gui_node)
    gui_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()