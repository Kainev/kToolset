# PySide Imports
import PySide.QtCore as qc
import PySide.QtGui as qg

# KAR Imports
import widgets
from ..utils import KAR_uiUtils as kuiUtils; reload(kuiUtils)


class ModuleOutliner(qg.QDockWidget):
    """
    The ModuleOutliner is a list, similar to the Maya outliner, that shows all currently installed modules
    and that allows you to select a module to edit.
    """

    def __init__(self, tool, parent=None):
        super(ModuleOutliner, self).__init__('Module Outliner', parent=parent)
        self.setFloating(False)
        self.setAllowedAreas(qc.Qt.LeftDockWidgetArea | qc.Qt.RightDockWidgetArea)
        self.setMinimumWidth(175)

        # Rig Scene
        self.tool = tool
        self.main_ui = parent
        self.add_modules_dock = self.main_ui.docks['available_modules']

        # Content Widget ------------------------------------------------ #
        self.content_widget = qg.QWidget()
        self.content_widget.setLayout(qg.QVBoxLayout())
        self.content_widget.layout().setContentsMargins(5, 5, 5, 5)
        self.content_widget.layout().setSpacing(2)
        self.content_widget.layout().setAlignment(qc.Qt.AlignTop)
        self.setWidget(self.content_widget)

        self._add_top_buttons()

        self.module_list = _ModuleOutlinerList(parent=self)
        self.content_widget.layout().addWidget(self.module_list)

        # Connect Signals ----------------------------------------------- #
        self.main_ui.update_signal.connect(self.update_outliner)
        self.module_list.drag_add.connect(self.dropped_from_add_modules)

    # ---------------------------------------------------------------------------------------------------------------- #
    # ---------------------------------------------------------------------------------------------------------------- #
    # Outliner Setup
    # ---------------------------------------------------------------------------------------------------------------- #
    # ---------------------------------------------------------------------------------------------------------------- #
    def _add_top_buttons(self):
        """
        Creates and adds the widget buttons above the outliner list to the layout
        """
        # Top bar layout
        layout = qg.QHBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(3)
        layout.setAlignment(qc.Qt.AlignLeft)
        self.content_widget.layout().addLayout(layout)

        # Delete Button
        btn_delete = widgets.IconButton(pixmap=kuiUtils.get_icon('bin_dark'),
                                        pixmap_hover=kuiUtils.get_icon('bin_light'), icon_size=(16, 16), parent=self)

        # Add Widgets
        layout.addSpacerItem(qg.QSpacerItem(5, 5, qg.QSizePolicy.Expanding))
        layout.addWidget(btn_delete)

        # Connect Signals
        btn_delete.clicked.connect(self.delete_selected)

    # ---------------------------------------------------------------------------------------------------------------- #
    # ---------------------------------------------------------------------------------------------------------------- #
    # Functional/Tool interface functions
    # ---------------------------------------------------------------------------------------------------------------- #
    # ---------------------------------------------------------------------------------------------------------------- #
    def delete_selected(self):
        """
        Retrieves the list of UUIDs stored in each selected _ListItem's data attribute,
        deletes the list items then removes the corresponding modules from the rig scene
        """
        # Get the UUIDs for each module being deleted
        removed_data = [_module.uuid for _module in self.module_list.get_selected_data(hierarchy=True)]
        # Remove the items from the outliner list
        self.module_list.remove_selected()
        # Remove the items from the scene
        self.tool.delete_module(removed_data, trigger_update=False)

    def delete_all(self):
        """
        Retrieves the list of UUIDs stored in each _ListItem's data attribute,
        deletes the list items then removes the corresponding modules from the rig scene

        Keep in mind this may NOT delete all modules if for some reason a module has not been
        correctly added to the outliner. It is safer to delete the modules directly from the scene
        using its delete function.
        """
        # Get the UUIDs for each module in the outliner
        removed_data = self.module_list.get_all_data()
        # Remove the items from the outliner list
        self.module_list.remove_all()
        # Remove the items from the scene
        self.tool.delete_modules(removed_data, trigger_update=False)

    def dropped_from_add_modules(self, event_args):
        """
        Adds dragged items into the scene.

        :param event_args: _ListItem from self.module_list that was dragged to the outliner
        """
        dropped_item, target_item, parent_item = event_args
        selected_modules = self.add_modules_dock.module_list.get_selected_items()

        def add_module(_m):
            """
            Adds a module to the scene and corresponding item to list give then
            the instance of the rig module

            :param _m: rig module instance to add
            """
            if target_item is None:
                # If item is to be parented to the world, simply add it to the scene and let the automatic
                # updating add it to list
                self.tool.add_module(_m, trigger_update=False)
            else:
                # Else if its been dropped onto a particular item manually add it to the list,
                # set its parent and move it into the correct position
                item = self.module_list.add_item(_m.name, _m.icon, _m)
                item.parent_item = parent_item
                self.module_list.move_item_under(item, target_item)
                self.tool.add_module(_m, trigger_update=False)
                item.update()

        # Checks to see if the dragged item was in the current selection.
        # If it is, all selected items are added to the outliner
        # If the dragged item was NOT part of the selection, then only the dragged item is added
        if dropped_item in selected_modules:
            for j in selected_modules:
                _module = j.data()  # Class is stored in data attribute. This creates an instance of that class
                add_module(_module)

        else:
            _module = dropped_item.data()
            add_module(_module)

        # Forces the main UI to send out an update signal, causing the outliner to add the new items
        # to its list
        self.main_ui.emit_update()

    def update_outliner(self):
        """
        Compares the outliner list items to the rig scenes module list.

        Scene Module not in outliner: Adds new list item corresponding to module
        Item in list with no match in module list: Deletes list item
        Item parent does not match modules parent: Re-parents list item to correct item
        :return:
        """
        outliner_list_data = self.module_list.get_all_data()

        for list_item in self.module_list.items:
            if list_item.data not in self.tool.modules.values():
                self.module_list.remove_item(list_item)

        for module_id in self.tool.modules:
            if self.tool.modules[module_id] not in outliner_list_data:
                self.module_list.add_item(self.tool.modules[module_id].name,
                                          icon_pixmap=self.tool.modules[module_id].icon,
                                          data=self.tool.modules[module_id])



class _ModuleOutlinerList(widgets.ListWidget):
    # Signals
    drag_add = qc.Signal(list)

    def __init__(self, parent=None, ):
        super(_ModuleOutlinerList, self).__init__(parent=parent)

    def dropEvent(self, event):
        if event.source().parent().objectName() == 'AvailableModulesList':
            self.drag_add.emit([event.source(), None, None])
            return

        super(_ModuleOutlinerList, self).dropEvent(event)

    def drop_event(self, target_item, event_args):
        dropped_item, location = event_args

        if dropped_item.parent().objectName() == 'AvailableModulesList':
            if location == 0:
                # Make sure the items don't get parented under the world item,
                # if the target_item is the dropped widget defaults to parenting to the world (None)
                if target_item != self._world_item:
                    self.drag_add.emit([dropped_item, target_item, target_item])
                else:
                    self.drag_add.emit([dropped_item, target_item, None])
                return
            elif location == 1:
                self.drag_add.emit([dropped_item, target_item, target_item.parent_item])
                return

        super(_ModuleOutlinerList, self).drop_event(target_item, event_args)
