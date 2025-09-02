#!/usr/bin/env python3

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='mecanum_teleop',
            executable='teleop_keyboard',
            name='mecanum_teleop_keyboard',
            output='screen',
            prefix='xterm -e',  # Chạy trong terminal riêng
        )
    ])
