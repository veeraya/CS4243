import numpy as np
from projection_lib import pts_set_2, quatmult, conjugate, quat2rot
import cv2
import math
import sys
#from ImageLoader_3 import returnMatrix
from tempfile import TemporaryFile
import pickle



# GLOBAL Camera intrinsic params
u0 = 0
v0 = 0
Bu = 1
Bv = 1
ku = 1
kv = 1
f = 500

def main():
    """
    Test projection and drawing projection into images
    """
    # initializing points
    img = cv2.imread("project.jpeg")

    """
    pts NxNx3
    pts[x,y,0] = z
    pts[x,y,1] = color
    pts[x,y,2] = (x, y) of projected points
    """
    pts1 = np.ones((img.shape[1], img.shape[0], 3), dtype=object)
    #pts1[:,:,1] = (255,255,255)
    """    		   	
    for x in range(16,310):
        for y in range(13, 239):
            pts1[x,y,0] = (20,30)
            pts1[x,y,1] = (53,95,255)

    for x in range(309,484):
        for y in range(161, 239):
            pts1[x,y,0] = (30,31,32,33,34,35,36,37,50)
            pts1[x,y,1] = (255,80,0)
    """
    #pts1 = returnMatrix()
  #    matFile = TemporaryFile()
  #   matFile.seek(0)
  #  pts1 = np.load(matFile)
    pkl_file = open('data.pkl', 'rb')
    
    pts1 = pickle.load(pkl_file)
    print "\nimg.shape[0] : ",img.shape[0]
    print "\nimg.shape[1] : ",img.shape[1]
    for x in range(img.shape[1]):
	for y in range(img.shape[0]):
		pts1[x,y,1] = (img[y,x,0],img[y,x,1],img[y,x,2])

    print "pts1[718,814,0] \n",pts1[718,814,0]
		

#    cv2.imwrite('image.jpeg',img)
#    cv2.waitKey(0)
    degree = 60
    cam_orient = get_cam_orientation(angle=math.radians(-degree), no_frames = 1)
    cam_pos = get_cam_position(angle=math.radians(degree), no_frames = 1)
    #pts1 = np.loadtxt("Image.bin")
   # cam_original_position = [0.0, -383.0127018922193, 100.0, -100.60254037844396] 	#[0.0, -816.0254037844386, 100.0, -586.602540378444]
#    cam_original_position = [0.0, -100.0, 600.0, 195.0]
    cam_original_position = cam_pos[1]
#    cam_original_orientation = np.matrix([[0.5,0.0,-0.8660254],[0.0,1.0,0.0],[0.8660254,0.0,0.5]])
    cam_original_orientation = cam_orient[1]

    cam_position = get_cam_position(angle=math.radians(-12), no_frames=10, cam_original_position=cam_original_position)
    cam_orientation = get_cam_orientation(angle=math.radians(12), no_frames=10, cam_original_orientation = cam_original_orientation)
    #all_pts = project_points(pts1, cam_position, cam_orientation, 0, 3)
    #draw_image(all_pts)
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
            if type(pts[x,y,0]) == tuple:
                for i,z in enumerate(pts[x,y,0]):
                    # z = pts[x,y,0]
		    
       		    
                    x_proj = pts[x,y,2][i][0]
                    y_proj = pts[x,y,2][i][1]
                    x_proj += 600
                    y_proj += 700
                    if (z < min_depth_arr[y_proj,x_proj] and 0 <= x_proj < row and 0 <= y_proj<column):
                        projection_matrix[y_proj,x_proj]= pts[x,y,1] if type(pts[x,y,1]) == tuple else [255,255,255]
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
    i = 0
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
                if type(pts[x,y,0]) == tuple:
                    for z in pts[x,y,0]:
			
			#if(i<len(pts[x,y,0])):
			#	z = t[i]
			#	print "\n z  ",z
			#		i+=1
                        #z = pts[x,y,0]
                        #print z
			#print "\n Type of depth element: ",type(z)
			sp = np.matrix([[x],[y],[z]])
			
                        #sp = np.matrix(pts1[i, :]).reshape(3,1)
                        u_fp = ((f * np.transpose((sp - tf)) * i_f * Bu) / (np.transpose((sp - tf)) * k_f)) + u0
                        v_fp = ((f * np.transpose((sp - tf)) * j_f * Bv) / (np.transpose((sp - tf)) * k_f)) + v0
                        x_projected = u_fp[0,0]
                        y_projected = v_fp[0,0]
                        if type(new_pts[x,y,2]) == list:
                            new_pts[x,y,2].append((x_projected, y_projected))
                        else:
                            new_pts[x,y,2] = [(x_projected, y_projected)]
        draw_image(new_pts, "frame_2%d.png" % frame)
        print "Save frame_2%d.png" % frame

def get_cam_position(angle = -np.pi/6, no_frames = 4, cam_original_position = [0,100,100,-5 * 100]):
    """ Return camera position for frame 2-4 using quaternion maths """
    cam_position = []
    cam_position.append(cam_original_position)
    q = [math.cos(angle/2), math.sin(angle/2), 0, 0]
    q_conj = conjugate(q)
    # print "Quaternion rotation:", q
    # print "Q prime:", q_conj
    for i in range(0, no_frames):
        new_cam = quatmult(quatmult(q,cam_position[-1]), q_conj)
        cam_position.append(new_cam)
    return cam_position

def get_cam_orientation(angle = np.pi/6, no_frames = 4, cam_original_orientation = np.matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])):
    """ Return camera orientation """
    q_cam = [math.cos(angle/2), math.sin(angle/2),0, 0]
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
