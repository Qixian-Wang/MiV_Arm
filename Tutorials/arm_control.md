system ros setup
```shell
source /opt/ros/jazzy/setup.bash
```

Launch ROS2:
```shell
ros2 launch <package_name> <launch_file_name>
```

Example:
```shell
ros2 launch <> <> robot_model:=miv_arm
```

Listen to topic:
```shell
ros2 topic echo /miv_arm/joint_states

ros2 topic hz /miv_arm/joint_states

ros2 topic info /miv_arm/joint_states
```

Single joint control:
