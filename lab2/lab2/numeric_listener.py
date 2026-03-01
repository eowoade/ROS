import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Int8


class NumericListener(Node):
    def __init__(self):
        super().__init__('numeric_listener')
        self.subscription_string = self.create_subscription(String, 'chatter', self.listener_callback, 10)
        self.subscription_string  # prevent unused variable warning
        self.subscription_int = self.create_subscription(Int8, 'numeric_chatter', self.listener_callback, 10)
        self.subscription_int  # prevent unused variable warning
        

    def listener_callback(self, msg):
        self.get_logger().info(f'I heard: {msg.data!r}')


def main(args=None):
    rclpy.init(args=args)
    numeric_listener = NumericListener()
    rclpy.spin(numeric_listener)


if __name__ == '__main__':
    main()
