import numpy as np
import math
import matplotlib.pyplot as plt
from projection_lib import quat2rot, dilate, dilate_and_sky
from mpl_toolkits.mplot3d.axes3d import Axes3D
import matplotlib as mpl
import cv2
import math
import sys
import pickle
from multiprocessing import Process, Pool

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
    degree = 50
    no_frames = 10
    scale = 1
    k = 2
    cam_original_position = get_cam_position(angle=math.radians(degree), no_frames = 1, cam_original_position=[0,0,610,-8 * 100], k=k)[1]
    cam_original_orientation = get_cam_orientation(angle=math.radians(-degree * scale), no_frames = 1)[1]#np.matrix([[0.5,0.,-0.8660254],[0.,1.,0.],[0.8660254,0.,0.5]])
    cam_position = get_cam_position(angle=math.radians(-degree * 2.0 / no_frames), no_frames=no_frames, cam_original_position=cam_original_position, k=k)
    cam_orientation = get_cam_orientation(angle=math.radians(degree * 2.0 * scale / no_frames), no_frames=no_frames, cam_original_orientation = cam_original_orientation)

    """ FOR FASTEST PROJECTION, SET multithread and fill_blank to False """
    project_and_draw(pts1, cam_position, cam_orientation, 0, no_frames-1, multithread=True, fill_blank = False)

def draw_image(pts, filename = "frame.png", use_cloud = False, fill_blank=False, shift=0):
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
    row = 1100
    column = 1700
    if use_cloud:
        projection_matrix = cv2.imread("cloud.jpg")
    else:
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
                    x_proj += 900
                    y_proj += 500
                    if pts[x,y,1] != 1:
                        print x_proj
                        print y_proj
                    if (0 <= x_proj < column and 0 <= y_proj< row and z < min_depth_arr[y_proj,x_proj]):
                        projection_matrix[y_proj,x_proj]= img[y,x]#pts[x,y,1] if type(pts[x,y,1]) == tuple else [255,255,255]
                        min_depth_arr[y_proj,x_proj] = z
    if fill_blank:
        print "Dilation #1"
        projection_matrix = dilate_and_sky(projection_matrix, shift=shift)

    cv2.imwrite(filename ,projection_matrix[:900, 400:])


def project_and_draw(pts, cam_position, cam_orientation, start_frame, end_frame, multithread = False, fill_blank = False):
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
    pool = Pool()
    for frame in range(start_frame, end_frame+1):
        if multithread:
             #use all available cores, otherwise specify the number you want as an argument
            pool.apply_async(project_and_draw_single_frame, args=(pts, cam_position, cam_orientation, frame, fill_blank))
            #p = Process(target=project_and_draw_single_frame, args=(pts, cam_position, cam_orientation, frame, fill_blank))
            #p.start()
        else:
            project_and_draw_single_frame(pts, cam_position, cam_orientation, frame, fill_blank)
    pool.close()
    pool.join()

def project_and_draw_single_frame(pts, cam_position, cam_orientation, frame, fill_blank=False):
    """
    Project and draw single frame. This used to be part of the function project_and_draw but its has been
    made into a separate function to enable multi-threading.
    """
    print "Starting project and draw frame %d" % frame
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
                    # - 816 because we want to shift our image such that the midpoint has x value of 0
                    sp = np.matrix([[x-816],[y],[z]])
                    u_fp = ((f * np.transpose((sp - tf)) * i_f * Bu) / (np.transpose((sp - tf)) * k_f)) + u0
                    v_fp = ((f * np.transpose((sp - tf)) * j_f * Bv) / (np.transpose((sp - tf)) * k_f)) + v0
                    x_projected = u_fp[0,0]
                    y_projected = v_fp[0,0]
                    if type(new_pts[x,y,2]) == list:
                        new_pts[x,y,2].append((x_projected, y_projected))
                    else:
                        new_pts[x,y,2] = [(x_projected, y_projected)]
    draw_image(new_pts, "result/frame_%d.png" % frame, use_cloud=False,fill_blank=fill_blank, shift=round(frame*5))
    print "Save frame_%d.png" % frame

def get_cam_position(angle = -np.pi/6, no_frames = 12, cam_original_position = [0,0,100,-5 * 100], k = 2):
    """
    Return camera position for each frame using rotation matrix
    **Change k value to make the ellipse flatter. The bigger the value, the more flat it becomes. when k = 1, it becomes a circle
    """
    r = np.matrix([[math.cos(angle), k * math.sin(angle)],[math.sin(angle) * 1/(-k), math.cos(angle)]])
    y = cam_original_position[2]
    cam_position_2d = [[[cam_original_position[1]],[cam_original_position[3]]]] # [x,z]
    cam_position_3d = [cam_original_position]
    for i in range(0, no_frames):
        p = cam_position_2d[i]
        new_cam = r * p
        cam_position_2d.append(new_cam)
        cam_position_3d.append([0, new_cam[0,0], y, new_cam[1,0]])
    return cam_position_3d

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

def test_cam_post():
    degree = 60
    cam_original_position = get_cam_position(angle=math.radians(degree), no_frames = 1, cam_original_position=[0,0,610,-5 * 100])[1]
    cam_position = get_cam_position(angle=math.radians(-12), no_frames=10, cam_original_position=cam_original_position)
    print cam_position
    #print get_cam_position(angle = math.radians(-12), no_frames=12, cam_original_position=[0,0,100,-500])

def test_cam_orient():
    print get_cam_orientation()


if __name__ == "__main__":
    main()
    #test_cam_post()
    #test_cam_orient()
    #degree = 60
    #print get_cam_orientation(angle=math.radians(-degree), no_frames = 1)
    #print get_cam_position(angle=math.radians(degree), no_frames = 1)
