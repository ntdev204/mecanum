#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import sys
import select
import termios
import tty


class MecanumTeleop(Node):
    def __init__(self):
        super().__init__('mecanum_teleop')
        
        # Publisher cho cmd_vel
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        
        # Các thông số điều khiển
        self.linear_speed = 0.5  # m/s
        self.angular_speed = 1.0  # rad/s
        self.speed_increment = 0.1
        
        # Lưu trạng thái terminal
        self.settings = termios.tcgetattr(sys.stdin)
        
        self.get_logger().info('Mecanum Teleop Node started')
        self.print_instructions()
        
    def print_instructions(self):
        """In hướng dẫn sử dụng"""
        print("\n" + "="*50)
        print("MECANUM ROBOT KEYBOARD CONTROL")
        print("="*50)
        print("Moving around:")
        print("   q    w    e    u    i")
        print("   a    s    d")
        print("   z    x    c")
        print("")
        print("Movement controls:")
        print("w/x : forward/backward")
        print("a/d : strafe left/right")
        print("q/e : forward-left/right diagonal")
        print("z/c : backward-left/right diagonal")
        print("u/i : rotate left/right")
        print("s : stop")
        print("")
        print("Speed control:")
        print("t/g : increase/decrease linear speed")
        print("y/h : increase/decrease angular speed")
        print("")
        print("HOLD KEY to move continuously")
        print("RELEASE KEY to stop")
        print("")
        print("Current speeds:")
        print(f"Linear: {self.linear_speed:.1f} m/s")
        print(f"Angular: {self.angular_speed:.1f} rad/s")
        print("")
        print("CTRL-C to quit")
        print("="*50)
        
    def get_key(self):
        """Đọc một ký tự từ keyboard"""
        tty.setraw(sys.stdin.fileno())
        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
        if rlist:
            key = sys.stdin.read(1)
        else:
            key = ''
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)
        return key
    
    def create_twist_msg(self, linear_x=0.0, linear_y=0.0, angular_z=0.0):
        """Tạo Twist message"""
        twist = Twist()
        twist.linear.x = linear_x
        twist.linear.y = linear_y
        twist.linear.z = 0.0
        twist.angular.x = 0.0
        twist.angular.y = 0.0
        twist.angular.z = angular_z
        return twist
    
    def run(self):
        """Vòng lặp chính"""
        try:
            current_twist = Twist()  # Lưu trạng thái chuyển động hiện tại
            
            while rclpy.ok():
                key = self.get_key()
                
                # Nếu không có key nào được nhấn, dừng robot
                if key == '':
                    current_twist = self.create_twist_msg()
                    self.cmd_vel_pub.publish(current_twist)
                    continue
                    
                # Chuyển động cơ bản
                if key == 'w':  # Forward
                    current_twist = self.create_twist_msg(linear_x=self.linear_speed)
                    self.get_logger().info('Moving forward')
                    
                elif key == 'x':  # Backward
                    current_twist = self.create_twist_msg(linear_x=-self.linear_speed)
                    self.get_logger().info('Moving backward')
                    
                elif key == 'a':  # Strafe left
                    current_twist = self.create_twist_msg(linear_y=self.linear_speed)
                    self.get_logger().info('Strafing left')
                    
                elif key == 'd':  # Strafe right
                    current_twist = self.create_twist_msg(linear_y=-self.linear_speed)
                    self.get_logger().info('Strafing right')
                    
                # Chuyển động chéo
                elif key == 'q':  # Forward-left diagonal
                    current_twist = self.create_twist_msg(
                        linear_x=self.linear_speed * 0.7,
                        linear_y=self.linear_speed * 0.7
                    )
                    self.get_logger().info('Moving forward-left diagonal')
                    
                elif key == 'e':  # Forward-right diagonal
                    current_twist = self.create_twist_msg(
                        linear_x=self.linear_speed * 0.7,
                        linear_y=-self.linear_speed * 0.7
                    )
                    self.get_logger().info('Moving forward-right diagonal')
                    
                elif key == 'z':  # Backward-left diagonal
                    current_twist = self.create_twist_msg(
                        linear_x=-self.linear_speed * 0.7,
                        linear_y=self.linear_speed * 0.7
                    )
                    self.get_logger().info('Moving backward-left diagonal')
                    
                elif key == 'c':  # Backward-right diagonal
                    current_twist = self.create_twist_msg(
                        linear_x=-self.linear_speed * 0.7,
                        linear_y=-self.linear_speed * 0.7
                    )
                    self.get_logger().info('Moving backward-right diagonal')
                    
                # Chuyển động xoay
                elif key == 'u':  # Rotate left
                    current_twist = self.create_twist_msg(angular_z=self.angular_speed)
                    self.get_logger().info('Rotating left')
                    
                elif key == 'i':  # Rotate right
                    current_twist = self.create_twist_msg(angular_z=-self.angular_speed)
                    self.get_logger().info('Rotating right')
                    
                # Stop
                elif key == 's':
                    current_twist = self.create_twist_msg()
                    self.get_logger().info('Stopping')
                    
                # Speed control
                elif key == 't':  # Increase linear speed
                    self.linear_speed = min(2.0, self.linear_speed + self.speed_increment)
                    self.get_logger().info(f'Linear speed: {self.linear_speed:.1f} m/s')
                    continue
                    
                elif key == 'g':  # Decrease linear speed
                    self.linear_speed = max(0.1, self.linear_speed - self.speed_increment)
                    self.get_logger().info(f'Linear speed: {self.linear_speed:.1f} m/s')
                    continue
                    
                elif key == 'y':  # Increase angular speed
                    self.angular_speed = min(3.0, self.angular_speed + self.speed_increment)
                    self.get_logger().info(f'Angular speed: {self.angular_speed:.1f} rad/s')
                    continue
                    
                elif key == 'h':  # Decrease angular speed
                    self.angular_speed = max(0.1, self.angular_speed - self.speed_increment)
                    self.get_logger().info(f'Angular speed: {self.angular_speed:.1f} rad/s')
                    continue
                    
                elif key == '\x03':  # Ctrl+C
                    break
                    
                else:
                    if key != '':
                        self.get_logger().warn(f'Unknown key: {key}')
                    # Giữ nguyên chuyển động hiện tại
                
                # Publish twist message
                self.cmd_vel_pub.publish(current_twist)
                
        except Exception as e:
            self.get_logger().error(f'Error: {e}')
            
        finally:
            # Send stop command
            twist = self.create_twist_msg()
            self.cmd_vel_pub.publish(twist)
            self.get_logger().info('Teleop stopped')


def main(args=None):
    rclpy.init(args=args)
    
    try:
        teleop = MecanumTeleop()
        teleop.run()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f'Error: {e}')
    finally:
        # Restore terminal settings
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, termios.tcgetattr(sys.stdin))
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
