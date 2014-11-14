import sys
from PyQt4 import QtCore, QtGui, uic
import numpy as np
import matplotlib.path as mpPath
import cv2 as cv
from tempfile import TemporaryFile
import pickle

 
form_class = uic.loadUiType("ImageLoader.ui")[0]
img = cv.imread("project.jpeg")

x = 0.0
y = 0.0
curr_x = 0
curr_y = 0
numberOfPoints = 0			#number of points selected - value is visible in the output text file
count = 0
setsOfPoints = []			#A local list to hold the pixels selected for individual structures at a time.
listOfSetsOfPoints = []
numberOfBuildingSelected = 1
enteredDepth = 0
listBuildingPointsWithDepth = []	#stores pixel of building selected and corresponding depth entered
listSkyGrassWithDepth = []		#stores pixel of Sky or Grass selected and corresponding depth entered
skyOrGrassDone = 0
pixmap_2 = 0
listPixelWDepth = [] 			#List to hold all pixels and correspoding depth
mat_allPixelWDepth = np.ones((img.shape[1],img.shape[0],3),dtype = object) 	

					#Matrix to store depth for corresponding pixel

selectionOption = ["Buildings - front face", "Building - no side face","Building - no side face (H)", "Building - no side face (Slant)", "Building - partial side face  RtoL","Building - partial side face  LtoR",  "Grass","Sky"]

