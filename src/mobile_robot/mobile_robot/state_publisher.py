import rclpy
from rclpy.node import Node

from sensor_msgs.msg import JointState
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster


class StatePublisher(Node):

    def __init__(self):
        super().__init__('state_publisher')

        self.joint_pub = self.create_publisher(
            JointState,
            'joint_states',
            10
        )

        self.broadcaster = TransformBroadcaster(self)

        self.timer = self.create_timer(
            0.03,
            self.publish_state
        )

        self.position = 0.0

        self.get_logger().info("state_publisher started")

    def publish_state(self):
        now = self.get_clock().now()

        joint_state = JointState()
        joint_state.header.stamp = now.to_msg()

        joint_state.name = [
            'front_left_wheel_joint',
            'front_right_wheel_joint',
            'rear_left_wheel_joint',
            'rear_right_wheel_joint'
        ]

        self.position += 0.05

        joint_state.position = [
            self.position,
            self.position,
            self.position,
            self.position
        ]

        self.joint_pub.publish(joint_state)

        t = TransformStamped()

        t.header.stamp = now.to_msg()
        t.header.frame_id = 'odom'
        t.child_frame_id = 'chassis'

        t.transform.translation.x = 0.0
        t.transform.translation.y = 0.0
        t.transform.translation.z = 0.0

        t.transform.rotation.x = 0.0
        t.transform.rotation.y = 0.0
        t.transform.rotation.z = 0.0
        t.transform.rotation.w = 1.0

        self.broadcaster.sendTransform(t)


def main(args=None):
    rclpy.init(args=args)

    node = StatePublisher()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()