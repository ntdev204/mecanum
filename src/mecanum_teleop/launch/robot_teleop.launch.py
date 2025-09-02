#!/usr/bin/env python3

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    # Launch arguments
    use_keyboard_arg = DeclareLaunchArgument(
        'use_keyboard',
        default_value='true',
        description='Use keyboard teleop'
    )
    
    use_joy_arg = DeclareLaunchArgument(
        'use_joy',
        default_value='false',
        description='Use joystick teleop'
    )
    
    # Include main robot system
    robot_bringup = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('mecanum_bringup'),
                'launch',
                'mecanum_robot.launch.py'
            ])
        ]),
        launch_arguments={
            'use_rviz': 'true',
            'use_controller': 'true'
        }.items()
    )
    
    # Keyboard teleop node
    keyboard_teleop = Node(
        package='mecanum_teleop',
        executable='teleop_keyboard',
        name='mecanum_teleop_keyboard',
        output='screen',
        condition=IfCondition(LaunchConfiguration('use_keyboard'))
    )
    
    # Joy nodes
    joy_node = Node(
        package='joy',
        executable='joy_node',
        name='joy_node',
        output='screen',
        parameters=[{
            'dev': '/dev/input/js0',
            'deadzone': 0.05,
            'autorepeat_rate': 20.0,
        }],
        condition=IfCondition(LaunchConfiguration('use_joy'))
    )
    
    joy_teleop = Node(
        package='mecanum_teleop',
        executable='teleop_joy',
        name='mecanum_teleop_joy',
        output='screen',
        condition=IfCondition(LaunchConfiguration('use_joy'))
    )
    
    return LaunchDescription([
        use_keyboard_arg,
        use_joy_arg,
        robot_bringup,
        keyboard_teleop,
        joy_node,
        joy_teleop,
    ])
