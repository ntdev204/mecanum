# Mecanum Robot ROS2 Package

Hệ thống điều khiển robot mecanum với ROS2 Humble.

## Cấu trúc Package

```
mecanum/
├── src/
│   ├── mecanum_msgs/          # Custom messages cho robot
│   ├── mecanum_description/   # URDF và visualization
│   ├── mecanum_control/       # Node điều khiển robot
│   └── mecanum_bringup/      # Launch files và scripts
```

## Build System

```bash
# Build toàn bộ workspace
cd /path/to/workspace
colcon build

# Build một package cụ thể
colcon build --packages-select <package_name>

# Source environment
source install/setup.bash
```

## Chạy Hệ Thống

### 1. Visualization (Display only)
```bash
# Chỉ hiển thị robot trong RViz
ros2 launch mecanum_description display.launch.py
```

### 2. Hệ thống đầy đủ (Bringup)
```bash
# Chạy toàn bộ hệ thống với RViz
ros2 launch mecanum_bringup mecanum_robot.launch.py

# Chạy cho hardware thật (không RViz)
ros2 launch mecanum_bringup hardware.launch.py

# Chạy cho simulation
ros2 launch mecanum_bringup simulation.launch.py
```

### 3. Keyboard Teleop
```bash
# Terminal 1: Chạy robot system
ros2 launch mecanum_bringup mecanum_robot.launch.py

# Terminal 2: Chạy keyboard control
ros2 run mecanum_teleop teleop_keyboard
```

#### Keyboard Controls:
```
Moving around:
   q    w    e
   a    s    d
   z    x    c
        u i

Movement controls:
w/x : forward/backward
a/d : strafe left/right
q/e : forward-left/right diagonal
z/c : backward-left/right diagonal
u/i : rotate left/right
s : stop

Speed control:
t/g : increase/decrease linear speed
y/h : increase/decrease angular speed

HOLD KEY to move continuously
RELEASE KEY to stop
```

### 4. Joystick Teleop
```bash
# Cài đặt joy package (nếu chưa có)
sudo apt install ros-humble-joy

# Chạy với joystick
ros2 launch mecanum_teleop teleop_joy.launch.py
```

### 5. Complete System với Teleop
```bash
# Keyboard control (default)
ros2 launch mecanum_teleop robot_teleop.launch.py

# Joystick control
ros2 launch mecanum_teleop robot_teleop.launch.py use_keyboard:=false use_joy:=true
```

## Cài đặt và Build

```bash
# Clone repository
cd ~/workspace/robot/mecanum

# Build workspace
colcon build

# Source environment
source install/setup.bash
```

## Cách sử dụng

### 1. Hiển thị robot trong RViz (chỉ visualization)

```bash
# Source environment
source install/setup.bash

# Launch robot description với RViz
ros2 launch mecanum_description display.launch.py
```

### 2. Chạy simulation (với controller)

```bash
# Source environment
source install/setup.bash

# Launch simulation
ros2 launch mecanum_bringup simulation.launch.py
```

### 3. Chạy trên hardware thật

```bash
# Source environment
source install/setup.bash

# Launch hardware
ros2 launch mecanum_bringup hardware.launch.py
```

### 4. Kiểm tra chức năng

```bash
# Kiểm tra topics
ros2 topic list

# Gửi lệnh điều khiển
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.5, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.5}}"

# Kiểm tra wheel velocities
ros2 topic echo /wheel_velocities
```

## Cấu trúc Files

```
src/
├── mecanum_msgs/
│   ├── msg/
│   │   └── WheelVelocity.msg
│   ├── CMakeLists.txt
│   └── package.xml
├── mecanum_description/
│   ├── urdf/
│   │   ├── mecanum_robot.urdf.xacro
│   │   └── materials.xacro
│   ├── launch/
│   │   ├── robot_description.launch.py
│   │   └── display.launch.py
│   ├── rviz/
│   │   └── mecanum_robot.rviz
│   ├── CMakeLists.txt
│   └── package.xml
├── mecanum_control/
│   ├── include/mecanum_control/
│   │   └── controller.hpp
│   ├── src/
│   │   └── controller.cpp
│   ├── CMakeLists.txt
│   └── package.xml
└── mecanum_bringup/
    ├── launch/
    │   ├── mecanum_robot.launch.py
    │   ├── simulation.launch.py
    │   └── hardware.launch.py
    ├── config/
    │   └── robot_params.yaml
    ├── CMakeLists.txt
    └── package.xml
```

## Parameters

Các thông số robot có thể được cấu hình trong file `mecanum_bringup/config/robot_params.yaml`:

- `base_width`: Khoảng cách giữa bánh trái và phải (m)
- `base_length`: Khoảng cách giữa bánh trước và sau (m)  
- `wheel_radius`: Bán kính bánh xe (m)
- `max_linear_velocity`: Vận tốc tịnh tiến tối đa (m/s)
- `max_angular_velocity`: Vận tốc góc tối đa (rad/s)

## Topics

### Published Topics

- `/wheel_velocities` (mecanum_msgs/WheelVelocity): Vận tốc các bánh xe
- `/robot_description` (std_msgs/String): Mô tả URDF robot
- `/joint_states` (sensor_msgs/JointState): Trạng thái các joint

### Subscribed Topics

- `/cmd_vel` (geometry_msgs/Twist): Lệnh điều khiển vận tốc

## Troubleshooting

1. **Lỗi không tìm thấy package**: Đảm bảo đã source environment
2. **RViz không hiển thị robot**: Kiểm tra robot_description topic
3. **Controller không hoạt động**: Kiểm tra /cmd_vel topic
