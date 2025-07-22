import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from roboticstoolbox.robot.DHRobot import DHRobot
from roboticstoolbox.robot.DHLink import RevoluteMDH 

# L1 = RevoluteMDH( d=105.03,     a=0,        alpha=0,            offset=np.pi/2,     modified=True )
# L2 = RevoluteMDH( d=0,          a=0,        alpha=np.pi/2,      offset=np.pi/2,     modified=True )
# L3 = RevoluteMDH( d=0.00,       a=300,      alpha=0,            offset=np.pi/2,     modified=True )
# L4 = RevoluteMDH( d=300,        a=0,        alpha=np.pi/2,      offset=np.pi/2,     modified=True )
# L5 = RevoluteMDH( d=0,          a=0,        alpha=np.pi/2,      offset=np.pi/2,     modified=True )
# L6 = RevoluteMDH( d=0,          a=50,       alpha=np.pi/2,      offset=0.0,         modified=True )

def generate_robot():
    L1 = RevoluteMDH( d=129.5,      a=0,        alpha=0,            offset=np.pi/2,     modified=True )
    L2 = RevoluteMDH( d=0,          a=0,        alpha=-np.pi/2,     offset=-np.pi/2,    modified=True )
    L3 = RevoluteMDH( d=0.00,       a=305.37,   alpha=0,            offset=0,           modified=True )
    L4 = RevoluteMDH( d=300,        a=0,        alpha=np.pi/2,      offset=np.pi/2,     modified=True )
    L5 = RevoluteMDH( d=0,          a=0,        alpha=np.pi/2,      offset=np.pi,     modified=True )
    L6 = RevoluteMDH( d=65,         a=0,        alpha=np.pi/2,      offset=0.0,         modified=True )

    robot_mdh = DHRobot([L1, L2, L3, L4, L5, L6], name='ViperX_MDH')

    # Joint angle limits
    robot_mdh.qlim = np.array([
        [-np.deg2rad(180), -np.deg2rad(101), -np.deg2rad(92), -np.deg2rad(180), -np.deg2rad(107), -np.deg2rad(180)],  # Lower limits
        [np.deg2rad(180), np.deg2rad(101), np.deg2rad(101), np.deg2rad(180), np.deg2rad(130), np.deg2rad(180)]           # Upper limits
    ])

    return robot_mdh


def generate_workspace(n_samples, draw_3d=False, draw_2d=True, enable_teach=False):
    robot = generate_robot()
    points = []
    for _ in range(n_samples):
        q = np.random.uniform(robot.qlim[0, :], robot.qlim[1, :])
        T = robot.fkine(q)
        pos = T.t
        points.append(pos)

    # Convert points list to numpy array
    points = np.array(points)

    if draw_3d:
        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection='3d')
        scatter = ax.scatter(points[:, 0], points[:, 1], points[:, 2], 
                    c=points[:, 2], cmap='viridis', alpha=0.6, s=1)
        ax.scatter([0], [0], [0], c='red', s=100, marker='o', label='Robot Base')

        ax.set_xlabel('X (mm)')
        ax.set_ylabel('Y (mm)')
        ax.set_zlabel('Z (mm)')
        ax.set_title('Reachable Workspace')
        ax.legend()

        # Add colorbar for 3D plot
        cbar = plt.colorbar(scatter, ax=ax, shrink=0.5, aspect=5)
        cbar.set_label('Z (mm)', rotation=270, labelpad=15)

        # Set equal aspect ratio
        max_range = np.array([points[:, 0].max()-points[:, 0].min(),
                                points[:, 1].max()-points[:, 1].min(),
                                points[:, 2].max()-points[:, 2].min()]).max() / 2.0
        mid_x = (points[:, 0].max()+points[:, 0].min()) * 0.5
        mid_y = (points[:, 1].max()+points[:, 1].min()) * 0.5
        mid_z = (points[:, 2].max()+points[:, 2].min()) * 0.5

        ax.set_xlim(mid_x - max_range, mid_x + max_range)
        ax.set_ylim(mid_y - max_range, mid_y + max_range)
        ax.set_zlim(mid_z - max_range, mid_z + max_range)

        plt.show()

    if draw_2d:
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
        plt.savefig('workspace_2d.png', format='png', dpi=1000)
        plt.close("all")

    if enable_teach:
        robot.teach(
            q=np.array([0, 0, 0, 0, 0, 0]),
            block=True,
            limits=None,
            vellipse=False,
            fellipse=False,
            backend='pyplot'
        )

if __name__ == "__main__":
    generate_workspace(n_samples=10000, draw_3d=False, draw_2d=True, enable_teach=False)