import sys
from PyQt4 import QtCore, QtGui, uic
 
form_class = uic.loadUiType("ImageLoader.ui")[0]

x = 0.0
y = 0.0
class ImageLoad(QtGui.QMainWindow, form_class):
	def __init__(self, parent=None):
		QtGui.QMainWindow.__init__(self, parent)
	        self.setupUi(self)
		self.loadImg_btn.clicked.connect(self.loadImageOnClick)
		self.label_2.setVisible(False)
		self.label_5.setVisible(False)


	def loadImageOnUI(self,filename):
		pixmap = QtGui.QPixmap(filename)
		return pixmap
		
	
#loadImg_btn

	def loadImageOnClick(self):
		global x
		global y
		filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File', '.')

		self.label.setScaledContents(True);
 		self.label.setPixmap(self.loadImageOnUI(filename))

#		image = QLabel()
#		self.image.setPixmap
#		self.image.setObjectName("image")
		self.label.mousePressEvent = self.getPos
#		self.getPos(self.label.mousePressEvent)
		#self.label.mousePressEvent(self.getPos)
		
		self.labelWidth.setText(str(self.loadImageOnUI(filename).height()))
		self.label_2.setVisible(True)
		self.labelHeight.setText(str(self.loadImageOnUI(filename).width()))
		#self.image.setPixmap(QPixmap(filename))

	def getPos(self , event):
		global x
		global y
		self.label_5.setVisible(True)
		self.label_x.setText(str(event.pos().x()))
		self.label_y.setText(str(event.pos().y()))
#		x = 
#		y = 
	

		

app = QtGui.QApplication(sys.argv)
imgLoader = ImageLoad()
imgLoader.show()
app.exec_()
