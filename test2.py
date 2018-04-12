import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon

class Test(QWidget):
	def __init__(self):
		super().__init__()

		self.init_UI()
	def init_UI(self):
		self.setGeometry(300, 300, 300, 220)
		self.setWindowTitle("Hello")
		self.setWindowIcon(QIcon("rubber duckie.png"))

		self.show()

def main():
	app = QApplication(sys.argv)
	test = Test()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()