from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QApplication

import sys

# define UI layout
class ProductivityMonitor(QDialog):
	def __init__(self):
		super(ProductivityMonitor, self).__init__()
		loadUi('../GUI/main.ui', self)
		
		# button definition
		self.test.clicked.connect(self.test_func)
		self.start.clicked.connect(self.start_func)
		self.clear.clicked.connect(self.clear_data_func)
		self.stop.clicked.connect(self.stop_func)

		self.check_status = False

	def test_func(self):
		pass
	
	def clear_data_func(self):
		pass

	def start_func(self):
		if not self.check_status:
			self.test.setEnabled(False)
			self.clear.setEnabled(False)
			self.check_status = True
	
	def stop_func(self):
		if self.check_status:
			self.test.setEnabled(True)
			self.clear.setEnabled(True)
			self.check_status = False


# start app
if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = ProductivityMonitor()
	window.show()
	sys.exit(app.exec())
