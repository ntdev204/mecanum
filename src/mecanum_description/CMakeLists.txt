cmake_minimum_required(VERSION 3.8)
project(mecanum_description)

find_package(ament_cmake REQUIRED)

# Install URDF and launch files
install(DIRECTORY launch urdf rviz
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
