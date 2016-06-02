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

        # Content Frame
        content_frame = qg.QFrame()
        self.layout().addWidget(content_frame)
        content_frame.setFrameStyle(qg.QFrame.Box | qg.QFrame.Sunken)
        content_frame.setLayout(qg.QVBoxLayout())
        content_frame.layout().setContentsMargins(5, 5, 5, 5)
        content_frame.layout().setSpacing(2)
        content_frame.layout().addWidget(widgets.decorators.Heading('Installed Modules', parent=self))
        
        # Main Content
        size_policy_expanding = qg.QSizePolicy(qg.QSizePolicy.Expanding, qg.QSizePolicy.Expanding)
        
        content_splitter = qg.QSplitter(qc.Qt.Orientation.Horizontal)
        content_splitter.setSizePolicy(size_policy_expanding)

        content_frame.layout().addWidget(content_splitter)

        # Installed Modules List
        modules_list = widgets.ListWidget()
        modules_list2 = widgets.ListWidget()
        content_splitter.addWidget(modules_list)
        content_splitter.addWidget(modules_list2)

        content_splitter.setSizes([200, 300])



        



