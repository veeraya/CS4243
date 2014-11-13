import numpy as np
import math
import matplotlib.pyplot as plt
from projection_lib import pts_set_2, quatmult, conjugate, quat2rot
from mpl_toolkits.mplot3d.axes3d import Axes3D
import matplotlib as mpl
import cv2
import math
import sys
import pickle

# GLOBAL Camera intrinsic params
u0 = 0
v0 = 0
Bu = 1
Bv = 1
ku = 1
kv = 1
f = 500

img = cv2.imread("project.jpeg")
def main():
    """
    Test projection and drawing projection into images
    """
    # initializing points
    """
    pts NxNx3
    pts[x,y,0] = z
    pts[x,y,1] = color
    pts[x,y,2] = (x, y) of projected points
    """
    pkl_file = open('data.pkl', 'rU')
    pts1 = pickle.load(pkl_file)
    print "pts1[718,814,0]",pts1[718,814]
    degree = 60
    cam_original_position = get_cam_position(angle=math.radians(degree), no_frames = 1, cam_original_position=[0,0,610,-5 * 100])[1]
    cam_original_orientation = get_cam_orientation(angle=math.radians(-degree), no_frames = 1)[1]#np.matrix([[0.5,0.,-0.8660254],[0.,1.,0.],[0.8660254,0.,0.5]])
    cam_position = get_cam_position(angle=math.radians(-12), no_frames=10, cam_original_position=cam_original_position)
    cam_orientation = get_cam_orientation(angle=math.radians(12), no_frames=10, cam_original_orientation = cam_original_orientation)

    project_and_draw(pts1, cam_position, cam_orientation, 0, 10)

def draw_image(pts, filename = "frame.png"):
    """
    Draw a single image from list of points
    :param pts: list of points of an image
    :param filename: filename of the image to be saved

    Note:
    pts has dimension NxNx3
    pts[x,y,0] = z
    pts[x,y,1] = color
    pts[x,y,2] = (x, y) of projected points
    """
    row = 3000
    column = 3000
    projection_matrix=np.ones((row,column,3))
    projection_matrix[:,:] = [255,255,255]
    min_depth_arr = np.ones((row, column))
    min_depth_arr[:,:] = sys.maxint
    for x in range(0, pts.shape[0]):
        for y in range(0, pts.shape[1]):
            if type(pts[x,y,0]) == tuple or type(pts[x,y,0]) == list:
                for i,z in enumerate(pts[x,y,0]):
                    x_proj = pts[x,y,2][i][0]
                    y_proj = pts[x,y,2][i][1]
                    #print "x",x_proj
                    #print "y",y_proj
                    x_proj += 2000
                    y_proj += 700
                    if pts[x,y,1] != 1:
                        print x_proj
                        print y_proj
                    if (0 <= x_proj < row and 0 <= y_proj<column and z < min_depth_arr[y_proj,x_proj]):
                        projection_matrix[y_proj,x_proj]= img[y,x]#pts[x,y,1] if type(pts[x,y,1]) == tuple else [255,255,255]
                        min_depth_arr[y_proj,x_proj] = z
    cv2.imwrite(filename ,projection_matrix)


def project_and_draw(pts, cam_position, cam_orientation, start_frame, end_frame):
    """
    :param pts: list of points
    :param cam_position: camera position
    :param cam_orientation: camera orientation
    :param start_frame: start frame with index starting from 0
    :param end_frame: end frame

    Note:
    pts has dimension NxNx3
    pts[x,y,0] = z
    pts[x,y,1] = color
    pts[x,y,2] = (x, y) of projected points
    """
    for frame in range(start_frame, end_frame+1):
        new_pts = np.array(pts, copy=True)
        depth_array = np.empty((pts.shape[0], pts.shape[1]))
        depth_array[:,:] = sys.maxint
        tf = np.matrix(cam_position[frame][1:]).reshape(3,1)
        i_f = np.matrix(cam_orientation[frame][:][0]).reshape(3,1)
        j_f = np.matrix(cam_orientation[frame][:][1]).reshape(3,1)
        k_f = np.matrix(cam_orientation[frame][:][2]).reshape(3,1)
        for x in range(0, pts.shape[0]):
            for y in range(0, pts.shape[1]):
                if type(pts[x,y,0]) == tuple or type(pts[x,y,0]) == list:
                    for z in pts[x,y,0]:
                        sp = np.matrix([[x-816],[y],[z]])
                        #sp = np.matrix(pts1[i, :]).reshape(3,1)
                        u_fp = ((f * np.transpose((sp - tf)) * i_f * Bu) / (np.transpose((sp - tf)) * k_f)) + u0
                        v_fp = ((f * np.transpose((sp - tf)) * j_f * Bv) / (np.transpose((sp - tf)) * k_f)) + v0
                        x_projected = u_fp[0,0]
                        y_projected = v_fp[0,0]
                        if type(new_pts[x,y,2]) == list:
                            new_pts[x,y,2].append((x_projected, y_projected))
                        else:
                            new_pts[x,y,2] = [(x_projected, y_projected)]
        draw_image(new_pts, "frame_%d.png" % frame)
        print "Save frame_%d.png" % frame

def get_cam_position(angle = -np.pi/6, no_frames = 4, cam_original_position = [0,100,100,-5 * 100]):
    """ Return camera position for frame 2-4 using quaternion maths """
    cam_position = []
    cam_position.append(cam_original_position)
    q = [math.cos(angle/2), 0, math.sin(angle/2), 0]
    q_conj = conjugate(q)
    # print "Quaternion rotation:", q
    # print "Q prime:", q_conj
    for i in range(0, no_frames):
        new_cam = quatmult(quatmult(q,cam_position[-1]), q_conj)
        cam_position.append(new_cam)
    return cam_position

def get_cam_orientation(angle = np.pi/6, no_frames = 4, cam_original_orientation = np.matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])):
    """ Return camera orientation """
    q_cam = [math.cos(angle/2), 0, math.sin(angle/2), 0]
    r_matrix = quat2rot(q_cam)
    cam_orientation = []
    cam_orientation.append(cam_original_orientation)
    for i in range(0, no_frames):
        new_quatmat = r_matrix * cam_orientation[-1]
        cam_orientation.append(new_quatmat)
    return cam_orientation

if __name__ == "__main__":
    main()
    #degree = 60
    #print get_cam_orientation(angle=math.radians(-degree), no_frames = 1)
    #print get_cam_position(angle=math.radians(degree), no_frames = 1)
