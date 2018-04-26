import sys
from PyQt5.QtWidgets import qApp, QAction, QApplication, QWidget, QGridLayout, QMainWindow
from PyQt5.QtGui import QIcon, QFont

"""
	A single SymbolTest page
"""
class SymbolTestWidget(QWidget):
	"""
	@modifies symbol_, text_context_, visual_context_, has_visual
	@effects creates a new page object with the supplied fields set to the fiven value
			 or none if the value does not work 
	"""
	def __init__(self, symbol=None, text_context=None, visual_context=None, parent):
		symbol_ = symbol_
		text_context_ = text_context
		visual_context_ = visual_context
		if(not(visual_context_) == None):
			has_visual = true
		else:
			has_visual = false
		super().__init__(parent)
		self.init_gui(parent)
	"""
	@modifes none
	@effects draws the test on the provided page, places the fields in the correct locatio
	"""
	def init_gui(self, parent):
		layout = QGridLayout()
		layout.setSpacing(10)

		self.setLayout(self.layout)
		pass

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

def generateBlankPage():
	pass

def generateResponder():
	pass

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