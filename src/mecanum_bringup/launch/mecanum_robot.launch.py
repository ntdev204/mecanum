#!/usr/bin/env python3

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, GroupAction
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, Command
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    # Declare launch arguments
    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation (Gazebo) clock if true'
    )
    
    use_rviz_arg = DeclareLaunchArgument(
        'use_rviz',
        default_value='true',
        description='Start RViz2 for visualization'
    )
    
    use_controller_arg = DeclareLaunchArgument(
        'use_controller',
        default_value='true',
        description='Start mecanum controller'
    )

    # Get the package directory
    pkg_path = FindPackageShare('mecanum_description')
    
    # Path to the URDF file
    urdf_file = PathJoinSubstitution([pkg_path, 'urdf', 'mecanum_robot.urdf.xacro'])
    
    # Robot State Publisher node
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': Command(['xacro ', urdf_file]),
            'use_sim_time': LaunchConfiguration('use_sim_time')
        }]
    )
    
    # Joint State Publisher node (for testing without real hardware)
    joint_state_publisher = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        output='screen',
        parameters=[{
            'use_sim_time': LaunchConfiguration('use_sim_time')
        }]
    )
    
    # Mecanum kinematics node
    mecanum_kinematics = Node(
        package='mecanum_kinematics',
        executable='mecanum_kinematics_node',
        name='mecanum_kinematics',
        output='screen',
        parameters=[{
            'use_sim_time': LaunchConfiguration('use_sim_time')
        }],
        condition=IfCondition(LaunchConfiguration('use_controller'))
    )
    
    # Odometry node
    odometry_node = Node(
        package='mecanum_kinematics',
        executable='odometry.py',
        name='mecanum_odometry',
        output='screen',
        parameters=[{
            'use_sim_time': LaunchConfiguration('use_sim_time')
        }],
        condition=IfCondition(LaunchConfiguration('use_controller'))
    )
    
    # RViz2 node
    rviz_group = GroupAction([
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=['-d', PathJoinSubstitution([
                FindPackageShare('mecanum_description'),
                'rviz',
                'mecanum_robot_teleop.rviz'
            ])],
            parameters=[{
                'use_sim_time': LaunchConfiguration('use_sim_time')
            }]
        )
    ], condition=IfCondition(LaunchConfiguration('use_rviz')))
    
    return LaunchDescription([
        use_sim_time_arg,
        use_rviz_arg,
        use_controller_arg,
        robot_state_publisher,
        joint_state_publisher,
        mecanum_kinematics,
        odometry_node,
        rviz_group,
    ])
