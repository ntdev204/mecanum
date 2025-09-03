#include "mecanum_kinematics/kinematics.hpp"

MecanumKinematics::MecanumKinematics() 
: Node("mecanum_kinematics_node"), L_(0.3), W_(0.2), R_(0.05) {
    cmd_vel_sub_ = this->create_subscription<geometry_msgs::msg::Twist>(
        "cmd_vel", 10, std::bind(&MecanumKinematics::cmdVelCallback, this, std::placeholders::_1)
    );
    wheel_vel_pub_ = this->create_publisher<mecanum_msgs::msg::WheelVelocity>("wheel_vel", 10);

    RCLCPP_INFO(this->get_logger(), "Mecanum kinematics node started");
}

void MecanumKinematics::cmdVelCallback(const geometry_msgs::msg::Twist::SharedPtr msg) {
    double vx = msg->linear.x;
    double vy = msg->linear.y;
    double wz = msg->angular.z;

    double fl = (1.0/R_) * ( vx - vy - (L_+W_)*wz );
    double fr = (1.0/R_) * ( vx + vy + (L_+W_)*wz );
    double rl = (1.0/R_) * ( vx + vy - (L_+W_)*wz );
    double rr = (1.0/R_) * ( vx - vy + (L_+W_)*wz );

    auto wheel_msg = mecanum_msgs::msg::WheelVelocity();
    wheel_msg.front_left  = fl;
    wheel_msg.front_right = fr;
    wheel_msg.rear_left   = rl;
    wheel_msg.rear_right  = rr;

    wheel_vel_pub_->publish(wheel_msg);
}
