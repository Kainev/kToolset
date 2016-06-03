# PySide Imports
import PySide.QtCore as qc
import PySide.QtGui as qg

# KAR Imports
import widgets
from ..utils import KAR_uiUtils as kuiUtils; reload(kuiUtils)


class ModuleOutliner(qg.QWidget):
    """
    The ModuleOutliner is a list, similar to the Maya outliner, that shows all currently installed modules
    and allows you to select a module to edit.
    """

    outliners = []

    # Order of list items UUIDS
    outliner_order = []

    def __init__(self, scene, parent=None):
        super(ModuleOutliner, self).__init__(parent=parent)

        # Rig Scene
        self.scene = scene

        self.setLayout(qg.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(2)

        self._add_top_buttons()

        self.module_list = _ModuleOutlinerList(parent=self)
        self.layout().addWidget(self.module_list)

        # Display Order
       # self.outliner_order = self.module_list.get_order()

        self.module_list.add_item('Test', kuiUtils.get_icon('Biped_Arm'), None)
        self.module_list.add_item('Test2', kuiUtils.get_icon('Biped_Arm'), None)
        self.module_list.add_item('Test3', kuiUtils.get_icon('Biped_Leg'), None)
        self.module_list.add_item('Test4', kuiUtils.get_icon('Biped_Arm'), None)
        self.module_list.add_item('Test5', kuiUtils.get_icon('Biped_Hand'), None)

    def _add_top_buttons(self):
        layout = qg.QHBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(3)
        layout.setAlignment(qc.Qt.AlignLeft)

        btn_delete = qg.QPushButton('Delete', self)
        btn_delete.setFixedWidth(55)
        btn_delete.setFixedHeight(20)
        btn_delete.clicked.connect(self._delete)

        layout.addWidget(btn_delete)

        self.layout().addLayout(layout)


    def _delete(self):
        pass


class _ModuleOutlinerList(widgets.ListWidget):
    def __init__(self, parent=None):
        super(_ModuleOutlinerList, self).__init__(parent=parent)



