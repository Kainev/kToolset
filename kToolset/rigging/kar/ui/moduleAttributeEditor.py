# PySide Imports
import PySide.QtCore as qc
import PySide.QtGui as qg

# KAR Imports

#from kToolset.kToolset.rigging.kar import ui
from .. import ui as kui


class ModuleAttributeEditor(qg.QWidget):
    """
    To write..
    """
    def __init__(self, scene, parent=None):
        super(ModuleAttributeEditor, self).__init__(parent=parent)

        # Rig Scene
        self.scene = scene

        # Content Frame
        content_frame = qg.QFrame()
        # self.layout().addWidget(content_frame)
        content_frame.setFrameStyle(qg.QFrame.Box | qg.QFrame.Sunken)
        content_frame.setLayout(qg.QVBoxLayout())
        content_frame.layout().setContentsMargins(5, 5, 5, 5)
        content_frame.layout().setSpacing(2)
        content_frame.layout().addWidget(kui.widgets.decorators.Heading('Installed Modules', parent=self))

        # Main Content
        size_policy_expanding = qg.QSizePolicy(qg.QSizePolicy.Expanding, qg.QSizePolicy.Expanding)

        self.setSizePolicy(size_policy_expanding)




        



