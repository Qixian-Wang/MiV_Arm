import numpy as np
import matplotlib.pyplot as plt
import roboticstoolbox as rtb
from mpl_toolkits.mplot3d import Axes3D
from roboticstoolbox.robot.DHRobot import DHRobot
from roboticstoolbox.robot.DHLink import RevoluteMDH 

from utils import w_p_to_Slist, get_joint_axes_from_robot, get_joint_positions_from_robot

class Kinematics:
    def __init__(self, urdf_path, joint_limits):
        self.robot = rtb.ERobot.URDF(urdf_path)
        self.num_joints = self.robot.n
        self.num_links = self.num_joints + 1 # We suppose the number of links is one more than the number of joints
        self.q0 = np.zeros(self.num_joints)

        self.robot.qlim = joint_limits

    def check_robot_urdf(self):
        print(self.robot)
        print("DoF:", self.robot.n)

    def show_robot_demo(self):
        self.robot.teach(
            q=self.q0,
            block=True,
            limits=None,
            vellipse=False,
            fellipse=False,
            backend='pyplot'
        )

    def compute_Slist(self):
        expected_axes = get_joint_axes_from_robot(self.robot, self.num_joints)
        joint_positions = get_joint_positions_from_robot(self.q0, self.robot, self.num_links)

        slist = w_p_to_Slist(expected_axes, joint_positions, self.num_joints)
        print("Slist:\n", slist)
        return slist
    
    def compute_M(self):
        m_matrix = self.robot.fkine(self.q0).A
        print("M:\n", m_matrix)
        return m_matrix
    
    def draw_workspace(self, n_samples=5000) :
        points = []
        for _ in range(n_samples):
            q = np.random.uniform(self.robot.qlim[0, :], self.robot.qlim[1, :])
            T = self.robot.fkine(q)
            pos = T.t
            points.append(pos)

        points = np.array(points) * 1000 # Convert to mm

        fig, axes = plt.subplots(2, 2, figsize=(15, 12))

        # XY plane (top view)
        scatter_xy = axes[0, 0].scatter(points[:, 0], points[:, 1], c=points[:, 2], 
                            cmap='plasma', alpha=0.6, s=1)
        axes[0, 0].set_xlabel('X (mm)')
        axes[0, 0].set_ylabel('Y (mm)')
        axes[0, 0].set_title('Workspace - XY Plane (Top View)')
        axes[0, 0].axis('equal')
        axes[0, 0].grid(True)
        cbar_xy = plt.colorbar(scatter_xy, ax=axes[0, 0])
        cbar_xy.set_label('Z (mm)')

        # XZ plane (side view)
        scatter_xz = axes[0, 1].scatter(points[:, 0], points[:, 2], c=points[:, 1], 
                            cmap='plasma', alpha=0.6, s=1)
        axes[0, 1].set_xlabel('X (mm)')
        axes[0, 1].set_ylabel('Z (mm)')
        axes[0, 1].set_title('Workspace - XZ Plane (Side View)')
        axes[0, 1].axis('equal')
        axes[0, 1].grid(True)
        cbar_xz = plt.colorbar(scatter_xz, ax=axes[0, 1])
        cbar_xz.set_label('Y (mm)')

        # YZ plane (front view)
        scatter_yz = axes[1, 0].scatter(points[:, 1], points[:, 2], c=points[:, 0], 
                            cmap='plasma', alpha=0.6, s=1)
        axes[1, 0].set_xlabel('Y (mm)')
        axes[1, 0].set_ylabel('Z (mm)')
        axes[1, 0].set_title('Workspace - YZ Plane (Front View)')
        axes[1, 0].axis('equal')
        axes[1, 0].grid(True)
        cbar_yz = plt.colorbar(scatter_yz, ax=axes[1, 0])
        cbar_yz.set_label('X (mm)')

        plt.tight_layout()
        plt.savefig('workspace.png', format='png', dpi=300)
        plt.close("all")

