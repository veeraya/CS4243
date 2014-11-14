import cv2
import cv2.cv as cv

# create video
img1 = cv2.imread('frame_0.png')

height,width,layers = img1.shape
codec = cv.CV_FOURCC('I', 'Y', 'U', 'V')

video = cv2.VideoWriter('video.avi',codec,2,(width,height),1)

for i in range(11):
	img = cv2.imread('frame_%d.png' % i)
	video.write(img)

cv2.destroyAllWindows()
video.release()