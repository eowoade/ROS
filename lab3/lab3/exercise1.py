import threading
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from rclpy.exceptions import ROSInterruptException
import signal

class SecondWalker(Node):
    def __init__(self):
        super().__init__('secondwalker')
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.rate = self.create_rate(10)  # 10 Hz

    def circle_walk(self):
        desired_velocity = Twist()
        desired_velocity.linear.x = 0.2  # Forward with 0.2 m/s
        desired_velocity.angular.z = 0.5
        self.publisher.publish(desired_velocity)

    def stop(self):
        desired_velocity = Twist()
        desired_velocity.linear.x = 0.0  # Send zero velocity to stop the robot
        self.publisher.publish(desired_velocity)
        
def main():
    def signal_handler(sig, frame):
        second_walker.stop()
        rclpy.shutdown()

    rclpy.init(args=None)
    second_walker = SecondWalker()

    signal.signal(signal.SIGINT, signal_handler)
    thread = threading.Thread(target=rclpy.spin, args=(second_walker,), daemon=True)
    thread.start()

    try:
        while rclpy.ok():
            second_walker.circle_walk()
            second_walker.rate.sleep()
    except ROSInterruptException:
        pass


if __name__ == "__main__":
    main()