import numpy as np

from forward_kinematics import Kinematics


# Define urdf path and robot joint number
urdf_path = "/Users/aia/Desktop/vscode/robot_kenematic/xarm7.urdf"

joint_limits = np.array([
                        [-np.deg2rad(180), -np.deg2rad(101), -np.deg2rad(92), -np.deg2rad(180), -np.deg2rad(107), -np.deg2rad(180)],  # Lower limits
                        [np.deg2rad(180), np.deg2rad(101), np.deg2rad(101), np.deg2rad(180), np.deg2rad(130), np.deg2rad(180)]           # Upper limits
                        ])

robot_kinematics = Kinematics(urdf_path, joint_limits)

# Show robot demo
demo = robot_kinematics.show_robot_demo()

# Compute Slist
Slist = robot_kinematics.compute_Slist()

# Compute M
M = robot_kinematics.compute_M()

# Draw workspace
robot_kinematics.draw_workspace()


# DH, incase it is needed
# L1 = RevoluteMDH( d=129.5,      a=0,        alpha=0,            offset=np.pi/2,     modified=True )
# L2 = RevoluteMDH( d=0,          a=0,        alpha=-np.pi/2,     offset=-np.pi/2,    modified=True )
# L3 = RevoluteMDH( d=0.00,       a=305.37,   alpha=0,            offset=0,           modified=True )
# L4 = RevoluteMDH( d=300,        a=0,        alpha=np.pi/2,      offset=np.pi/2,     modified=True )
# L5 = RevoluteMDH( d=0,          a=0,        alpha=np.pi/2,      offset=np.pi,     modified=True )
# L6 = RevoluteMDH( d=65,         a=0,        alpha=np.pi/2,      offset=0.0,         modified=True )