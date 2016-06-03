# PySide Imports
import PySide.QtCore as qc
import PySide.QtGui as qg

# KAR Imports
import widgets


class AvailableModules(qg.QDockWidget):
    """
    The ModuleOutliner is a list, similar to the Maya outliner, that shows all currently installed modules
    and allows you to select a module to edit.
    """
    # SIGNALS
    add_module = qc.Signal()

    def __init__(self, parent=None):
        super(AvailableModules, self).__init__('Add Modules', parent=parent)
        self.setFloating(False)
        self.setAllowedAreas(qc.Qt.LeftDockWidgetArea | qc.Qt.RightDockWidgetArea)

        self.content_widget = qg.QWidget()

        self.content_widget.setLayout(qg.QVBoxLayout())
        self.content_widget.layout().setContentsMargins(0, 0, 0, 0)
        self.content_widget.layout().setSpacing(2)
        self.content_widget.layout().setAlignment(qc.Qt.AlignTop)

        self.setWidget(self.content_widget)

        self._add_top_buttons()

        module_list = widgets.ListWidget(parent=self)
        self.content_widget.layout().addWidget(module_list)

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

        self.content_widget.layout().addLayout(layout)

    def _delete(self):
        pass

