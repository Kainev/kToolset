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

    def __init__(self, scene, parent=None):
        super(AvailableModules, self).__init__('Available Modules', parent=parent)
        self.setFloating(False)
        self.setAllowedAreas(qc.Qt.LeftDockWidgetArea | qc.Qt.RightDockWidgetArea)
        self.setMinimumWidth(175)

        self.scene = scene

        self.content_widget = qg.QWidget()
        self.content_widget.setLayout(qg.QVBoxLayout())
        self.content_widget.layout().setContentsMargins(5, 5, 5, 5)
        self.content_widget.layout().setSpacing(2)
        self.content_widget.layout().setAlignment(qc.Qt.AlignTop)
        self.setWidget(self.content_widget)

        self.module_list = widgets.ListWidget(parent=self, drop_enabled=False)
        self.module_list.list_widget.setObjectName('AvailableModulesList')

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

        add_button_lower.clicked.connect(self._add_selected)

        self._add_list_items()

    def _add_list_items(self):
        """
        Adds the visual items to the list
        """
        for module in self.MODULES:
            self.module_list.add_item(module.__name__, module.icon, data=module)

    def _add_selected(self):
        """
        Adds currently selected modules to the scene and forces an update
        """
        _modules = self.module_list.get_selected_data()
        for m in _modules:
            _module = m()
            self.scene.add_module(_module, trigger_update=False)

        self.scene.force_update()

    def drag_add(self, event_args):
        """
        Adds dragged items into the scene.

        :param event_args: _ListItem from self.module_list that was dragged to the outliner
        """
        dropped_item, target_item, parent_item = event_args

        selected_modules = self.module_list.get_selected_items()

        # Checks to see if the dragged item was in the current selection.
        # If it is, all selected items are added to the outliner
        # If the dragged item was NOT part of the selection, then only the dragged item is added
        if dropped_item in selected_modules:
            for m in selected_modules:
                _module = m.data()
                self.scene.add_module(_module, trigger_update=False)
        else:
            _module = dropped_item.data()
            self.scene.add_module(_module, trigger_update=False)

        # Forces the scene to send out an update signal, causing the outliner to add the new items
        # to its list
        self.scene.force_update()


