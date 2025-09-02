#!/usr/bin/env python3

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    # Include main robot launch with simulation parameters
    robot_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('mecanum_bringup'),
                'launch',
                'mecanum_robot.launch.py'
            ])
        ]),
        launch_arguments={
            'use_sim_time': 'true',
            'use_rviz': 'true',
            'use_controller': 'true'
        }.items()
    )
    
    return LaunchDescription([
        robot_launch,
    ])
