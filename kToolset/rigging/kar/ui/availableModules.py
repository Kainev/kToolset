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
    add_module = qc.Signal()

    # AVAILABLE MODULES
    MODULES = [{'name': 'Biped_Arm', 'template': modules.ArmModule},
               {'name': 'Biped_Hand', 'template': modules.HandModule},
               {'name': 'Biped_Spine', 'template': modules.SpineModule},
               {'name': 'Biped_Leg', 'template': modules.LegModule},
               {'name': 'Biped_Foot', 'template': modules.FootModule},
               {'name': 'Biped_Joint', 'template': modules.JointModule}]

    def __init__(self, parent=None):
        super(AvailableModules, self).__init__('Available Modules', parent=parent)
        self.setFloating(False)
        self.setAllowedAreas(qc.Qt.LeftDockWidgetArea | qc.Qt.RightDockWidgetArea)
        self.setMinimumWidth(175)

        self.content_widget = qg.QWidget()
        self.content_widget.setLayout(qg.QVBoxLayout())
        self.content_widget.layout().setContentsMargins(5, 5, 5, 5)
        self.content_widget.layout().setSpacing(2)
        self.content_widget.layout().setAlignment(qc.Qt.AlignTop)
        self.setWidget(self.content_widget)

        self.module_list = widgets.ListWidget(parent=self, drag_enabled=False)

        add_button_upper = qg.QPushButton('Add')
        main_label_upper = qg.QLabel('Available Modules')
        main_label_upper.setAlignment(qc.Qt.AlignHCenter | qc.Qt.AlignVCenter)

        add_button_lower = qg.QPushButton('Add')
        main_label_lower = qg.QLabel('Available Modules')
        main_label_lower.setAlignment(qc.Qt.AlignHCenter | qc.Qt.AlignVCenter)

        self.content_widget.layout().addWidget(add_button_upper)
        self.content_widget.layout().addSpacerItem(qg.QSpacerItem(5, 5))
        self.content_widget.layout().addWidget(main_label_upper)
        self.content_widget.layout().addSpacerItem(qg.QSpacerItem(5, 5))
        self.content_widget.layout().addWidget(self.module_list)
        self.content_widget.layout().addSpacerItem(qg.QSpacerItem(5, 5))
        self.content_widget.layout().addWidget(main_label_lower)
        self.content_widget.layout().addSpacerItem(qg.QSpacerItem(5, 5))
        self.content_widget.layout().addWidget(add_button_lower)

        self._add_list_items()

    def _add_list_items(self):
        for module in self.MODULES:
            self.module_list.add_item(module['name'], module['template'].icon, data=module)

