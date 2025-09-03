#pragma once

#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/twist.hpp"
#include "mecanum_msgs/msg/wheel_velocity.hpp"

class MecanumKinematics : public rclcpp::Node {
public:
    MecanumKinematics();

private:
    void cmdVelCallback(const geometry_msgs::msg::Twist::SharedPtr msg);

    rclcpp::Subscription<geometry_msgs::msg::Twist>::SharedPtr cmd_vel_sub_;
    rclcpp::Publisher<mecanum_msgs::msg::WheelVelocity>::SharedPtr wheel_vel_pub_;

    double L_, W_, R_;
};
