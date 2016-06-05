# PySide Imports
import PySide.QtCore as qc
import PySide.QtGui as qg

# KAR Imports
import widgets
from ..utils import KAR_uiUtils as kuiUtils; reload(kuiUtils)


class ModuleOutliner(qg.QDockWidget):
    """
    The ModuleOutliner is a list, similar to the Maya outliner, that shows all currently installed modules
    and allows you to select a module to edit.
    """

    outliners = []

    # Order of list items UUIDS
    outliner_order = []

    def __init__(self, scene, parent=None):
        super(ModuleOutliner, self).__init__('Module Outliner', parent=parent)
        self.setFloating(False)
        self.setAllowedAreas(qc.Qt.LeftDockWidgetArea | qc.Qt.RightDockWidgetArea)

        # Rig Scene
        self.scene = scene

        # Content Widget
        self.content_widget = qg.QWidget()
        self.content_widget.setLayout(qg.QVBoxLayout())
        self.content_widget.layout().setContentsMargins(5, 5, 5, 5)
        self.content_widget.layout().setSpacing(2)
        self.content_widget.layout().setAlignment(qc.Qt.AlignTop)
        self.setWidget(self.content_widget)

        self._add_top_buttons()

        self.module_list = _ModuleOutlinerList(parent=self)
        self.content_widget.layout().addWidget(self.module_list)

        self.module_list.add_item('Test', kuiUtils.get_icon('Biped_Arm'), None)
        self.module_list.add_item('Test2', kuiUtils.get_icon('Biped_Arm'), None)
        self.module_list.add_item('Test3', kuiUtils.get_icon('Biped_Leg'), None)
        self.module_list.add_item('Test4', kuiUtils.get_icon('Biped_Arm'), None)
        self.module_list.add_item('Test5', kuiUtils.get_icon('Biped_Hand'), None)

        self.setMinimumWidth(175)
        self.update()

    def _add_top_buttons(self):
        layout = qg.QHBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(3)
        layout.setAlignment(qc.Qt.AlignLeft)

        btn_delete = widgets.IconButton(pixmap=kuiUtils.get_icon('bin_dark'),
                                        pixmap_hover=kuiUtils.get_icon('bin_light'), icon_size=(16, 16), parent=self)
        btn_delete.clicked.connect(self._delete)

        layout.addSpacerItem(qg.QSpacerItem(5, 5, qg.QSizePolicy.Expanding))
        layout.addWidget(btn_delete)

        self.content_widget.layout().addLayout(layout)


    def _delete(self):
        self.module_list.remove_selected()


class _ModuleOutlinerList(widgets.ListWidget):
    def __init__(self, parent=None):
        super(_ModuleOutlinerList, self).__init__(parent=parent)



