import cv2
import cv2.cv as cv

# create video
img1 = cv2.imread('1.jpg')
img2 = cv2.imread('2.jpg')
img3 = cv2.imread('3.jpg')

height,width,layers = img1.shape
codec = cv.CV_FOURCC('I', 'Y', 'U', 'V')

video = cv2.VideoWriter('video.avi',codec,25,(width,height),1)

video.write(img1)
video.write(img2)
video.write(img3)

cv2.destroyAllWindows()
video.release()