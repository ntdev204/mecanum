#!/usr/bin/env python3

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        # Joy node để đọc joystick
        Node(
            package='joy',
            executable='joy_node',
            name='joy_node',
            output='screen',
            parameters=[{
                'dev': '/dev/input/js0',  # Joystick device
                'deadzone': 0.05,
                'autorepeat_rate': 20.0,
            }]
        ),
        
        # Mecanum joy teleop node
        Node(
            package='mecanum_teleop',
            executable='teleop_joy',
            name='mecanum_teleop_joy',
            output='screen',
        )
    ])
