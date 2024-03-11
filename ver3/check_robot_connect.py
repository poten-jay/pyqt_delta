import json
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from wimt_msg.msg import TrackerArray  

class JointStateSubscriber(Node):
    def __init__(self):
        super().__init__('joint_state_subscriber')
        self.robot_status = False
        self.vision_status = False
        self.subscription_joint_states = self.create_subscription(
            JointState,
            'joint_states',
            self.joint_state_callback,
            10)
        self.subscription_tracked_objects = self.create_subscription(
            TrackerArray,  # /tracked_objects 토픽의 메시지 타입
            'tracked_objects',
            self.tracked_objects_callback,
            10)
        self.last_msg_time_joint_states = self.get_clock().now()
        self.last_msg_time_tracked_objects = self.get_clock().now()
        self.timeout_sec = 3  # Set the timeout duration in seconds
        self.create_timer(1, self.check_timeout)  # Check every second

    def joint_state_callback(self, msg):
        self.last_msg_time_joint_states = self.get_clock().now()
        self.robot_status = not(0.0 in msg.position)

    def tracked_objects_callback(self, msg):
        self.last_msg_time_tracked_objects = self.get_clock().now()
        self.vision_status = True  # /tracked_objects 메시지를 받으면 vision을 True로 설정

    def check_timeout(self):
        # Check timeout for joint_states
        if (self.get_clock().now() - self.last_msg_time_joint_states).nanoseconds / 1e9 > self.timeout_sec:
            self.robot_status = False
        # Check timeout for tracked_objects
        if (self.get_clock().now() - self.last_msg_time_tracked_objects).nanoseconds / 1e9 > self.timeout_sec:
            self.vision_status = False
        # 상태 업데이트 후 io.json 파일 업데이트
        self.update_io_file()

    def update_io_file(self):
        print("updating")
        io_data = {"robot": self.robot_status, "conveyor": False, "vision": self.vision_status, "encoder": False}
        with open('./document/io.json', 'w') as outfile:
            json.dump(io_data, outfile, indent=4)
        print(f"Updated robot to {self.robot_status}")
        print(f"Updated vistion to {self.vision_status}")

def main(args=None):
    rclpy.init(args=args)
    joint_state_subscriber = JointStateSubscriber()
    rclpy.spin(joint_state_subscriber)

    joint_state_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
