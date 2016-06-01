# PySide Imports
import PySide.QtCore as qc
import PySide.QtGui as qg

# KAR Imports
import widgets

class Modules(qg.QWidget):
    """
    To write..
    """
    def __init__(self):
        super(Modules, self).__init__()
        # Master layout settings
        self.setLayout(qg.QVBoxLayout())
        self.layout().setContentsMargins(5, 5, 5, 5)
        self.layout().setSpacing(0)
        self.layout().setAlignment(qc.Qt.AlignTop)

        frame_main = qg.QFrame()
        self.layout().addWidget(frame_main)
        frame_main.setFrameStyle(qg.QFrame.Box | qg.QFrame.Sunken)
        frame_main.setLayout(qg.QVBoxLayout())
        frame_main.layout().setContentsMargins(5, 5, 5, 5)
        frame_main.layout().setSpacing(2)
        frame_main.layout().addWidget(widgets.decorators.Heading('Installed Modules', parent=self))



