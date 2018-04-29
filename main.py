import sys, os
from PyPDF2 import PdfFileReader
from PyQt5.QtWidgets import qApp, QAction, QApplication, QFileDialog, QGridLayout, QInputDialog, QLabel, QLineEdit, QMainWindow, QPushButton, QStackedWidget, QTextEdit, QWidget
from PyQt5.QtGui import QIcon, QFont, QPainter, QPen, QPixmap, QTextDocument
from PyQt5.QtPrintSupport import QPrinter
from PyQt5 import QtCore

"""
	A single SymbolTest page
"""
class SymbolTestWidget(QWidget):
	"""
	@modifies symbol_, text_context_, visual_context_, has_visual
	@effects creates a new page object with the supplied fields set to the fiven value
			 or none if the value does not work 
	"""
	def __init__(self,  parent, symbol=None, text_context=None, visual_context=None, comp_questions=[], pageNumber=0, pageTotal=0):
		self.parent_ = parent
		self.symbol_ = symbol
		self.text_context_ = text_context
		self.visual_context_ = visual_context
		super().__init__(parent)
		self.questions = comp_questions

		self.symbol_label = QLabel(self)
		self.page_label = QLabel(self)
		self.textual_label = QLabel(self)
		self.textual_edit = QTextEdit(self)
		self.visual_label = QLabel(self)

		self.layout = QGridLayout()
		self.setLayout(self.layout)

		self.page = pageNumber
		self.numPages = pageTotal
		self.init_gui(parent)


	"""
	@modifes none
	@effects draws the test on the provided page, places the fields in the correct locatio
	"""
	def init_gui(self, parent):
		#self.setFixedHeight(800)
		#self.setFixedWidth(800)
		self.layout.setSpacing(5)

		if self.symbol_ != None:
			pic = QPixmap(self.symbol_)
			pic = pic.scaled(350, 350);
			self.symbol_label.setPixmap(pic)
		else:
			pic = QPixmap("blank image.png")
			pic = pic.scaled(350, 350)
			self.symbol_label.setPixmap(pic)

		self.layout.addWidget(self.symbol_label, 6, 1, 3, 5)

		self.page_label.setText("<b>Page " + str(self.page) + "/" + str(self.numPages) + "</b>")
		self.layout.addWidget(self.page_label, 0, 10, 1, 1)

		if self.visual_context_ == None and self.text_context_ != None:
			self.textual_label.setText("<b>Context:</b>")
			self.textual_edit.setText(self.text_context_)
			self.layout.addWidget(self.textual_label, 6, 7)
			self.layout.addWidget(self.textual_edit, 7, 7, 1, 1)

		elif self.visual_context_ == None and self.text_context_ == None:
			self.textual_label.setText("<b>Context:</b>")
			self.layout.addWidget(self.textual_label, 6, 7)
			self.layout.addWidget(self.textual_edit, 7, 7, 1, 1)

			visual_contextBtn = QPushButton("Add Visual Context", self)
			visual_contextBtn.setToolTip("Used to add or change the image that provides context for the symbol")
			visual_contextBtn.clicked.connect(self.open_visual)
			self.layout.addWidget(visual_contextBtn, 9, 7, 1, 1)
		
		else:
			pic = QPixmap(self.visual_context_)
			pic = pic.scaled(350, 350)
			self.visual_label.setPixmap(pic)
			self.layout.addWidget(visual_label, 6, 7, 2, 2)

		symbolBtn = QPushButton("Add Symbol", self)
		symbolBtn.setToolTip("Used to add or change the symbol on this page")
		symbolBtn.resize(symbolBtn.sizeHint())
		symbolBtn.clicked.connect(self.open_symbol)
		self.layout.addWidget(symbolBtn, 9, 1, 1, 1)

		counter = 13
		for question in self.questions:
			qBox = QLineEdit(self)
			qNumbering = QLabel(self)
			qBox.setText(question)
			qNumbering.setText("Question " + str(counter - 12) + ":")
			self.layout.addWidget(qNumbering, counter, 1, 1, 1)
			self.layout.addWidget(qBox, counter, 2, 1, 1)
			counter += 1
	"""
	@modifes self.symbol_label
	@effects opens an image file and sets symbol_label to have that image
	"""
	def open_symbol(self):
		fname = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\',"Image files (*.jpg *.png)")
		if fname != ('', ''):
			pic = QPixmap(fname[0])
			pic = pic.scaled(350, 350)
			self.symbol_ = fname[0]
			self.symbol_label.setPixmap(pic)
		elif fname == ('', '') and self.symbol_ == None:
			pic = QPixmap("blank image.png") 
			pic = pic.scaled(350, 350)
			self.symbol_label.setPixmap(pic)

	def open_visual(self):
		fname = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\',"Image files (*.jpg *.png)")
		if fname != ('', ''):
			pic = QPixmap(fname[0])
			pic = pic.scaled(350, 350)
			self.visual_label.setPixmap(pic)
			if self.visual_context_ == None:
				self.textual_edit.hide()
				self.textual_label.hide()
				self.layout.addWidget(self.visual_label, 1, 1, 4, 5)
			
			self.visual_context_ = fname[0]

	def get_page(self):
		return str(self.page)

	def get_numPages(self):
		return self.numPages

	def set_page(self, pageNum):
		self.page = pageNum
		self.page_label.setText("<b>Page " + str(self.page) + "/" + str(self.numPages) + "</b>")

	def set_numPages(self, pageTotal):
		self.numPages = pageTotal
		self.page_label.setText("<b>Page " + str(self.page) + "/" + str(self.numPages) + "</b>")

	def set_symbol(self, symbol):
		self.symbol_ = symbol
		pic = QPixmap(symbol)
		pic = pic.scaled(350, 350)
		self.symbol_label.setPixmap(pic)

	def get_symbol(self):
		return self.symbol_label.pixmap()
	def get_context(self):
		return str(self.textual_edit.toPlainText())
	def get_question1(self):
		return str(self.questions[0])
	def get_question2(self):
		return str(self.questions[1])
	def has_visual_context(self):
		if self.visual_context_ != None:
			return True
		return False
	def get_visual_context(self):
		return self.visual_label.pixmap()

