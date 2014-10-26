import sys
from PyQt4 import QtCore, QtGui, uic
 
form_class = uic.loadUiType("ImageLoader.ui")[0]

x = 0.0
y = 0.0
curr_x = 0
curr_y = 0
numberOfPoints = 0
count = 0
setsOfPoints = []
listOfSetsOfPoints = []
class ImageLoad(QtGui.QMainWindow, form_class):
	def __init__(self, parent=None):
		QtGui.QMainWindow.__init__(self, parent)
	        self.setupUi(self)
		self.loadImg_btn.clicked.connect(self.loadImageOnClick)
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

	#Function to load image into Pixmap.
	def loadImageOnUI(self,filename):
		pixmap = QtGui.QPixmap(filename)
		return pixmap
		
	


	#Function to load the image once selected from open dialog box
	def loadImageOnClick(self):
		global x
		global y
		filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File', '.') 		#Open file dialog box

#		self.label.setScaledContents(True);
#		label_width = self.label.width()
#		label_height = self.label.height()
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

		self.label_5.setVisible(True)
		curr_x = event.pos().x()
		curr_y = event.pos().y()
		self.label_x.setText(str(curr_x))
		self.label_y.setText(str(curr_y))
		#self.drawPoint(curr_x,curr_y)
		
		numberOfPoints = int(self.numberOfPoints_text.toPlainText())
		
		setsOfPoints.append((curr_x,curr_y))
		count += 1
		if(count == numberOfPoints):
			self.initPointSelection_btn.setVisible(True)
			count = 0

				

	

	#Function to enable text box to input number of points to be entered
	def makeVisibleNumberOfPointsInput(self):
		self.numberOfPoints_label.setVisible(True)
		self.numberOfPoints_text.setVisible(True)

		
	#Function to receive the "number of points" value from the text box :: BTN "Select Points clicked on the Image"
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
		setsOfPoints = [] 				#Reinitializing sub-list setsOfPoints for next selection
	
	

	#Function to draw circle at pixel clicked by user
	def drawPoints(self, qp):
		global curr_x
		global curr_y
		qp.setPen(QtCore.Qt.red)
	        #size = self.size()
		qp.drawPoint(curr_x, curr_y)

	def paintEvent(self, event):

		qp = QtGui.QPainter()
	        qp.begin(self)
		self.drawPoints(qp)
		
	#Function to enter depth of the selected points  BTN::enterDepth_btn
	def getDepthUserInput(self):

		depth, ok = QtGui.QInputDialog.getInt(self, "Depth from camera",
	        "Enter depth of the selected points", QtGui.QLineEdit.Normal, 1, 1073741824)
		if ok:
			strng = "Depth entered is : " + str(depth)
			self.label_toTest2.setText(strng)
		#else:
		#	self.label_toTest2.setText("Not able to receive depth value")
		
	
	#Function to reset all the variables and parameters to input next sets of points
	def resetAllMembers(self):
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

app = QtGui.QApplication(sys.argv)
imgLoader = ImageLoad()
imgLoader.show()
app.exec_()
