import sys
from PyQt5.QtWidgets import (QLabel, QTextEdit, QLineEdit, QGridLayout, QMenu, qApp, QApplication, QWidget, QMessageBox,
							 QPushButton, QToolTip, QMainWindow, QAction)
from PyQt5.QtGui import QIcon, QFont
		
class Test(QWidget):
	def __init__(self):
		super().__init__()

		self.init_UI()

	def init_UI(self):

		QToolTip.setFont(QFont('TimesNewRoman', 10))
		self.setToolTip('This is a <b>QWidget</b> widget')
 		
		grid = QGridLayout()
		grid.setSpacing(10)
		"""
		exitAct = QAction('&Exit', self)
		exitAct.setShortcut('Ctrl+Q')
		exitAct.setStatusTip('Exit application')
		exitAct.triggered.connect(qApp.quit)

		self.statusBar()
		menubar = self.menuBar()
		filemenu = menubar.addMenu('&File')
		filemenu.addAction(exitAct)
		"""
		btn = QPushButton('Button', self)
		btn.setToolTip('This is a <b>QPushBotton</b> widger')
		btn.resize(btn.sizeHint())
		
		imageBox = 

		description = QLabel('Description')
		descriptionEdit = QTextEdit("Your description here")

		grid.addWidget(description, 4, 5)
		grid.addWidget(descriptionEdit, 4, 6, 4, 1)
				
		grid.addWidget(btn, 7, 5, 1, 1)


		self.setLayout(grid)
		self.setGeometry(300, 300, 300, 250)
		self.setWindowTitle("Hello")
		self.setWindowIcon(QIcon("rubber duckie.png"))
		self.show()

	def closeEvent(self, event):
		confirm = QMessageBox.question(self, 'Message',
									   'Are you sure you want to quit?', QMessageBox.Yes | 
    									QMessageBox.No, QMessageBox.No)
		if confirm == QMessageBox.Yes:
			event.accept()
		else:
			event.ignore()

	def contextMenuEvent(self, event):
       
           cmenu = QMenu(self)
           
           newAct = cmenu.addAction("New")
           opnAct = cmenu.addAction("Open")
           quitAct = cmenu.addAction("Quit")
           action = cmenu.exec_(self.mapToGlobal(event.pos()))
           
           if action == quitAct:
               qApp.quit()
def main():
	app = QApplication(sys.argv)
	test = Test()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()