class ImageLoad(QtGui.QMainWindow, form_class):
	def __init__(self, parent=None):
		global selectionOption
		QtGui.QMainWindow.__init__(self, parent)
	        self.setupUi(self)
		self.loadImg_btn.clicked.connect(self.loadImageOnClick)
		#self.scrollAreaMainWindow.setWidget(self.centralwidget)	
		self.label_2.setVisible(False)
		self.label_5.setVisible(False)
		self.numberOfPoints_label.setVisible(False)
		self.numberOfPoints_text.setVisible(False)
		self.initPointSelection_btn.setVisible(False)
		self.enterDepth_btn.setVisible(False)
		self.inputDepth_btn.clicked.connect(self.makeVisibleNumberOfPointsInput)
		self.initPointSelection_btn.clicked.connect(self.getNumberOfPointsInput)
		self.label.mousePressEvent = self.getPos		#this gets the position of mousePress over label.
		self.enterDepth_btn.clicked.connect(self.getDepthUserInput)
		self.reset_btn.clicked.connect(self.resetAllMembers)
		self.reset_btn.setToolTip('To reset all members of this form')
		self.optionsList.addItems(selectionOption)
		self.skyGrassCheck.setVisible(False)


	#Function to load image into Pixmap.
	def loadImageOnUI(self,filename):
		pixmap = QtGui.QPixmap(filename)
		return pixmap
		
	


	#Function to load the image once selected from open dialog box
	def loadImageOnClick(self):
		global x
		global y
		global pixmap_2
		filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File', '.') 		#Open file dialog box

		#pixmap_2 = (self.loadImageOnUI(filename)).scaled(label_width,label_height)
		pixmap_2 = self.loadImageOnUI(filename)			#loading image into pixmap that is selected from open dialog box
		self.label.width = pixmap_2.width()			#Setting width x height of label (where image is shown) as the
		self.label.height = pixmap_2.height() 			#width x height of the image
		self.scrollArea.setWidget(self.label)			#setting label inside the scrollArea
		self.label.setPixmap(pixmap_2)				#making image to be visible on the label.

		##Here we are only getting the image's size.									
		self.labelWidth.setText(str(pixmap_2.height()))
		self.labelHeight.setText(str(pixmap_2.width()))
		self.label_2.setVisible(True)

	
	#Function to get position of click of mouse over the image
	def getPos(self , event):
		global x
		global y
		global numberOfPoints
		global setsOfPoints

		global count 
		global curr_x
		global curr_y
		global pixmap_2

		self.label_5.setVisible(True)
		curr_x = event.pos().x()
		curr_y = event.pos().y()
		self.label_x.setText(str(curr_x))
		self.label_y.setText(str(curr_y))
		#self.drawPoint(curr_x,curr_y)
		
		numberOfPoints = int(self.numberOfPoints_text.toPlainText())
		
		if self.numberOfPoints_text.isVisible():
			
			setsOfPoints.append((curr_x,curr_y))
			count += 1
			if(count == numberOfPoints):
				self.initPointSelection_btn.setVisible(True)
				count = 0

				
		img = QtGui.QImage(pixmap_2.toImage())			##Showing a dot for every click on the image
		img.setPixel(curr_x,curr_y,255)				#
		pixmap_2 = pixmap_2.fromImage(img)			#
		self.label.setPixmap(pixmap_2)				#
	

	#Function to enable text box to input number of points to be entered
	def makeVisibleNumberOfPointsInput(self):
		self.numberOfPoints_label.setVisible(True)
		self.numberOfPoints_text.setVisible(True)

		
	#Function to receive the "number of points" value from the text box and read the pixels
	# selected on the image  :: BTN "Select Points clicked on the Image"
	def getNumberOfPointsInput(self):
		
		global numberOfPoints
		global listOfSetsOfPoints
		global setsOfPoints
		
		if ((numberOfPoints is None) or numberOfPoints == 0):
			
			QtGui.QMessageBox.critical(self, "Error", "You need to enter number of points first")
			return
			 
		
		#self.label_toTest.setText(str(numberOfPoints))
		self.enterDepth_btn.setVisible(True)
		listOfSetsOfPoints.append(setsOfPoints)
		self.label_toTest.setText(str(listOfSetsOfPoints))
		
	
	


	def paintEvent(self, event):
		qp = QtGui.QPainter()
	        qp.begin(self)
		self.drawPoints(qp)
		

	#Function to draw circle at pixel clicked by user
	def drawPoints(self, qp):
		global curr_x
		global curr_y
		qp.setPen(QtCore.Qt.red)
	        #size = self.size()
		qp.drawPoint(curr_x, curr_y)

	

	
	#Function to enter depth of the selected points  BTN::enterDepth_btn
	def getDepthUserInput(self):
		global enteredDepth
		global listBuildingPointsWithDepth
		global numberOfBuildingSelected
		global setsOfPoints
		global skyOrGrassDone
		selectedOption = self.optionsList.currentText()
		depth, ok = QtGui.QInputDialog.getInt(self, "Depth from camera",
	        "Enter depth of the selected points", QtGui.QLineEdit.Normal, -1073741824, 1073741824)

		enteredDepth = depth;

		#Appending details of user input data to a list. This will contain identifier of building, points selected for that 
		#building and the depth input.

		if(selectedOption == "Buildings - front face"):
										#not self.skyGrassCheck.isChecked()):
			print "Selected option is Buildings - front face\n"						
			QtGui.QMessageBox.critical(self, "Warning", "sets of points just selected "+str(setsOfPoints))
			temp = [numberOfBuildingSelected,setsOfPoints,enteredDepth]
			QtGui.QMessageBox.critical(self, "Warning", "This depth will be applied to all the pixels lying on the selected face of the building")
			listBuildingPointsWithDepth.append(temp)
			numberOfBuildingSelected += 1

		elif(selectedOption == 'Building - no side face'):
			length, ok = QtGui.QInputDialog.getInt(self, "Length of the side wall",
		        "Enter expected length of the wall currently not visible", QtGui.QLineEdit.Normal, 1, 1073741824)
			temp = [str(selectedOption),setsOfPoints,enteredDepth,length]
			QtGui.QMessageBox.critical(self, "Warning", "This depth will be used to assign depth to all the pixels of the hidden wall")
			listBuildingPointsWithDepth.append(temp)

#Building - no side face (H)
		elif(selectedOption == "Building - no side face (H)"):
			length, ok = QtGui.QInputDialog.getInt(self, "Length of the side wall",
		        "Enter expected length of the wall currently not visible", QtGui.QLineEdit.Normal, 1, 1073741824)
			temp = [str(selectedOption),setsOfPoints,enteredDepth,length]
			QtGui.QMessageBox.critical(self, "Warning", "This depth will be used to assign depth to all the pixels of the hidden wall")
			listBuildingPointsWithDepth.append(temp)

		elif(selectedOption == "Building - no side face (Slant)"):
			length, ok = QtGui.QInputDialog.getInt(self, "Length of the side wall",
		        "Enter expected length of the wall currently not visible", QtGui.QLineEdit.Normal, 1, 1073741824)
			temp = [str(selectedOption),setsOfPoints,enteredDepth,length]
			QtGui.QMessageBox.critical(self, "Warning", "This depth will be used to assign depth to all the pixels of the hidden Slant wall")
			listBuildingPointsWithDepth.append(temp)

		elif(selectedOption == "Building - partial side face  RtoL"):
			length, ok = QtGui.QInputDialog.getInt(self, "Length of the side wall",
		        "Enter length of the side wall", QtGui.QLineEdit.Normal, 1, 1073741824)
						
			temp = [str(selectedOption),setsOfPoints,enteredDepth,length]
			QtGui.QMessageBox.critical(self, "Warning", "This depth will be used to assign depth to all the pixels that will be visible as the camera moves")
			listBuildingPointsWithDepth.append(temp)

