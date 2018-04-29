TEMPLATE = """
<!DOCTYPE HTML>
<HTML>
	<HEAD>
		<style>
		.column {{
			float: left;
			padding: 10px;
			height: 100%;
			margin 0;
		}}

		.column.side{{
			width: 25%;
		}}

		.column.middle{{
			width: 50%;
		}}

		.row {{
			width: 100%;
		}}

		.row:before,
		.row:after{{
			content: "";
			display: table;
			clear: both;
		}}
		</style>
	</HEAD>
	<BODY>
		<div class="row">
			<div class="column side">
				<img src="{}" width="350" height="350">

			</div>
			<div class="column middle">
			</div>
			<div class="column side">
				<p>
					{}
				</p> 
			</div>
		</div>
		<div class="row">
			<div class="column side">
				<p>
					{}
				</p>
				<p>
					{}
				</p>
			</div>
			<div class="column middle">
			</div>
			<div class="colum  side">
			</div>
		</div>
	</BODY>
</HTML>
"""

import sys, io, os
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PyQt5.QtWidgets import qApp, QAction, QApplication, QFileDialog, QGridLayout, QLabel, QLineEdit, QMainWindow, QPushButton, QStackedWidget, QTextEdit, QWidget
from PyQt5.QtGui import QIcon, QFont, QPainter, QPen, QPixmap, QTextDocument
from PyQt5.QtPrintSupport import QPrinter
#from PyQt5.QtTextFlag import TextWordWrap
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
		self.textual_edit = QTextEdit(self)

		self.page = pageNumber
		self.numPages = pageTotal
		self.init_gui(parent)


	"""
	@modifes none
	@effects draws the test on the provided page, places the fields in the correct locatio
	"""
	def init_gui(self, parent):
		self.setFixedHeight(500)
		self.setFixedWidth(500)

		textual_label = QLabel(self)
		visual_label = QLabel(self)

		layout = QGridLayout()
		layout.setColumnMinimumWidth(3, 10)
		layout.setSpacing(5)

		if self.symbol_ != None:
			pic = QPixmap(self.symbol_)
			pic.scaled(350, 350);
			self.symbol_label.setPixmap(pic)
		else:
			pic = QPixmap("blank image.png")
			pic.scaled(350, 350)
			self.symbol_label.setPixmap(pic)
		layout.setRowStretch(1, 1)
		layout.setColumnStretch(4, 1)
		layout.addWidget(self.symbol_label, 1, 1, 2, 2)

		self.page_label.setText("Page " + str(self.page) + "/" + str(self.numPages))
		layout.addWidget(self.page_label, 0, 10, 1, 1)

		if self.visual_context_ == None and self.text_context_ != None:
			textual_label.setText("Context")
			self.textual_edit.setText(self.text_context_)
			layout.addWidget(textual_label, 2, 4)
			layout.addWidget(self.textual_edit, 2, 5, 1, 1)

		elif self.visual_context_ == None and self.text_context_ == None:
			textual_label.setText("Context")
			layout.addWidget(textual_label, 1, 4)
			layout.addWidget(self.textual_edit, 2, 4, 1, 4)

		else:
			visual_label = visual_context_

		symbolBtn = QPushButton("Add Symbol", self)
		symbolBtn.setToolTip("Used to add or change the symbol on this page")
		symbolBtn.resize(symbolBtn.sizeHint())
		symbolBtn.clicked.connect(self.open_symbol)
		layout.addWidget(symbolBtn, 3, 1, 1, 1)

		counter = 7
		for question in self.questions:
			qBox = QLineEdit(self)
			qNumbering = QLabel(self)
			qBox.setText(question)
			qNumbering.setText("Question " + str(counter - 6) + ":")
			layout.addWidget(qNumbering, counter, 1, 1, 1)
			layout.addWidget(qBox, counter, 2, 1, 1)
			counter += 1
		self.setLayout(layout)

	"""
	@modifes self.symbol_label
	@effects opens an image file and sets symbol_label to have that image
	"""
	def open_symbol(self):
		fname = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\',"Image files (*.jpg *.png)")
		if fname != None:
			pic = QPixmap(fname[0])
			pic = pic.scaled(350, 350)
			self.symbol_ = fname[0]
			#pic.scaled(350, 350)
			self.symbol_label.setPixmap(pic)
		else:
			pic = QPixmap("blank image.png") 
			pic = pic.scaled(350, 350)
			#pic.scaled(350, 35)
			self.symbol_label.setPixmap(pic)

	def get_page(self):
		return str(self.page)
	def get_numPages(self):
		return self.numPages
	def set_page(self, pageNum):
		self.page = pageNum
		self.init_gui()
	def set_numPages(self, pageTotal):
		self.numPages = pageTotal
		self.page_label.setText("Page " + str(self.page) + "/" + str(self.numPages))

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

