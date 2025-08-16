import numpy as np

def w_p_to_Slist(w,p,ROBOT_DOF):
    Slist = []
    for i in range(0,ROBOT_DOF):
      w_ = w[i]
      p_ = p[i]
      v_ = -np.cross(w_,p_)
      Slist.append([w_[0],w_[1],w_[2],v_[0],v_[1],v_[2]])
    return np.transpose(Slist)

def get_joint_axes_from_robot(robot, num_joints):
    q0 = np.zeros(robot.n)
    J = robot.jacob0(q0)
    
    joint_axes = []
    for i in range(num_joints):
        omega = J[3:6, i]
        omega = omega / np.linalg.norm(omega)
        joint_axes.append(omega)
    
    return joint_axes

def get_joint_positions_from_robot(q0, robot, num_links):
    joint_positions = []
    for i in range(num_links):
        fk = robot.fkine(q0, robot.links[i])
        joint_positions.append(fk.t)
    return joint_positions[1:]