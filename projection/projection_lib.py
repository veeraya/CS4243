import numpy as np
import math
import matplotlib.pyplot as plt

def fill_blank(img):
    num_row = img.shape[0]
    num_col = img.shape[1]

    for y in range(num_row-2, -1, -1):
        for x in range(num_col-2, -1, -1):
            if np.array_equal(img[x,y], [255,255,255]):
                if not np.array_equal(img[x-1,y], [255,255,255]):
                    img[x,y] = img[x-1,y]
                elif not np.array_equal(img[x-2,y], [255,255,255]):
                    img[x,y] = img[x-2,y]
                elif not np.array_equal(img[x,y-1], [255,255,255]):
                    img[x,y] = img[x,y-1]
                elif not np.array_equal(img[x,y-2], [255,255,255]):
                    img[x,y] = img[x,y-2]

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
