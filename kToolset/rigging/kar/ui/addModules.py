# PySide Imports
import PySide.QtCore as qc
import PySide.QtGui as qg

# KAR Imports
import widgets

from .. import modules; reload(modules)


class AvailableModules(qg.QDockWidget):
    """
    The ModuleOutliner is a list, similar to the Maya outliner, that shows all currently installed modules
    and allows you to select a module to edit.
    """
    # SIGNALS
    add_module = qc.Signal(list)

    # AVAILABLE MODULES
    MODULES = [modules.ArmModule,
               modules.HandModule,
               modules.SpineModule,
               modules.LegModule,
               modules.FootModule,
               modules.JointModule]

    def __init__(self, tool, parent=None):
        super(AvailableModules, self).__init__('Add Modules', parent=parent)
        self.setFloating(False)
        self.setAllowedAreas(qc.Qt.LeftDockWidgetArea | qc.Qt.RightDockWidgetArea)
        self.setMinimumWidth(175)

        self.tool = tool
        self.main_ui = parent

        self.content_widget = qg.QWidget()
        self.content_widget.setLayout(qg.QVBoxLayout())
        self.content_widget.layout().setContentsMargins(5, 5, 5, 5)
        self.content_widget.layout().setSpacing(2)
        self.content_widget.layout().setAlignment(qc.Qt.AlignTop)
        self.setWidget(self.content_widget)

        self.module_list = widgets.ListWidget(parent=self, drop_enabled=False)
        self.module_list.list_widget.setObjectName('AvailableModulesList')

        main_label_upper = qg.QLabel('Available Modules')
        main_label_upper.setAlignment(qc.Qt.AlignHCenter | qc.Qt.AlignVCenter)

        add_button_lower = qg.QPushButton('Add')

        self.content_widget.layout().addSpacerItem(qg.QSpacerItem(4, 4))
        self.content_widget.layout().addWidget(main_label_upper)
        self.content_widget.layout().addSpacerItem(qg.QSpacerItem(10, 10))
        self.content_widget.layout().addWidget(self.module_list)
        self.content_widget.layout().addSpacerItem(qg.QSpacerItem(5, 5))
        self.content_widget.layout().addWidget(add_button_lower)

        add_button_lower.clicked.connect(self.add_selected)

        self._add_list_items()

    def _add_list_items(self):
        """
        Adds the visual items to the list
        """
        for module in self.MODULES:
            self.module_list.add_item(module.__name__, module.icon, data=module)

    def add_selected(self):
        """
        Adds currently selected modules to the scene and forces an update
        """
        _modules = self.module_list.get_selected_data()
        for m in _modules:
            _module = m()
            self.tool.add_module(_module, trigger_update=False)

        self.main_ui.emit_update()


