import threading
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from rclpy.exceptions import ROSInterruptException
import signal
import time

class ThirdWalker(Node):
    def __init__(self):
        super().__init__('thirdwalker')
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.rate = self.create_rate(10)  # 10 Hz

    def square_walk(self, linear_speed, angular_speed, duration):
        desired_velocity = Twist()
        desired_velocity.linear.x = linear_speed
        desired_velocity.angular.z = angular_speed
        
        for i in range(duration):
            if not rclpy.ok():
                break
            self.publisher.publish(desired_velocity)
            self.rate.sleep()

    def stop(self):
        desired_velocity = Twist()
        self.publisher.publish(desired_velocity)
        time.sleep(1)
        
def main():
    def signal_handler(sig, frame):
        third_walker.stop()
        rclpy.shutdown()

    rclpy.init(args=None)
    third_walker = ThirdWalker()

    signal.signal(signal.SIGINT, signal_handler)
    thread = threading.Thread(target=rclpy.spin, args=(third_walker,), daemon=True)
    thread.start()

    try:
        while rclpy.ok():
            for i in range(4):
                third_walker.square_walk(0.2, 0.0, 30)
                third_walker.stop()
                third_walker.square_walk(0.0, 0.5, 34)
                third_walker.stop()
    except ROSInterruptException:
        pass


if __name__ == "__main__":
    main()