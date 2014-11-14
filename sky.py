import cv2
import numpy as np

img = cv2.imread('frame_7 2.png')
sky = cv2.imread('sky1.png')
height,width,layers = img.shape

# print img[0,0]

for x in range(235,width-270):
	for y in range(785):
		if (img[y,x] == [255,255,255]).all():
			img[y,x] = sky[y,x]
			
cv2.imwrite('result.jpg', img)