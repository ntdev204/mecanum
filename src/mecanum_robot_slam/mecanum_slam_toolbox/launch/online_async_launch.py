from ament_index_python.packages import get_package_share_directory
import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
import launch_ros.actions
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.conditions import IfCondition
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    bringup_dir = get_package_share_directory('turn_on_mecanum_robot')
    launch_dir = os.path.join(bringup_dir, 'launch')

    mecanum_robot = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(launch_dir, 'turn_on_mecanum_robot.launch.py')),
    )
    mecanum_lidar = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(launch_dir, 'mecanum_lidar.launch.py')),
    )
    return LaunchDescription([
        mecanum_robot,mecanum_lidar,
        launch_ros.actions.Node(
        	parameters=[
        		get_package_share_directory("mecanum_slam_toolbox") + '/config/mapper_params_online_async.yaml'
        	],
            package='slam_toolbox',
            executable='async_slam_toolbox_node',
            name='slam_toolbox',
            output='screen',
            remappings=[('odom','odom_combined')]
        )
    ])
