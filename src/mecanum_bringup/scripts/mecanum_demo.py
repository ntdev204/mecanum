#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time


class MecanumDemo(Node):
    def __init__(self):
        super().__init__('mecanum_demo')
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.get_logger().info('Mecanum Demo Node started')
        
    def send_velocity(self, linear_x=0.0, linear_y=0.0, angular_z=0.0, duration=2.0):
        """Gửi lệnh velocity trong thời gian xác định"""
        twist = Twist()
        twist.linear.x = linear_x
        twist.linear.y = linear_y
        twist.angular.z = angular_z
        
        end_time = time.time() + duration
        while time.time() < end_time:
            self.cmd_vel_pub.publish(twist)
            time.sleep(0.1)
            
        # Stop
        twist = Twist()
        self.cmd_vel_pub.publish(twist)
        time.sleep(0.5)
        
    def run_demo(self):
        """Chạy demo các chuyển động"""
        speed = 0.5
        
        self.get_logger().info('Starting Mecanum 10-Direction Movement Demo')
        time.sleep(2)
        
        # 1. Forward (w)
        self.get_logger().info('1. Moving Forward (w)')
        self.send_velocity(linear_x=speed)
        
        # 2. Backward (x)
        self.get_logger().info('2. Moving Backward (x)')
        self.send_velocity(linear_x=-speed)
        
        # 3. Strafe Left (a)
        self.get_logger().info('3. Strafing Left (a)')
        self.send_velocity(linear_y=speed)
        
        # 4. Strafe Right (d)
        self.get_logger().info('4. Strafing Right (d)')
        self.send_velocity(linear_y=-speed)
        
        # 5. Forward-Left Diagonal (q)
        self.get_logger().info('5. Moving Forward-Left Diagonal (q)')
        self.send_velocity(linear_x=speed*0.7, linear_y=speed*0.7)
        
        # 6. Forward-Right Diagonal (e)
        self.get_logger().info('6. Moving Forward-Right Diagonal (e)')
        self.send_velocity(linear_x=speed*0.7, linear_y=-speed*0.7)
        
        # 7. Backward-Left Diagonal (z)
        self.get_logger().info('7. Moving Backward-Left Diagonal (z)')
        self.send_velocity(linear_x=-speed*0.7, linear_y=speed*0.7)
        
        # 8. Backward-Right Diagonal (c)
        self.get_logger().info('8. Moving Backward-Right Diagonal (c)')
        self.send_velocity(linear_x=-speed*0.7, linear_y=-speed*0.7)
        
        # 9. Rotate Left (u)
        self.get_logger().info('9. Rotating Left (u)')
        self.send_velocity(angular_z=1.0)
        
        # 10. Rotate Right (i)
        self.get_logger().info('10. Rotating Right (i)')
        self.send_velocity(angular_z=-1.0)
        
        self.get_logger().info('10-Direction Demo completed!')


def main():
    rclpy.init()
    
    demo = MecanumDemo()
    
    try:
        demo.run_demo()
    except KeyboardInterrupt:
        demo.get_logger().info('Demo interrupted')
    
    demo.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
