# PySide Imports
import PySide.QtCore as qc
import PySide.QtGui as qg

# KAR Imports
#from .. import KAR_autoRigUI as karUI
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

    def __init__(self, scene, main_ui, parent=None):
        super(ModuleOutliner, self).__init__('Module Outliner', parent=parent)
        self.setFloating(False)
        self.setAllowedAreas(qc.Qt.LeftDockWidgetArea | qc.Qt.RightDockWidgetArea)

        # Rig Scene
        self.scene = scene

        self.main_ui = main_ui
        print self.main_ui.docks

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

        self.setMinimumWidth(175)
        self.update()

        self.module_list.add_item('test', None, None)
        self.module_list.add_item('test', None, None)
        self.module_list.add_item('test', None, None)
        self.module_list.add_item('test', None, None)

        # Connect Signals
        self.scene.scene_updated.connect(self.update_outliner)
        self.module_list.drag_add.connect(self.main_ui.docks['available_modules'].drag_add)



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
        """
        Retrieves the list of UUIDs stored in each selected _ListItem's data attribute,
        deletes the list items then removes the corresponding modules from the rig scene
        """
        removed_data = self.module_list.get_selected_data(hierarchy=True)
        self.module_list.remove_selected()
        self.scene.delete_modules(removed_data, trigger_update=False)

    def update_outliner(self):
        """
        Compares the outliner list items to the rig scenes module list.

        Scene Module not in outliner: Adds new list item corresponding to module
        Item in list with no match in module list: Deletes list item
        Item parent does not match modules parent: Reparents list item to correct item
        :return:
        """
        module_list_data = self.module_list.get_all_data()
        scene_modules = self.scene.get_all_modules()

        for _module in scene_modules:
            val = next((x for x in module_list_data if x == scene_modules[_module].uuid), None)

            if val is None:
                self.module_list.add_item(scene_modules[_module].name, icon_pixmap=scene_modules[_module].icon,
                                          data=scene_modules[_module].uuid)


class _ModuleOutlinerList(widgets.ListWidget):
    # Signals
    drag_add = qc.Signal(qg.QWidget)

    def __init__(self, parent=None, ):
        super(_ModuleOutlinerList, self).__init__(parent=parent)

    def dropEvent(self, event):
        if event.source().parent().objectName() == 'AvailableModulesList':
            self.drag_add.emit(event.source())
            return

        super(_ModuleOutlinerList, self).drop_event(target_item, event_args)


    def drop_event(self, target_item, event_args):
        dropped_item, location = event_args

        if dropped_item.parent().objectName() == 'AvailableModulesList':
            return

        super(_ModuleOutlinerList, self).drop_event(target_item, event_args)



