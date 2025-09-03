#include "rclcpp/rclcpp.hpp"
#include "mecanum_kinematics/kinematics.hpp"

int main(int argc, char **argv) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<MecanumKinematics>());
    rclcpp::shutdown();
    return 0;
}
