# Python Imports
from functools import partial

# Maya Imports
from maya import OpenMayaUI as OpenMayaUI
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from maya.app.general.mayaMixin import MayaQDockWidget
from maya.OpenMayaUI import MQtUtil

# PySide imports
from shiboken import wrapInstance
import PySide.QtGui as qg
import PySide.QtCore as qc


class KAutoRiggerUI(MayaQWidgetDockableMixin, qg.QMainWindow):
    """
    Main UI for the kAutoRigger. Handles all aspects of the UI and the interfacing between this UI
    and the kAutoRigger Tool itself.
    """

    TOOL_NAME = 'kAutoRigger'

    def __init__(self, parent=None):
        """
        Sets the KAutoRiggerUI docks main window preferences, establishes the layout and initializes all
        other windows/docks.
        """
        self.delete_instances()
        super(self.__class__, self).__init__(parent=parent)
        
        maya_main_window_ptr = OpenMayaUI.MQtUtil.mainWindow()
        self.maya_main_window = wrapInstance(long(maya_main_window_ptr), qg.QMainWindow)
        self.setObjectName(self.__class__.TOOL_NAME)  # Make this unique enough if using it to clear previous instance!

        # Window settings
        self.setWindowFlags(qc.Qt.WindowStaysOnTopHint)
        self.setWindowTitle('kAutoRigger')
        # self.setStyleSheet(ui_generic.getMainStyleSheet()) ## GET MAIN STYLE SHEET
        self.statusBar().showMessage("Ready")

        # Menu Bar
        menu_bar = self.menuBar()
        # Establish menus
        self.file_menu = menu_bar.addMenu('&File')
        self.edit_menu = menu_bar.addMenu('&Edit')
        self.windows_menu = menu_bar.addMenu('&Windows')
        self.help_menu = menu_bar.addMenu('&Help')
        # Make menus tear-able
        self.file_menu.setTearOffEnabled(True)
        self.edit_menu.setTearOffEnabled(True)
        self.windows_menu.setTearOffEnabled(True)
        self.help_menu.setTearOffEnabled(True)

        self._add_actions()

    # ---------------------------------------------------------------------------------------------------------------- #

    def _add_actions(self):
        """
        Adds the actions ('options') to the main windows menu bar and sets their 'triggered' signal connection
        to the corresponding function (i.e. pressing Save Rig triggers the rig save function).
        """
        # FILE MENU -----------------------------------------------------------------#
        self.file_menu.setFixedWidth(215)

        # Actions
        file_action_new_rig = qg.QAction('New Rig', self)
        file_action_open_rig = qg.QAction('Open Rig', self)
        file_action_save_rig = qg.QAction('Save Rig', self)
        file_action_save_rig_as = qg.QAction('Save Rig As..', self)
        file_action_save_preset = qg.QAction('Save Preset', self)
        file_action_import_preset = qg.QAction('Import Preset', self)
        file_action_exit = qg.QAction('Exit', self)

        # Add Actions
        self.file_menu.addAction(file_action_new_rig)
        self.file_menu.addAction(file_action_open_rig)
        file_sep01 = self.file_menu.addSeparator()
        file_sep01.setText('Save')
        self.file_menu.addAction(file_action_save_rig)
        self.file_menu.addAction(file_action_save_rig_as)
        file_sep02 = self.file_menu.addSeparator()
        file_sep02.setText('Preset')
        self.file_menu.addAction(file_action_save_preset)
        self.file_menu.addAction(file_action_import_preset)
        self.file_menu.addSeparator()
        self.file_menu.addAction(file_action_exit)

        # WINDOWS MENU --------------------------------------------------------------#
        self.windows_menu.setFixedWidth(215)

        # Actions
        win_action_module_outliner = qg.QAction('Module Outliner', self, triggered=self.test)
        win_action_avail_modules = qg.QAction('Available Modules', self)
        win_action_parent_editor = qg.QAction('Module Parent Editor', self)
        win_action_placement_systems = qg.QAction('Module Placement Editor', self)
        win_action_space_editor = qg.QAction('Module Space Editor', self)

        # Add Actions
        self.windows_menu.addAction(win_action_module_outliner)
        self.windows_menu.addAction(win_action_avail_modules)
        win_sep01 = self.windows_menu.addSeparator()
        win_sep01.setText('Editors')
        self.windows_menu.addAction(win_action_parent_editor)
        self.windows_menu.addAction(win_action_placement_systems)
        self.windows_menu.addAction(win_action_space_editor)

    # ---------------------------------------------------------------------------------------------------------------- #
    # ---------------------------------------------------------------------------------------------------------------- #
    # OPEN/CLOSE FUNCTIONS FOR UI
    # ---------------------------------------------------------------------------------------------------------------- #
    # ---------------------------------------------------------------------------------------------------------------- #

    def dockCloseEventTriggered(self):
        """
        Overrides default dockCloseEventTriggered method to run custom delete function

        NOTES: Potentially change this function to only hide the UI instead of deleting it,
        as the autoRig tool is created from this instance of the UI, if the window is closed
        all auto rigging progress will be gone.
        """
        global ui_open
        ui_open = False
        self.delete_instances()

    def delete_instances(self):
        """
        Deletes all instances of the UI dock
        """
        # Get Mayas window wrapped as a widget
        maya_main_window_ptr = OpenMayaUI.MQtUtil.mainWindow()
        maya_main_window = wrapInstance(long(maya_main_window_ptr),
                                        qg.QMainWindow)

        # Search all children of the main window to find currently open instances of this UI
        for obj in maya_main_window.children():
            if type(obj) == MayaQDockWidget:
                if obj.widget().objectName() == self.__class__.TOOL_NAME:
                    maya_main_window.removeDockWidget(obj)
                    obj.setParent(None)
                    obj.deleteLater()

    def run(self):
        """
        Shows the UI
        """
        self.show(dockable=True)

    
# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# CREATE FUNCTION
# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #

kAuto_rig_ui = None
ui_open = False


def create():
    """
    Initializes the UI (which in turns creates an instance of the kAutoRigger Tool)
    and calls it's run function to show the window. If an instance is already running
    then this function has no effect.
    """
    global ui_open

    if not ui_open:
        ui_open = True

        global kAuto_rig_ui
        if kAuto_rig_ui is None:
            kAuto_rig_ui = KAutoRiggerUI()
        kAuto_rig_ui.run()