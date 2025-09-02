#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy


class MecanumJoyTeleop(Node):
    def __init__(self):
        super().__init__('mecanum_joy_teleop')
        
        # Publisher cho cmd_vel
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        
        # Subscriber cho joy messages
        self.joy_sub = self.create_subscription(
            Joy,
            '/joy',
            self.joy_callback,
            10
        )
        
        # Thông số điều khiển
        self.max_linear_speed = 1.0  # m/s
        self.max_angular_speed = 2.0  # rad/s
        
        # Joystick button/axis mapping (Xbox controller layout)
        self.axis_linear_x = 1    # Left stick vertical
        self.axis_linear_y = 0    # Left stick horizontal  
        self.axis_angular = 2     # Right stick horizontal
        self.button_enable = 4    # Left bumper (LB)
        self.button_turbo = 5     # Right bumper (RB)
        
        self.get_logger().info('Mecanum Joy Teleop Node started')
        self.get_logger().info('Controls:')
        self.get_logger().info('  Left stick: Linear movement (X/Y)')
        self.get_logger().info('  Right stick horizontal: Angular rotation')
        self.get_logger().info('  Left bumper (LB): Enable movement')
        self.get_logger().info('  Right bumper (RB): Turbo mode')
        
    def joy_callback(self, msg):
        """Callback xử lý Joy messages"""
        try:
            twist = Twist()
            
            # Kiểm tra enable button
            if len(msg.buttons) <= self.button_enable or not msg.buttons[self.button_enable]:
                # Nếu không nhấn enable button, dừng robot
                self.cmd_vel_pub.publish(twist)
                return
            
            # Đọc các axis values
            if len(msg.axes) > max(self.axis_linear_x, self.axis_linear_y, self.axis_angular):
                linear_x = msg.axes[self.axis_linear_x]
                linear_y = msg.axes[self.axis_linear_y] 
                angular_z = msg.axes[self.axis_angular]
                
                # Kiểm tra turbo mode
                turbo_multiplier = 1.0
                if len(msg.buttons) > self.button_turbo and msg.buttons[self.button_turbo]:
                    turbo_multiplier = 2.0
                
                # Tính toán velocities
                twist.linear.x = linear_x * self.max_linear_speed * turbo_multiplier
                twist.linear.y = linear_y * self.max_linear_speed * turbo_multiplier
                twist.angular.z = angular_z * self.max_angular_speed * turbo_multiplier
                
                # Limit max speeds
                max_linear = self.max_linear_speed * turbo_multiplier
                max_angular = self.max_angular_speed * turbo_multiplier
                
                if abs(twist.linear.x) > max_linear:
                    twist.linear.x = max_linear if twist.linear.x > 0 else -max_linear
                if abs(twist.linear.y) > max_linear:
                    twist.linear.y = max_linear if twist.linear.y > 0 else -max_linear
                if abs(twist.angular.z) > max_angular:
                    twist.angular.z = max_angular if twist.angular.z > 0 else -max_angular
            
            # Publish twist message
            self.cmd_vel_pub.publish(twist)
            
        except Exception as e:
            self.get_logger().error(f'Error processing joy message: {e}')


def main(args=None):
    rclpy.init(args=args)
    
    try:
        joy_teleop = MecanumJoyTeleop()
        rclpy.spin(joy_teleop)
    except KeyboardInterrupt:
        pass
    finally:
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
