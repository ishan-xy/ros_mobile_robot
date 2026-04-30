from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    pkg_share = FindPackageShare("mobile_robot")

    world_file = PathJoinSubstitution([pkg_share, "sdf", "warehouse.sdf"])
    rviz_config = PathJoinSubstitution([pkg_share, "config", "rviz.rviz"])

    return LaunchDescription([

        ExecuteProcess(
            cmd=["ign", "gazebo", world_file, "-r"],
            output="screen"
        ),

        Node(
            package="ros_gz_bridge",
            executable="parameter_bridge",
            arguments=[
                "/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist",
                "/odom@nav_msgs/msg/Odometry@gz.msgs.Odometry",
                "/scan@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan"
            ],
            output="screen"
        ),

        Node(
            package="teleop_twist_keyboard",
            executable="teleop_twist_keyboard",
            name="teleop",
            output="screen",
            parameters=[
                {"speed": 0.3},
                {"turn": 1.0}
            ],
            prefix="xterm -e"
        ),

        Node(
            package="rviz2",
            executable="rviz2",
            name="rviz2",
            arguments=["-d", rviz_config],
            output="screen"
        ),
    ])