#"Building - partial side face  LtoR"
		elif(selectedOption == "Building - partial side face  LtoR"):
			length, ok = QtGui.QInputDialog.getInt(self, "Length of the side wall",
		        "Enter length of the side wall", QtGui.QLineEdit.Normal, 1, 1073741824)
						
			temp = [str(selectedOption),setsOfPoints,enteredDepth,length]
			QtGui.QMessageBox.critical(self, "Warning", "This depth will be used to assign depth to all the pixels that will be visible as the camera moves")
			listBuildingPointsWithDepth.append(temp)


		elif(selectedOption != 'Sky' or selectedOption != 'Grass'):
			skyOrGrassDone+=1
			temp = [str(selectedOption),setsOfPoints,enteredDepth]
			listSkyGrassWithDepth.append(temp)		
		
		if (len(listSkyGrassWithDepth) != 0):
			QtGui.QMessageBox.critical(self, "Warning", "Points entered for Sky and/or Grass are  "+str(listSkyGrassWithDepth))
			
		
		if ok:
			strng = "Depth entered is : " + str(depth)
			self.label_toTest2.setVisible(True)
			self.label_toTest2.setText(str(listBuildingPointsWithDepth))
			setsOfPoints = [] 				#Reinitializing sub-list setsOfPoints for next selection
		
		
		
		



	def closeEvent(self, event):

		global listBuildingPointsWithDepth
		global listSkyGrassWithDepth
		global mat_allPixelWDepth
		print str(self.optionsList.currentText())
		print "\n Close event called"
		print "\nlistBuildingPointsWithDepth : ",listBuildingPointsWithDepth
		print "\nlistSkyGrassWithDepth",listSkyGrassWithDepth
		if(len(listSkyGrassWithDepth) != 0):
			combinedList = listBuildingPointsWithDepth
			for i in range(len(listSkyGrassWithDepth)):
				combinedList.append(listSkyGrassWithDepth[i])

			self.getBuildingPixelsWDepth(combinedList)
		
		elif(len(listSkyGrassWithDepth) == 0):
			self.getBuildingPixelsWDepth(listBuildingPointsWithDepth)
		
		output = open('data.pkl', 'wb')
		pickle.dump(mat_allPixelWDepth, output)
		output.close()
		#f = open("PixelandDepth.txt","w")
		#f.write("Building/structure points : "+str(listBuildingPointsWithDepth)+"\n")
		#f.write("Sky or Front Grass : "+str(listSkyGrassWithDepth)+"\n")
		#f.close	



	##Function to read the list of building vertices with depths and apply that depth to all the pixels of that face of the building
	def getBuildingPixelsWDepth(self,listWDepth):
		global mat_allPixelWDepth
		global listBuildingPointsWithDepth
		#listWDepth = listBuildingPointsWithDepth
		global listPixelWDepth			#This list holds all the pixels of a plane for which points has been selected
		
		print "\nList received inside getBuildingPixelsWDepth function is : ",listWDepth

		for i in range(len(listWDepth)):
			
			depth = listWDepth[i][2]
			list_x = self.getListX(listWDepth[i][1])			##Need to define functions getListX / Y
			list_y = self.getListY(listWDepth[i][1])

			min_x = min(list_x)
			min_y = min(list_y)
			max_x = max(list_x)
			max_y = max(list_y)
			#if (str(listWDepth[i][0]) != "Building - no side face (Slant)"):
			buildingShapeArray = np.zeros((len(listWDepth[i][1])+1,2))
			#if (str(listWDepth[i][0]) == "Building - no side face (Slant)"):
			#	buildingShapeArray = np.zeros((len(listWDepth[i][1]),2))
			
			for j in range(len(listWDepth[i][1])+1):
				if (j <= (len(listWDepth[i][1]) - 1)):
					buildingShapeArray[j][0] = listWDepth[i][1][j][0]
					buildingShapeArray[j][1] = listWDepth[i][1][j][1]
				
				elif (j == len(listWDepth[i][1])):# and str(listWDepth[i][0]) != "Building - no side face (Slant)"):
					buildingShapeArray[j][0] = listWDepth[i][1][0][0]
					buildingShapeArray[j][1] = listWDepth[i][1][0][1]

		
			p = min_x
			q = min_y
			poly = mpPath.Path(buildingShapeArray,codes=None,closed=True)
			##OPTIMIZATION: No need to make a seperate list of points. We can directly assign depths to the matrix

			if(len(str(listWDepth[i][0])) < 3):	
				depth_int = depth
				depth = (depth_int,)
