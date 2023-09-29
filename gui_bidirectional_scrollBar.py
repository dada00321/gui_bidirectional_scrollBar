"""
Bi-direction slide bar + tick labels
-------------------
Reference:
[1] Python PyQt4 slider with tick labels
https://stackoverflow.com/questions/47494305/python-pyqt4-slider-with-tick-labels
"""
import sys
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QStyle, QStyleOptionSlider, QLabel
from PyQt5.QtCore import QRect, QPoint, Qt
from qtrangeslider import QRangeSlider

class LabeledSlider(QtWidgets.QWidget):
	def __init__(self, minimum, maximum, interval=1, orientation=Qt.Horizontal,
			labels=None, parent=None):
		super(LabeledSlider, self).__init__(parent=parent)

		levels=range(minimum, maximum+interval, interval)
		if labels is not None:
			if not isinstance(labels, (tuple, list)):
				raise Exception("<labels> is a list or tuple.")
			if len(labels) != len(levels):
				raise Exception("Size of <labels> doesn't match levels.")
			self.levels=list(zip(levels,labels))
		else:
			self.levels=list(zip(levels,map(str,levels)))

		if orientation==Qt.Horizontal:
			self.layout=QtWidgets.QVBoxLayout(self)
		elif orientation==Qt.Vertical:
			self.layout=QtWidgets.QHBoxLayout(self)
		else:
			raise Exception("<orientation> wrong.")

		# gives some space to print labels
		self.left_margin=10
		self.top_margin=10
		self.right_margin=10
		self.bottom_margin=10

		self.layout.setContentsMargins(self.left_margin,self.top_margin,
				self.right_margin,self.bottom_margin)

		#self.sl=QtWidgets.QSlider(orientation, self)
		self.sl = QRangeSlider()
		self.sl.setOrientation(1) # horizontal orientation
		self.sl.setMinimum(minimum)
		self.sl.setMaximum(maximum)
		#self.sl.setValue(minimum)


		if orientation==Qt.Horizontal:
			self.sl.setTickPosition(QtWidgets.QSlider.TicksBelow)
			self.sl.setMinimumWidth(300) # just to make it easier to read
		else:
			self.sl.setTickPosition(QtWidgets.QSlider.TicksLeft)
			self.sl.setMinimumHeight(300) # just to make it easier to read
		'''
		'''
		self.sl.setTickInterval(interval)
		self.sl.setSingleStep(1)

		self.layout.addWidget(self.sl)

	def paintEvent(self, e):

		super(LabeledSlider,self).paintEvent(e)

		style=self.sl.style()
		painter=QPainter(self)
		st_slider=QStyleOptionSlider()
		st_slider.initFrom(self.sl)
		st_slider.orientation=self.sl.orientation()

		length=style.pixelMetric(QStyle.PM_SliderLength, st_slider, self.sl)
		available=style.pixelMetric(QStyle.PM_SliderSpaceAvailable, st_slider, self.sl)

		for v, v_str in self.levels:

			# get the size of the label
			rect=painter.drawText(QRect(), Qt.TextDontPrint, v_str)

			if self.sl.orientation()==Qt.Horizontal:
				# I assume the offset is layoutlf the length of slider, therefore
				# + length//2
				x_loc=QStyle.sliderPositionFromValue(int(self.sl.minimum()),
						int(self.sl.maximum()), int(v), int(available))+length//2

				# left bound of the text = center - layoutlf of text width + L_margin
				left=x_loc-rect.width()//2+self.left_margin
				bottom=self.rect().bottom()

				# enlarge margins if clipping
				if v==self.sl.minimum():
					if left<=0:
						self.left_margin=rect.width()//2-x_loc
					if self.bottom_margin<=rect.height():
						self.bottom_margin=rect.height()

					self.layout.setContentsMargins(self.left_margin,
							self.top_margin, self.right_margin,
							self.bottom_margin)

				if v==self.sl.maximum() and rect.width()//2>=self.right_margin:
					self.right_margin=rect.width()//2
					self.layout.setContentsMargins(self.left_margin,
							self.top_margin, self.right_margin,
							self.bottom_margin)

			else:
				y_loc=QStyle.sliderPositionFromValue(int(self.sl.minimum()),
						int(self.sl.maximum()), int(v), int(available), upsideDown=True)

				bottom=y_loc+length//2+rect.height()//2+self.top_margin-3
				# there is a 3 px offset tlayoutt I can't attribute to any metric

				left=self.left_margin-rect.width()
				if left<=0:
					self.left_margin=rect.width()+2
					self.layout.setContentsMargins(self.left_margin,
							self.top_margin, self.right_margin,
							self.bottom_margin)

			pos=QPoint(left, bottom)
			painter.drawText(pos, v_str)

		return

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	frame = QtWidgets.QWidget()
	frame.setWindowTitle("HSV sliders")

	layout = QtWidgets.QVBoxLayout()
	main_widget = QtWidgets.QWidget()

	main_layout = QtWidgets.QVBoxLayout()
	main_widget.setLayout(main_layout)

	#frame.setLayout(layout)
	frame.setLayout(main_layout)

	dimensions = {'h': [0,180,30], 's': [0,255,51], 'v': [0,255,51]}

	# Create three QLabel-slider pairs
	for dim, nums in dimensions.items():
		#label = QLabel(f"Slider {i+1}")
		label = QLabel(dim)
		#layout.addWidget(label)

		min_val, max_val, interval = nums
		slider = LabeledSlider(min_val, max_val, interval, orientation=Qt.Horizontal)
		#layout.addWidget(slider)

		# Add label and slider to a horizontal layout
		pair_layout = QtWidgets.QHBoxLayout()
		pair_layout.addWidget(label)
		pair_layout.addWidget(slider)

		main_layout.addLayout(pair_layout)

	'''
	w1 = LabeledSlider(0, 100, 20, orientation=Qt.Horizontal)
	layout.addWidget(w1)

	w2 = LabeledSlider(0, 255, 51, orientation=Qt.Horizontal)
	layout.addWidget(w2)

	w3 = LabeledSlider(0, 255, 51, orientation=Qt.Horizontal)
	layout.addWidget(w2)
	'''

	button = QtWidgets.QPushButton("Apply")
	main_layout.addWidget(button, 0, Qt.AlignCenter)

	frame.show()
	sys.exit(app.exec_())
