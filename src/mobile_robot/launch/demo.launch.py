from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():

    use_sim_time = LaunchConfiguration('use_sim_time')

    urdf_file = PathJoinSubstitution([
        FindPackageShare('mobile_robot'),
        'urdf',
        'robot.urdf.xml'
    ])

    robot_description = ParameterValue(
        Command([
            'cat ',
            urdf_file
        ]),
        value_type=str
    )

    return LaunchDescription([

        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation clock if true'
        ),

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[
                {
                    'use_sim_time': use_sim_time,
                    'robot_description': robot_description
                }
            ]
        ),

        Node(
            package='mobile_robot',
            executable='state_publisher',
            name='state_publisher',
            output='screen',
            parameters=[
                {
                    'use_sim_time': use_sim_time
                }
            ]
        ),
    ])