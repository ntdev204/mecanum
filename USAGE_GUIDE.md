# Mecanum Robot - Hướng Dẫn Sử Dụng

## 🤖 Giới Thiệu
Hệ thống robot mecanum với điều khiển 10 hướng và hiển thị trong RViz.

## 📦 Các Package

### 1. mecanum_msgs
- **Mục đích**: Định nghĩa custom messages
- **File chính**: `WheelVelocity.msg`

### 2. mecanum_description  
- **Mục đích**: Mô tả robot và hiển thị
- **File chính**: 
  - `mecanum_robot.urdf.xacro` - Mô hình robot
  - `display.launch.py` - Launch RViz

### 3. mecanum_control
- **Mục đích**: Logic điều khiển và odometry
- **File chính**:
  - `controller.cpp` - Controller C++
  - `scripts/odometry.py` - Tính toán vị trí

### 4. mecanum_bringup
- **Mục đích**: Khởi động toàn bộ hệ thống
- **File chính**: `mecanum_robot.launch.py`

### 5. mecanum_teleop
- **Mục đích**: Điều khiển từ bàn phím/joystick
- **File chính**: `scripts/teleop_keyboard.py`

## 🚀 Cách Sử Dụng

### Khởi động hệ thống hoàn chỉnh:
```bash
# Terminal 1: Launch robot system
cd ~/workspace/robot/mecanum
source install/setup.bash
ros2 launch mecanum_bringup mecanum_robot.launch.py

# Terminal 2: Keyboard control
cd ~/workspace/robot/mecanum
source install/setup.bash
ros2 run mecanum_teleop teleop_keyboard
```

### Chỉ hiển thị robot trong RViz:
```bash
ros2 launch mecanum_description display.launch.py
```

### Test demo 10 hướng:
```bash
python3 src/mecanum_bringup/scripts/mecanum_demo.py
```

## ⌨️ Điều Khiển Bàn Phím (10 Hướng)

```
q   w   e
|   ↑   |
←   s   →  u (rotate ↺)
|   ↓   |
z   x   c  i (rotate ↻)
```

### Phím điều khiển:
- **w**: Tiến thẳng
- **x**: Lùi thẳng  
- **a**: Sang trái
- **d**: Sang phải
- **q**: Tiến chéo trái
- **e**: Tiến chéo phải
- **z**: Lùi chéo trái
- **c**: Lùi chéo phải
- **u**: Xoay trái
- **i**: Xoay phải
- **s**: Dừng
- **t/g**: Tăng/giảm tốc độ tịnh tiến
- **y/h**: Tăng/giảm tốc độ xoay

## 🎮 Điều Khiển Joystick
```bash
ros2 run mecanum_teleop teleop_joy
```

## 📊 Topics
- `/cmd_vel`: Lệnh điều khiển
- `/odom`: Odometry data  
- `/robot_description`: Mô tả robot
- `/joint_states`: Trạng thái khớp
- `/tf`: Transform tree

## 🛠️ Build System
```bash
cd ~/workspace/robot/mecanum
colcon build
source install/setup.bash
```

## ✅ Tính Năng Đã Hoàn Thành
- ✅ Custom message types
- ✅ Robot description với URDF
- ✅ Hiển thị trong RViz
- ✅ Điều khiển 10 hướng bằng keyboard
- ✅ Điều khiển joystick
- ✅ Odometry và transform tree
- ✅ Launch files tự động
- ✅ Demo script đầy đủ

## 🎯 Hệ Thống Hoàn Chỉnh
Robot mecanum đã sẵn sàng sử dụng với đầy đủ tính năng điều khiển và hiển thị!
