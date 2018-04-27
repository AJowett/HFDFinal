import sys
from PyQt5.QtWidgets import qApp, QAction, QApplication, QFileDialog, QGridLayout, QLabel, QMainWindow, QPushButton, QWidget
from PyQt5.QtGui import QIcon, QFont, QPixmap

"""
	A single SymbolTest page
"""
class SymbolTestWidget(QWidget):
	"""
	@modifies symbol_, text_context_, visual_context_, has_visual
	@effects creates a new page object with the supplied fields set to the fiven value
			 or none if the value does not work 
	"""
	def __init__(self,  parent, symbol=None, text_context=None, visual_context=None):
		self.symbol_ = symbol
		self.text_context_ = text_context
		self.visual_context_ = visual_context
		super().__init__(parent)
		self.init_gui(parent)

	"""
	@modifes none
	@effects draws the test on the provided page, places the fields in the correct locatio
	"""
	def init_gui(self, parent):
		layout = QGridLayout()
		layout.setSpacing(10)
		textual_label = QLabel(self)
		visual_label = QLabel(self)
		symbol_label = QLabel(self)
		
		if self.visual_context_ == None and self.text_context_ != None:
			textual_label.setText(self.text_context_)
			layout.addWidget(textual_label, 2, 5, 1, 1)

		elif self.visual_context_ == None and self.text_context_ == None:
			textual_label.setText("Add Textual Context Here")
			layout.addWidget(textual_label, 2, 5, 1, 1)
		else:
			visual_label = visual_context_

		textBtn = QPushButton("Add/Modify textual context", self)
		textBtn.setToolTip("Used to change the description of the context in which this symbol appears")
		textBtn.resize(textBtn.sizeHint())

		symbolBtn = QPushButton("Add/Change symbol", self)
		symbolBtn.setToolTip("Used to add or change the symbol on this page")
		symbolBtn.resize(symbolBtn.sizeHint())
		symbolBtn.clicked.connect(self.getfile(symbol_label))

		layout.addWidget(textBtn, 3, 5, 1, 1)
		layout.addWidget(symbolBtn, 3, 1, 1, 1)
		self.setLayout(layout)

	def getfile(self, label):
		fname = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\',"Image files (*.jpg *.png)")
		print(fname, "\n")
		label.setPixmap(QPixmap(fname[0]))

	"""
	@modifies text_context_
	@effects sets text_context_ to the provided text_context
	"""
	def add_text_context(text_context):
	 	pass 

	"""
	@modifes text_context_
	@effects reads in text from the given file
,	"""
	def add_text_context_from_file(text_file_name):
		pass
	def add_visual_context():
		pass
	def add_symbol():
		pass


class ComprehensionTestApp(QMainWindow):
	def __init__(self):
		super().__init__()
		symbol_tests = []
		self.init_gui()

	def init_gui(self):
		exitAct = QAction('&Exit', self)
		exitAct.setShortcut('Ctrl+Q')
		exitAct.setStatusTip('Exit application')
		exitAct.triggered.connect(qApp.quit)

		menu_bar = self.menuBar()
		filemenu = menu_bar.addMenu('&File')
		filemenu.addAction(exitAct)

		self.setWindowTitle("Hello")
		self.setWindowIcon(QIcon("rubber duckie.png"))
		self.showMaximized()
		self.load_blank_test()

	def load_blank_test(self):
		test = SymbolTestWidget(self)
		self.setCentralWidget(test)

def main():
	app = QApplication(sys.argv)
	test = ComprehensionTestApp()
	sys.exit(app.exec_())

	"""
	w = QWidget()
	w.resize(250, 150)
	w.move(300, 300)
	w.setWindowTitle('Simple')
	w.show()
	sys.exit(app.exec_())
	"""

if __name__ == '__main__':
	main()