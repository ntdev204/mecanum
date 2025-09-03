#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, TransformStamped
from nav_msgs.msg import Odometry
from tf2_ros import TransformBroadcaster
import math
import time


class MecanumOdometry(Node):
    def __init__(self):
        super().__init__('mecanum_odometry')
        
        # Publishers
        self.odom_pub = self.create_publisher(Odometry, '/odom', 10)
        self.tf_broadcaster = TransformBroadcaster(self)
        
        # Subscribers
        self.cmd_vel_sub = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_vel_callback,
            10
        )
        
        # Robot state
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        
        # Current velocities
        self.vx = 0.0
        self.vy = 0.0
        self.vth = 0.0
        
        # Time tracking
        self.last_time = time.time()
        
        # Timer for odometry publishing
        self.timer = self.create_timer(0.02, self.publish_odometry)  # 50Hz
        
        self.get_logger().info('Mecanum Odometry Node started')
        
    def cmd_vel_callback(self, msg):
        """Update current velocities from cmd_vel"""
        self.vx = msg.linear.x
        self.vy = msg.linear.y
        self.vth = msg.angular.z
        
    def publish_odometry(self):
        """Publish odometry and transform"""
        current_time = time.time()
        dt = current_time - self.last_time
        self.last_time = current_time
        
        # Update robot position based on velocities
        # For mecanum wheels, we can move in any direction
        delta_x = (self.vx * math.cos(self.theta) - self.vy * math.sin(self.theta)) * dt
        delta_y = (self.vx * math.sin(self.theta) + self.vy * math.cos(self.theta)) * dt
        delta_th = self.vth * dt
        
        self.x += delta_x
        self.y += delta_y
        self.theta += delta_th
        
        # Normalize theta
        while self.theta > math.pi:
            self.theta -= 2.0 * math.pi
        while self.theta < -math.pi:
            self.theta += 2.0 * math.pi
            
        # Create odometry message
        odom = Odometry()
        odom.header.stamp = self.get_clock().now().to_msg()
        odom.header.frame_id = 'odom'
        odom.child_frame_id = 'base_footprint'
        
        # Position
        odom.pose.pose.position.x = self.x
        odom.pose.pose.position.y = self.y
        odom.pose.pose.position.z = 0.0
        
        # Orientation (quaternion from yaw)
        odom.pose.pose.orientation.x = 0.0
        odom.pose.pose.orientation.y = 0.0
        odom.pose.pose.orientation.z = math.sin(self.theta / 2.0)
        odom.pose.pose.orientation.w = math.cos(self.theta / 2.0)
        
        # Velocity
        odom.twist.twist.linear.x = self.vx
        odom.twist.twist.linear.y = self.vy
        odom.twist.twist.linear.z = 0.0
        odom.twist.twist.angular.x = 0.0
        odom.twist.twist.angular.y = 0.0
        odom.twist.twist.angular.z = self.vth
        
        # Publish odometry
        self.odom_pub.publish(odom)
        
        # Publish transform
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'odom'
        t.child_frame_id = 'base_footprint'
        
        t.transform.translation.x = self.x
        t.transform.translation.y = self.y
        t.transform.translation.z = 0.0
        
        t.transform.rotation.x = 0.0
        t.transform.rotation.y = 0.0
        t.transform.rotation.z = math.sin(self.theta / 2.0)
        t.transform.rotation.w = math.cos(self.theta / 2.0)
        
        self.tf_broadcaster.sendTransform(t)


def main(args=None):
    rclpy.init(args=args)
    
    try:
        odometry_node = MecanumOdometry()
        rclpy.spin(odometry_node)
    except KeyboardInterrupt:
        pass
    finally:
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
