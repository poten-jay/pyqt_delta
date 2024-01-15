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
    def __init__(self):
        super().__init__('gui_node')
        # Publisher 생성
        self.publisher_xyz = self.create_publisher(Point, 'input_xyz', 10)

    def publish_xyz(self, x, y, z):
        msg = Point()
        msg.x = x
        msg.y = y
        msg.z = z
        self.publisher_xyz.publish(msg)

def main():
    rclpy.init(args=None)
    gui_node = GUI_Node()
    rclpy.spin(gui_node)
    gui_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()