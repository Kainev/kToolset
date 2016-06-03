# Python Imports
from functools import partial

# Maya Imports
from maya import OpenMayaUI as OpenMayaUI
from maya.OpenMayaUI import MQtUtil
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin, MayaQDockWidget

# PySide Imports
import PySide.QtGui as qg
import PySide.QtCore as qc
from shiboken import wrapInstance

# KAR Imports
import KAR_scene
import ui as kui; reload(kui)

# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# INITIALIZE FUNCTION
# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
kAuto_rig_ui = None
app_running = False


def initialize():
    """
    Initializes the UI (which in turns creates an instance of the kAutoRigger Tool)
    and calls its run function to show the window. If an instance is already running
    then this function has no effect.
    """
    global app_running
    global kAuto_rig_ui

    if not app_running:
        app_running = True
        kAuto_rig_ui = None

        if kAuto_rig_ui is None:
            kAuto_rig_ui = KAutoRiggerUI()
            kAuto_rig_ui.run()
    else:
        kAuto_rig_ui.run()


# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# MAIN UI
# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
class KAutoRiggerUI(MayaQWidgetDockableMixin, qg.QMainWindow):
    """
    Main UI for the kAutoRigger. Handles all aspects of the UI and the interfacing between this UI
    and the kAutoRigger Tool itself.
    """

    TOOL_NAME = 'kAutoRigger'

    def __init__(self):
        """
        Sets the KAutoRiggerUI docks main window preferences, establishes the layout and initializes all
        other windows/docks.
        """
        self.delete_instances()
        super(self.__class__, self).__init__(parent=self.get_maya_window())

        # kAutoRigger Tool
        self.scene = KAR_scene.Scene()

        # Window settings
        self.setObjectName(self.__class__.TOOL_NAME)
        self.setWindowFlags(qc.Qt.WindowStaysOnTopHint)
        self.resize(600, 400)
        self.setWindowTitle('kAutoRigger')
        # self.setStyleSheet(ui_generic.getMainStyleSheet()) ## GET MAIN STYLE SHEET
        self.statusBar().showMessage("Ready")

        # Initialize the main window's menu bar
        self._init_menu_bar()

        # Setup tabs
        self._tab_widget = kui.widgets.TabWidget()
        self.setCentralWidget(self._tab_widget)
        self._tab_widget.add_tab(label='Modules', content_widget=kui.ModuleAttributeEditor(self.scene), selected=True)

    # ---------------------------------------------------------------------------------------------------------------- #

    def _init_menu_bar(self):
        """
        Creates the main window's menu bar, adds the actions ('options') and sets their 'triggered' signal
        connections to the corresponding function (i.e. pressing Save Rig triggers the rig save function).
        """
        # ----------------------------------------------------------------------------#
        # Menu Bar -------------------------------------------------------------------#
        menu_bar = self.menuBar()
        # Create menus
        file_menu = menu_bar.addMenu('&File')
        edit_menu = menu_bar.addMenu('&Edit')
        windows_menu = menu_bar.addMenu('&Windows')
        help_menu = menu_bar.addMenu('&Help')
        # Make menus tear-able
        file_menu.setTearOffEnabled(True)
        edit_menu.setTearOffEnabled(True)
        windows_menu.setTearOffEnabled(True)
        help_menu.setTearOffEnabled(True)

        # ---------------------------------------------------------------------------#
        # ACTIONS -------------------------------------------------------------------#

        # FILE MENU -----------------------------------------------------------------#
        file_menu.setFixedWidth(215)
        # Actions
        file_action_new_rig = qg.QAction('New Rig', self)
        file_action_open_rig = qg.QAction('Open Rig', self)
        file_action_save_rig = qg.QAction('Save Rig', self)
        file_action_save_rig_as = qg.QAction('Save Rig As..', self)
        file_action_save_preset = qg.QAction('Save Preset', self)
        file_action_import_preset = qg.QAction('Import Preset', self)
        file_action_exit = qg.QAction('Exit', self)
        # Functionality
        file_action_new_rig.triggered.connect(self.display_in_dev_message)
        file_action_open_rig.triggered.connect(self.display_in_dev_message)
        file_action_save_rig.triggered.connect(self.display_in_dev_message)
        file_action_save_rig_as.triggered.connect(self.display_in_dev_message)
        file_action_save_preset.triggered.connect(self.display_in_dev_message)
        file_action_import_preset.triggered.connect(self.display_in_dev_message)
        file_action_exit.triggered.connect(self.exit)
        # Add Actions
        file_menu.addAction(file_action_new_rig)
        file_menu.addAction(file_action_open_rig)
        file_sep01 = file_menu.addSeparator()
        file_sep01.setText('Save')
        file_menu.addAction(file_action_save_rig)
        file_menu.addAction(file_action_save_rig_as)
        file_sep02 = file_menu.addSeparator()
        file_sep02.setText('Preset')
        file_menu.addAction(file_action_save_preset)
        file_menu.addAction(file_action_import_preset)
        file_menu.addSeparator()
        file_menu.addAction(file_action_exit)

        # WINDOWS MENU --------------------------------------------------------------#
        windows_menu.setFixedWidth(215)
        # Actions
        win_action_module_outliner = qg.QAction('Module Outliner', self)
        win_action_avail_modules = qg.QAction('Available Modules', self)
        win_action_parent_editor = qg.QAction('Parent Editor', self)
        win_action_placement_systems = qg.QAction('Placement Editor', self)
        win_action_space_editor = qg.QAction('Space Editor', self)
        # Functionality
        win_action_module_outliner.triggered.connect(self.display_in_dev_message)
        win_action_avail_modules.triggered.connect(self.display_in_dev_message)
        win_action_parent_editor.triggered.connect(self.display_in_dev_message)
        win_action_placement_systems.triggered.connect(self.display_in_dev_message)
        win_action_space_editor.triggered.connect(self.display_in_dev_message)
        # Add Actions
        windows_menu.addAction(win_action_module_outliner)
        windows_menu.addAction(win_action_avail_modules)
        win_sep01 = windows_menu.addSeparator()
        win_sep01.setText('Editors')
        windows_menu.addAction(win_action_parent_editor)
        windows_menu.addAction(win_action_placement_systems)
        windows_menu.addAction(win_action_space_editor)

        # HELP MENU --------------------------------------------------------------#
        help_menu.setFixedWidth(215)
        # Actions
        help_action_about = qg.QAction('About', self)
        help_action_update = qg.QAction('Check for Updates..', self)
        help_action_docs = qg.QAction('Documentation', self)
        help_action_website = qg.QAction('Developer Website', self)
        # Functionality
        help_action_about.triggered.connect(self.display_in_dev_message)
        help_action_update.triggered.connect(self.display_in_dev_message)
        help_action_docs.triggered.connect(self.display_in_dev_message)
        help_action_website.triggered.connect(self.display_in_dev_message)
        # Add Actions
        help_menu.addAction(help_action_about)
        help_menu.addSeparator()
        help_menu.addAction(help_action_update)
        help_menu.addSeparator()
        help_menu.addAction(help_action_docs)
        help_menu.addAction(help_action_website)

    # ---------------------------------------------------------------------------------------------------------------- #
    # ---------------------------------------------------------------------------------------------------------------- #
    # OPEN/CLOSE FUNCTIONS FOR UI
    # ---------------------------------------------------------------------------------------------------------------- #
    # ---------------------------------------------------------------------------------------------------------------- #
    def run(self):
        """
        Shows the UI
        """
        self.show(dockable=True)

    def exit(self):
        """
        Runs the delete_instances function and sets the global variable app_running to False

        This method completely deletes the UI and kAutoRigger Tool. Any unsaved progress is lost.
        """

        exit_message = "Unsaved progress will be lost.. continue?"
        user_reply = qg.QMessageBox.question(self, 'Exit kAutoRigger', exit_message,
                                             qg.QMessageBox.Yes, qg.QMessageBox.No)

        if user_reply == qg.QMessageBox.Yes:
            global app_running
            app_running = False
            self.delete_instances()
        else:
            pass

    def dockCloseEventTriggered(self):
        """
        Overrides default dockCloseEventTriggered to have no effect. This results in the UI window
        simply being hidden but not closed.

        The user must press the 'Exit' button from the 'File' menu to completely quit the application.
        """
        pass

    def delete_instances(self):
        """
        Deletes all instances of the UI dock
        """
        maya_main_window = self.get_maya_window()

        # Search all children of the main window to find currently open instances of this UI
        for obj in maya_main_window.children():
            if type(obj) == MayaQDockWidget:
                if obj.widget().objectName() == self.__class__.TOOL_NAME:
                    maya_main_window.removeDockWidget(obj)
                    obj.setParent(None)
                    obj.deleteLater()

    @staticmethod
    def get_maya_window():
        # Get Mayas window wrapped as a widget
        maya_main_window_ptr = OpenMayaUI.MQtUtil.mainWindow()
        maya_main_window = wrapInstance(long(maya_main_window_ptr),
                                        qg.QMainWindow)

        return maya_main_window

    # ---------------------------------------------------------------------------------------------------------------- #
    # ---------------------------------------------------------------------------------------------------------------- #
    # MISC FUNCTIONS
    # ---------------------------------------------------------------------------------------------------------------- #
    # ---------------------------------------------------------------------------------------------------------------- #
    def display_in_dev_message(self):
        """
        Displays a message box informing the user that the feature they have just attempted
        to use is unavailable as it is still in development.
        """
        message = "Feature Unavailable: In Development"
        qg.QMessageBox.question(self, 'Development', message, qg.QMessageBox.Ok)