class ComprehensionTestApp(QMainWindow):
	def __init__(self):
		super().__init__()
		self.symbol_tests = QStackedWidget()
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

		menu_bar = self.menuBar()
		filemenu = menu_bar.addMenu('&File')
		filemenu.addAction(saveAct)
		filemenu.addAction(exitAct)

		nextAct = QAction(QIcon("next.png"), 'Next', self)
		nextAct.setStatusTip('Goes to the next page')
		nextAct.triggered.connect(self.next_page)

		prevAct = QAction(QIcon("prev.png"), "Prev", self)
		prevAct.setStatusTip('Goes to the previous page')
		prevAct.triggered.connect(self.prev_page)

		newAct = QAction(QIcon("add.png"), "Add", self)
		newAct.setStatusTip('Creates a new page')
		newAct.triggered.connect(self.add_blank_test)

		"""
		nextButton = PicButton(QPixmap("next.png"))
		nextButton.resize(self.sizeHint())
		nextButton.clicked.connect(self.next_page)
		"""

		tool_bar = self.addToolBar("Next Page")
		tool_bar.addAction(prevAct)
		tool_bar.addAction(nextAct)
		tool_bar.addAction(newAct)

		self.setWindowTitle("Hello")
		self.setWindowIcon(QIcon("rubber duckie.png"))
		self.setGeometry(500, 500, 500, 450)
		self.add_blank_test()
		self.setCentralWidget(self.symbol_tests)

		self.show()

	def add_blank_test(self):
		question1 = "Exactly what do you think this symbol means?"
		question2 = "What action would you take in response to this symbol?"
		page = self.symbol_tests.count() + 1
		test = SymbolTestWidget(self, comp_questions=[question1, question2], pageNumber=page, pageTotal=page)
		self.symbol_tests.addWidget(test)
		self.symbol_tests.setCurrentIndex(page - 1)

	def add_test(self):
		question1 = "Exactly what do you think this symbol means?"
		question2 = "What action would you take in response to this symbol?"
		page = self.symbol_tests.count() + 1
		test = SymbolTestWidget(self, comp_questions=[question1, question2], pageNumber=page, pageTotal=page)
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

		"""
		packet = io.BytesIO()
		can = canvas.Canvas(packet, pagesize=letter)
		can.drawString(10, 100, "Hello world")
		can.save()

		packet.seek(0)
		new_pdf = PdfFileReader(packet)
		existing_pdf = PdfFileReader(open(filename[0]), "rb")
		"""

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
			
			test = """This is a very long sentence that serves absolutely no purpose whatsoever.
asdfjkl; Let's see how our program handles this, ThisIsAnExtremelyLongWordLetsSeeWhatHappensShallWe? DicksNShit49420@cox.net Beep Beep Imma Jepp"""

			painter = QPainter()
			font = QFont("times")
			font.setPointSize(12)
			painter.begin(printer)
			painter.setFont(font)

			for i in range(0, self.symbol_tests.count()):
				#doc = QTextDocument()
				curr_symbol_test = self.symbol_tests.widget(i)

				pixmap = curr_symbol_test.get_symbol()
				pixmap = pixmap.scaled(350, 350)
				#print(pixmap)
				painter.drawPixmap(30, 100, pixmap)
				painter.drawText(750, 20, curr_symbol_test.get_page())
				painter.drawText(420, 200, 350, 400, QtCore.Qt.TextWordWrap, "Context: " + curr_symbol_test.get_context())
				painter.drawText(30, 600, curr_symbol_test.get_question1())
				painter.drawText(30, 830, curr_symbol_test.get_question2())

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

				"""
				template = TEMPLATE
				template = template.format(curr_symbol_test.get_symbol(), curr_symbol_test.get_context(), curr_symbol_test.get_question1(), curr_symbol_test.get_question2())
				print(template)
				doc = QTextDocument()
				doc.setHtml(template)
				print(doc.toHtml())
				doc.drawContents(painter)
				"""
				if(i < self.symbol_tests.count() - 1):
					printer.newPage()
	
			painter.end()
			
def main():
	app = QApplication(sys.argv)
	test = ComprehensionTestApp()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()