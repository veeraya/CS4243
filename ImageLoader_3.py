import sys
from PyQt4 import QtCore, QtGui, uic
 
form_class = uic.loadUiType("ImageLoader.ui")[0]


class ImageLoad(QtGui.QMainWindow, form_class):
	def __init__(self, parent=None):
		QtGui.QMainWindow.__init__(self, parent)
	        self.setupUi(self)
		self.loadImg_btn.clicked.connect(self.loadImageOnClick)
		self.label_2.setVisible(False)
		image = QLabel()
		self.image.setObjectName("image")
		self.image.mousePressEvent = self.getPos


	def loadImageOnUI(self,filename):
		pixmap = QtGui.QPixmap(filename)
		return pixmap
		
	
#loadImg_btn

	def loadImageOnClick(self):
		filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File', '.')

		self.label.setScaledContents(True);
 		self.label.setPixmap(self.loadImageOnUI(filename))
		self.labelWidth.setText(str(self.loadImageOnUI(filename).height()))
		self.label_2.setVisible(True)
		self.labelHeight.setText(str(self.loadImageOnUI(filename).width()))
		self.image.setPixmap(QPixmap(filename))

	def getPos(self , event):
	    x = event.pos().x()
	    y = event.pos().y() 

		

app = QtGui.QApplication(sys.argv)
imgLoader = ImageLoad()
imgLoader.show()
app.exec_()
