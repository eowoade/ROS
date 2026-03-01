import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Int8


class   NumericTalker(Node):
    def __init__(self):
        super().__init__('numeric_talker')
        self.publisher_string = self.create_publisher(String, 'chatter', 10)
        self.publisher_int = self.create_publisher(Int8, 'numeric_chatter', 10)

        timer_in_seconds = 0.5
        self.timer = self.create_timer(timer_in_seconds, self.talker_callback)
        self.counter = 0

    def talker_callback(self):
        msg = String()
        msg.data = f'Hello World, {self.counter}'
        self.publisher_string.publish(msg)
        self.get_logger().info(f'Publishing String: {msg.data}')
        
        msg_int = Int8()
        msg_int.data = self.counter
        self.publisher_int.publish(msg_int)
        self.get_logger().info(f'Publishing Integer: {msg_int.data}')
        
        if self.counter >= 127:
            self.counter = 0
        else:
            self.counter += 1


def main(args=None):
    rclpy.init(args=args)

    numeric_talker = NumericTalker()
    rclpy.spin(numeric_talker)


if __name__ == '__main__':
    main()


