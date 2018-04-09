import pdfkit
import PyQt5

class SymbolTest(Object):
	"""
	@modifies symbol_, text_context_, visual_context_, has_visual
	@effects creates a new page object with the supplied fields set to the fiven value
			 or none if the value does not work 
	"""
	def __init__(self, symbol=None, text_context=None, visual_context=None):
		symbol_ = symbol_
		text_context_ = text_context
		visual_context_ = visual_context
		if(not(visual_context_) == None):
			has_visual = true
		else:
			has_visual = false
	"""
	@modifes none
	@effects draws the test on the provided page, places the fields in the correct locatio
	"""
	def draw(self, page):
		pass

	"""
	@modifies text_context_
	@effects sets text_context_ to the provided text_context
	"""
	def add_text_context(text_context):
	 	pass 

	"""
	@modifes text_context_
	@effects reads in text from the given file,
	"""
	def add_text_context_from_file(text_file_name):
		pass
	def add_visual_context():
		pass
	def add_symbol():
		pass

def generateBlankPage():
	pass

def generateResponder():
	pass

def main():
	pass

if __name__ == '__main__':
	main()