class ComprehensionTestApp(QMainWindow):
	def __init__(self):
		super().__init__()
		self.symbol_tests = QStackedWidget()
		self.question1 = "Exactly what do you think this symbol means?"
		self.question2 = "What action would you take in response to this symbol?"
		self.init_gui()

	def init_gui(self):
		exitAct = QAction('&Exit', self)
		exitAct.setShortcut('Ctrl+Q')
		exitAct.setStatusTip('Exit application')
		exitAct.triggered.connect(qApp.quit)

		saveAct = QAction('&Save as PDF', self)
		saveAct.setShortcut('Ctrl+S')
		saveAct.setStatusTip('Saves as PDF')
		saveAct.triggered.connect(self.save_as_pdf)

		importAct = QAction('&Import symbols', self)
		importAct.setShortcut('Ctrl+I')
		importAct.setStatusTip('Imports all the specified images on to their own test page')
		importAct.triggered.connect(self.import_symbols)

		menu_bar = self.menuBar()
		filemenu = menu_bar.addMenu('&File')
		filemenu.addAction(importAct)
		filemenu.addAction(saveAct)
		filemenu.addAction(exitAct)

		newQuestAct = QAction('&Change default questions', self)
		newQuestAct.setStatusTip('Changes the default questions asked about the symbol')
		newQuestAct.triggered.connect(self.change_questions)

		moveLeftAct = QAction('&Move current page left', self)
		moveLeftAct.setShortcut('Ctrl+,')
		moveLeftAct.setStatusTip('Moves the current page one page to the left')
		moveLeftAct.triggered.connect(self.move_test_left)

		moveRightAct = QAction('&Move current page right', self)
		moveRightAct.setShortcut('Ctrl+.')
		moveRightAct.setStatusTip('Moves the current page one page to the right')
		moveRightAct.triggered.connect(self.move_test_right)

		editmenu = menu_bar.addMenu('&Edit')
		editmenu.addAction(newQuestAct)
		editmenu.addAction(moveLeftAct)
		editmenu.addAction(moveRightAct)

		nextAct = QAction(QIcon("next.png"), 'Next page (Ctrl+L)', self)
		nextAct.setShortcut('Ctrl+L')
		nextAct.setStatusTip('Goes to the next page')
		nextAct.triggered.connect(self.next_page)

		prevAct = QAction(QIcon("prev.png"), "Previous page (Ctrl+K)", self)
		prevAct.setShortcut('Ctrl+K')
		prevAct.setStatusTip('Goes to the previous page')
		prevAct.triggered.connect(self.prev_page)

		newAct = QAction(QIcon("add.png"), "Add a new page (Ctrl+N)", self)
		newAct.setShortcut('Ctrl+N')
		newAct.setStatusTip('Creates a new page')
		newAct.triggered.connect(self.add_blank_test)

		remAct = QAction(QIcon("remove.png"), "Delete page (Ctrl+R)", self)
		remAct.setShortcut('Ctrl+R')
		remAct.setStatusTip('Deletes the current page')
		remAct.triggered.connect(self.delete_test)

		tool_bar = self.addToolBar("Next Page")
		tool_bar.addAction(prevAct)
		tool_bar.addAction(nextAct)
		tool_bar.addAction(newAct)
		tool_bar.addAction(remAct)

		self.setWindowTitle("Open Comprehension Test Generator")
		self.setWindowIcon(QIcon("rubber duckie.png"))
		self.setGeometry(500, 500, 500, 450)
		self.add_blank_test()
		self.setCentralWidget(self.symbol_tests)

		self.show()

	def add_blank_test(self):
		page = self.symbol_tests.count() + 1
		test = SymbolTestWidget(self, comp_questions=[self.question1, self.question2], pageNumber=page, pageTotal=page)
		self.symbol_tests.addWidget(test)
		self.symbol_tests.setCurrentIndex(page - 1)

	def add_test(self):
		page = self.symbol_tests.count() + 1
		test = SymbolTestWidget(self, comp_questions=[self.question1, self.question2], pageNumber=page, pageTotal=page)
		self.symbol_tests.addWidget(test)
		self.symbol_tests.setCurrentIndex(page - 1)

	def next_page(self):
		if self.symbol_tests.currentIndex() < self.symbol_tests.count() - 1:
			self.symbol_tests.setCurrentIndex(self.symbol_tests.currentIndex() + 1)
			self.symbol_tests.currentWidget().set_numPages(self.symbol_tests.count())

	def prev_page(self):
		if self.symbol_tests.currentIndex() > 0:
			self.symbol_tests.setCurrentIndex(self.symbol_tests.currentIndex() - 1)
			self.symbol_tests.currentWidget().set_numPages(self.symbol_tests.count())

	def save_as_pdf(self):
		global TEMPLATE
		filename = QFileDialog.getSaveFileName(self, 'Save to PDF', 'c:\\',"*.pdf")
		print(filename)

		if filename != ('', ''):
			if os.path.exists(filename[0]):
				#os.remove(filename[0])
				infile = PdfFileReader(filename[0], 'rb')

				if infile.getNumPages() == 0:
					doc = QTextDocument()
					doc.print(printer)

			printer = QPrinter()
			printer.setPageSize(QPrinter.A4)
			printer.setOutputFormat(QPrinter.PdfFormat)
			printer.setOutputFileName(filename[0])
			
			painter = QPainter()
			font = QFont("times")
			font.setPointSize(12)
			painter.begin(printer)
			painter.setFont(font)

			for i in range(0, self.symbol_tests.count()):
				cur_symbol_test = self.symbol_tests.widget(i)
				
				if cur_symbol_test.has_visual_context() == False:
					pixmap = cur_symbol_test.get_symbol()
					pixmap = pixmap.scaled(350, 350)
					painter.drawPixmap(30, 100, pixmap)
					painter.drawText(750, 20, cur_symbol_test.get_page())
					painter.drawText(420, 200, 350, 400, QtCore.Qt.TextWordWrap, "Context: " + cur_symbol_test.get_context())
					painter.drawText(30, 600, cur_symbol_test.get_question1())
					painter.drawText(30, 830, cur_symbol_test.get_question2())

					cur_pen = painter.pen()
					line_pen = QPen()
					line_pen.setWidth(2)
					painter.setPen(line_pen)
					painter.drawLine(70, 656, 600, 656)
					painter.drawLine(70, 712, 600, 712)
					painter.drawLine(70, 768, 600, 768)

					painter.drawLine(70, 886, 600, 886)
					painter.drawLine(70, 942, 600, 942)
					painter.drawLine(70, 998, 600, 998)
					painter.setPen(cur_pen)
				else:
					pixmap = cur_symbol_test.get_visual_context()
					pixmap = pixmap.scaled(300, 300)

					painter.drawPixmap(200, 10, pixmap)

					pixmap = cur_symbol_test.get_symbol()
					pixmap = pixmap.scaled(250, 250)

					painter.drawPixmap(225, 320, pixmap)

					painter.drawText(750, 20, cur_symbol_test.get_page())
					#painter.drawText(420, 200, 350, 400, QtCore.Qt.TextWordWrap, "Context: " + cur_symbol_test.get_context())
					painter.drawText(30, 600, cur_symbol_test.get_question1())
					painter.drawText(30, 830, cur_symbol_test.get_question2())

					cur_pen = painter.pen()
					line_pen = QPen()
					line_pen.setWidth(2)
					painter.setPen(line_pen)
					painter.drawLine(70, 656, 600, 656)
					painter.drawLine(70, 712, 600, 712)
					painter.drawLine(70, 768, 600, 768)

					painter.drawLine(70, 886, 600, 886)
					painter.drawLine(70, 942, 600, 942)
					painter.drawLine(70, 998, 600, 998)
					painter.setPen(cur_pen)
				if(i < self.symbol_tests.count() - 1):
					printer.newPage()
	
			painter.end()

	def import_symbols(self):
		fnames = QFileDialog.getOpenFileNames(self, 'Open file', 'c:\\',"Image files (*.jpg *.png)")
		#print(fnames)
		if fnames != ([], ''):
			for i in range(len(fnames[0]) - 1, -1, -1):
				page = self.symbol_tests.count() + 1
				test = SymbolTestWidget(self, comp_questions=[self.question1, self.question2], pageNumber=page, pageTotal=page)
				test.set_symbol(fnames[0][i])
				self.symbol_tests.addWidget(test)
			self.symbol_tests.setCurrentIndex(page - 1)

	def delete_test(self):
		if self.symbol_tests.currentIndex() != 0:
			cur_idx = self.symbol_tests.currentIndex()
			self.symbol_tests.setCurrentIndex(cur_idx - 1)
			self.symbol_tests.removeWidget(self.symbol_tests.widget(cur_idx))
			for i in range(0, self.symbol_tests.count()):
				cur_symbol_test = self.symbol_tests.widget(i)
				cur_symbol_test.set_numPages(self.symbol_tests.count())
				
				if i >= cur_idx:
					cur_symbol_test.set_page(i + 1)

		elif self.symbol_tests.currentIndex() == 0 and self.symbol_tests.count() > 1:
			self.symbol_tests.setCurrentIndex(1)
			self.symbol_tests.removeWidget(self.symbol_tests.widget(0))
			for i in range(0, self.symbol_tests.count()):
				cur_symbol_test = self.symbol_tests.widget(i)
				cur_symbol_test.set_numPages(self.symbol_tests.count())
				cur_symbol_test.set_page(i + 1)

		elif self.symbol_tests.currentIndex() == 0 and self.symbol_tests.count() == 1:
			page = 1
			test = SymbolTestWidget(self, comp_questions=[self.question1, self.question2], pageNumber=page, pageTotal=page)
			self.symbol_tests.addWidget(test)
			self.symbol_tests.setCurrentIndex(1)
			self.symbol_tests.removeWidget(self.symbol_tests.widget(0))

	def move_test_left(self):
		cur_idx = self.symbol_tests.currentIndex()
		if cur_idx > 0:
			cur_widget = self.symbol_tests.widget(cur_idx)
			prev_widget = self.symbol_tests.widget(cur_idx - 1)
			cur_widget.set_page(int(cur_widget.get_page()) - 1)
			prev_widget.set_page(int(prev_widget.get_page()) + 1)

			self.symbol_tests.removeWidget(prev_widget)
			self.symbol_tests.insertWidget(self.symbol_tests.indexOf(cur_widget) + 1, prev_widget)
		
	def move_test_right(self):
		cur_idx = self.symbol_tests.currentIndex()
		if cur_idx < self.symbol_tests.count() - 1:
			cur_widget = self.symbol_tests.widget(cur_idx)
			next_widget = self.symbol_tests.widget(cur_idx + 1)
			cur_widget.set_page(int(cur_widget.get_page()) + 1)
			next_widget.set_page(int(next_widget.get_page()) - 1)

			self.symbol_tests.removeWidget(next_widget)
			self.symbol_tests.insertWidget(self.symbol_tests.indexOf(cur_widget), next_widget)

	def change_questions(self):
		text = QInputDialog.getText(self, "Question 1 Input", "Question 1: ", QLineEdit.Normal, self.question1)
		if str(text[0]) != '':
			self.question1 = str(text[0])
		text = QInputDialog.getText(self, "Question 2 Input", "Question 2: ", QLineEdit.Normal, self.question2)
		if str(text[0]) != '':
			self.question2 = str(text[0])

def main():
	app = QApplication(sys.argv)
	test = ComprehensionTestApp()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()