# str(listWDepth[i][0]) != "Sky" and str(listWDepth[i][0]) != "Grass"):			
				print "Setting pixels for front face\n"
				for p in range(min_x,max_x,1):
					for q in range(min_y,max_y,1):
						point = (p,q)
						isPointInside = bool(poly.contains_point(point,transform=None,radius=0.0))
						
						if isPointInside:
							listPixelWDepth.append([point,depth])
							mat_allPixelWDepth[p,q,0] = depth 
			elif(str(listWDepth[i][0]) == "Building - no side face"):
				print "Setting pixels for face that is not visible\n"
				depth_int = depth
				depth = (depth_int,)
				length = listWDepth[i][3]
				for q in range(min_y,max_y):
					point = (min_x,q)
					for i in range(1,length):
						depth = depth + ((depth_int+i),)	#making the tuple that holds multiple depths
					listPixelWDepth.append([point,depth])
					mat_allPixelWDepth[min_x,q,0] = depth 
					depth = ()
					print "mat_allPixelWDepth[min_x,q,0] : ",mat_allPixelWDepth[min_x,q,0]

#Building - no side face (H)

			elif(str(listWDepth[i][0]) == "Building - no side face (H)"):
				print "Setting pixels for horizontal face that is not visible\n"
				depth_int = depth
				depth = (depth_int,)
				length = listWDepth[i][3]
				for p in range(min_x,max_x):
					point = (p,min_y)
					for i in range(1,length):
						depth = depth + ((depth_int+i),)	#making the tuple that holds multiple depths
					listPixelWDepth.append([point,depth])
					mat_allPixelWDepth[min_x,q,0] = depth 
					depth = ()
					print "mat_allPixelWDepth[min_x,q,0] : ",mat_allPixelWDepth[min_x,q,0]


			elif(str(listWDepth[i][0]) == "Building - no side face (Slant)"):
				print "Setting pixels for SLANTED face that is not visible\n"
				print "Min_x : ",min_x
				print "Max_x : ",max_x
				print "Min_y : ",min_y
				print "Max_y : ",max_y
				print "buildingShapeArray: ",buildingShapeArray
				length = listWDepth[i][3]
				depth_int = depth
				depth = (depth_int,)
				for p in range(min_x,max_x,1):
					for q in range(min_y,max_y,1):
						point = (p,q)
						isPointOnLine = bool(poly.contains_point(point,transform=None,radius=0.0))
						if(isPointOnLine):
							print "\nPoint on the line found"
							for i in range(1,length):
								depth = depth + (depth_int+i,)	#making the tuple that holds multiple depths
							listPixelWDepth.append([point,depth])
							mat_allPixelWDepth[p,q,0] = depth 
							depth = ()
						#print "mat_allPixelWDepth[min_x,q,0] : ",mat_allPixelWDepth[min_x,q,0]
			
			elif(str(listWDepth[i][0]) == "Building - partial side face  RtoL"):
				length = listWDepth[i][3]
				print "Setting pixels for face that is partially visible\n"
				depth_int = depth
#				depth = (depth_int,)
				depth = ()
				alpha = int(round(length/(max_x - min_x)))

				for p in range(max_x,min_x,-1):
					for q in range(min_y,max_y,1):
						point = (p,q)
						isPointInside = bool(poly.contains_point(point,transform=None,radius=0.0))
						
						if isPointInside:
							#m = max_x - p
							for j in range(alpha+1):
								depth = depth + (depth_int+j,)
							depth_int = alpha + depth_int
							#depth = (depth_int+2*m-1, depth_int+2*m)
							listPixelWDepth.append([point,depth])
							mat_allPixelWDepth[p,q,0] = depth
							#print "\nDepth applied to point ",p," -- ",q," is ",mat_allPixelWDepth[p,q,0]
							depth = ()
			#"Building - partial side face  LtoR"
			elif(str(listWDepth[i][0]) == "Building - partial side face  LtoR"):
				length = listWDepth[i][3]
				print "Setting pixels for face that is partially visible\n"
				depth_int = depth
