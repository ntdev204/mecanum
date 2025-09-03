cmake_minimum_required(VERSION 3.8)
project(mecanum_kinematics)

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(tf2 REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(mecanum_msgs REQUIRED)

include_directories(include)

add_executable(mecanum_kinematics_node src/main.cpp src/kinematics.cpp)
ament_target_dependencies(mecanum_kinematics_node
  rclcpp
  geometry_msgs
  nav_msgs
  tf2
  tf2_ros
  mecanum_msgs
)

install(TARGETS
  mecanum_kinematics_node
  DESTINATION lib/${PROJECT_NAME}
)

# Install Python scripts
install(PROGRAMS
  scripts/odometry.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
