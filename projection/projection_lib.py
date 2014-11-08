import numpy as np
import math
import matplotlib.pyplot as plt

def pts_set_2():

  def create_intermediate_points(pt1, pt2, granularity):
    new_pts = []
    vector = np.array([(x[0] - x[1]) for x in zip(pt1, pt2)])
    return [(np.array(pt2) + (vector * (float(i)/granularity))) for i in range(1, granularity)]

  pts = []
  granularity = 20

  # Create cube wireframe
  pts.extend([[-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1], \
              [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]])

  pts.extend(create_intermediate_points([-1, -1, 1], [1, -1, 1], granularity))
  pts.extend(create_intermediate_points([1, -1, 1], [1, 1, 1], granularity))
  pts.extend(create_intermediate_points([1, 1, 1], [-1, 1, 1], granularity))
  pts.extend(create_intermediate_points([-1, 1, 1], [-1, -1, 1], granularity))

  pts.extend(create_intermediate_points([-1, -1, -1], [1, -1, -1], granularity))
  pts.extend(create_intermediate_points([1, -1, -1], [1, 1, -1], granularity))
  pts.extend(create_intermediate_points([1, 1, -1], [-1, 1, -1], granularity))
  pts.extend(create_intermediate_points([-1, 1, -1], [-1, -1, -1], granularity))

  pts.extend(create_intermediate_points([1, 1, 1], [1, 1, -1], granularity))
  pts.extend(create_intermediate_points([1, -1, 1], [1, -1, -1], granularity))
  pts.extend(create_intermediate_points([-1, -1, 1], [-1, -1, -1], granularity))
  pts.extend(create_intermediate_points([-1, 1, 1], [-1, 1, -1], granularity))

  # Create triangle wireframe
  pts.extend([[-0.5, -0.5, -1], [0.5, -0.5, -1], [0, 0.5, -1]])
  pts.extend(create_intermediate_points([-0.5, -0.5, -1], [0.5, -0.5, -1], granularity))
  pts.extend(create_intermediate_points([0.5, -0.5, -1], [0, 0.5, -1], granularity))
  pts.extend(create_intermediate_points([0, 0.5, -1], [-0.5, -0.5, -1], granularity))

  return np.array(pts)

pts = pts_set_2()


def quatmult(p, q):
    # quaternion multiplication
    out = [p[0]*q[0] - p[1]*q[1] - p[2]*q[2] - p[3]*q[3],
           p[0]*q[1] + p[1]*q[0] + p[2]*q[3] - p[3]*q[2],
           p[0]*q[2] - p[1]*q[3] + p[2]*q[0] + p[3]*q[1],
           p[0]*q[3] + p[1]*q[2] - p[2]*q[1] + p[3]*q[0]]
    return out

def conjugate(p):
    return [p[0],-p[1],-p[2],-p[3]]

#print quatmult([1,0,1,0], [1,0.5,0.5,0.75])
#print quatmult([-math.sin(np.pi),3,4,3], [4,3.9,-1,-3])

def quat2rot(q):
    """
    :param q:
    :return a 3x3 rotation matrix parameterized with the elements of a given input quaternion.
    """
    q0 = q[0]
    q1 = q[1]
    q2 = q[2]
    q3 = q[3]
    R = [[q0**2+q1**2-q2**2-q3**2, 2*((q1*q2)-(q0*q3)), 2*((q1*q3)+(q0*q2))],
         [2*((q1*q2)+(q0*q3)), q0**2+q2**2-q1**2-q3**2, 2*((q2*q3)-(q0*q1))],
         [2*((q1*q3)-(q0*q2)), 2*((q2*q3)+(q0*q1)), q0**2+q3**2-q1**2-q2**2]]
    return np.matrix(R)