#				depth = (depth_int,)
				depth = ()
				alpha = int(round(length/(max_x - min_x)))

				for p in range(min_x,max_x,1):
					for q in range(min_y,max_y,1):
						point = (p,q)
						isPointInside = bool(poly.contains_point(point,transform=None,radius=0.0))
						if isPointInside:
							#m = max_x - p
							for j in range(alpha+1):
								depth = depth + (depth_int+j,)
							depth_int = alpha + depth_int
							#depth = (depth_int+2*m-1, depth_int+2*m)
							listPixelWDepth.append([point,depth])
							mat_allPixelWDepth[p,q,0] = depth
							#print "\nDepth applied to point ",p," -- ",q," is ",mat_allPixelWDepth[p,q,0]
							depth = ()


			elif(str(listWDepth[i][0]) == 'Sky' or str(listWDepth[i][0]) == 'Grass'):
				print "Setting pixels for Sky or Grass\n"
				depth_int = depth
				depth = (depth_int,)
				d = 0
				for p in range(min_y,max_y,1):
					for q in range(min_x,max_x,1):
						point = (q,p)
						isPointInside = bool(poly.contains_point(point,transform=None,radius=0.0))
						if isPointInside:
							depth = (depth_int - d,depth_int - d+1)			#depth = (depth_int + max_y-p,)
							listPixelWDepth.append([point,depth])
							mat_allPixelWDepth[q,p,0] = depth

					d+=1
		
		
		#f1 = open("BuildingShape.txt","w")
		#f1.write("Building Shape array : "+str(buildingShapeArray)+"\n")
		

		#self.toTestPixelSelection(listPixelWDepth)

		#f = open("AllPixelsWDepth.txt","w")
		#f.write("min_x : "+str(min_x)+"\n")
		#f.write("min_y : "+str(min_y)+"\n")
		#f.write("max_x : "+str(max_x)+"\n")
		#f.write("max_y : "+str(max_y)+"\n")

		#f.write("List Pixel with Depth -- the input to the function : "+str(listWDepth)+"\n")


#		f.write("Building/structure points : "+str(listPixelWDepth)+"\n")
		#f.write("Depth at pixel 739 x 825 : "+str(mat_allPixelWDepth[739,825,0])+"\n\n")
		#f.write("Building/structure points : "+str(mat_allPixelWDepth)+"\n")
		#f.write("\n Length of list  : "+str(len(listPixelWDepth)))
	

	
	#Function to reset all the variables and parameters to input next sets of points
	def resetAllMembers(self):
	
		global numberOfBuildingSelected
		global enteredDepth
		global listBuildingPointsWithDepth
		global skyOrGrassDone
		self.label_5.setVisible(False)					## Re-initializing the UI as it was
		self.numberOfPoints_label.setVisible(False)			## right after loading the photo
		self.numberOfPoints_text.setVisible(False)			##
		self.initPointSelection_btn.setVisible(False)
		self.enterDepth_btn.setVisible(False)
		self.label_toTest.setText("")
		self.label_toTest2.setText("")
		self.label_x.setText("")
		self.label_y.setText("")
		self.numberOfPoints_text.clear()

		if skyOrGrassDone == 2:
				self.skyGrassCheck.setEnabled(False)
				self.skyGrassCheck.setCheckState(0)
				selectionOption_2 = []
				self.optionsList.addItems(selectionOption_2)
				selectionOption_2 = ["Buildings - front face", "Building - no side face","Building - no side face (H)" , "Building - no side face (Slant)","Building - partial side face  RtoL", "Building - partial side face  LtoR"]
				self.optionsList.addItems(selectionOption_2)

		
		


	#Function to get list of only X coordinates out of a given list of Points(x,y)
	def getListX(self,listPoints):
		list_x = []
		for i in range(len(listPoints)):
			list_x.append(listPoints[i][0])
		return list_x


	#Function to get list of only Y coordinates out of a given list of Points(x,y)
	def getListY(self,listPoints):
		list_y = []
		for i in range(len(listPoints)):
			list_y.append(listPoints[i][1])
		return list_y

	
	#Function to test how points are getting selected
	def toTestPixelSelection(self, pixelWDepth):
		global mat_allPixelWDepth
		img = cv.imread('project.jpeg')
		for i in range(mat_allPixelWDepth.shape[0]):
			for j in range(mat_allPixelWDepth.shape[1]):
				if(mat_allPixelWDepth[i,j,0] != 1):
					img[j][i] = 0

		cv.imwrite('project_selected_Pixels.jpeg',img)
	

app = QtGui.QApplication(sys.argv)
imgLoader = ImageLoad()
imgLoader.show()
app.exec_()


#To return the matrix for all pixels and depths
def returnMatrix():
	global mat_allPixelWDepth

	return imgLoader.mat_allPixelWDepth

