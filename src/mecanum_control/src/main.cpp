#include "rclcpp/rclcpp.hpp"
#include "mecanum_control/controller.hpp"

int main(int argc, char **argv) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<MecanumController>());
    rclcpp::shutdown();
    return 0;
}
