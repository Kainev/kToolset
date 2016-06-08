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
import KAR_scene; reload(KAR_scene)
import ui as kui; reload(kui)

# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# INITIALIZE FUNCTION
# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
MainUI = None
app_running = False


def initialize():
    """
    Initializes the UI (which in turns creates an instance of the kAutoRigger Tool)
    and calls its run function to show the window. If an instance is already running
    then this function has no effect.
    """
    global app_running
    global MainUI

    if not app_running:
        app_running = True
        MainUI = None

        if MainUI is None:
            MainUI = KAutoRiggerUI()
            MainUI.run()
    else:
        MainUI.run()


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
        self.setDockOptions(qg.QMainWindow.AnimatedDocks | qg.QMainWindow.AllowNestedDocks |
                            qg.QMainWindow.AllowTabbedDocks | qg.QMainWindow.VerticalTabs)
        self.resize(920, 500)

        self.setWindowTitle('kAutoRigger')
        # self.setStyleSheet(ui_generic.getMainStyleSheet()) ## GET MAIN STYLE SHEET
        self.statusBar().showMessage("Ready")

        # Docks
        self.docks = {}
        self._init_docks()

        # Initialize the main window's menu bar
        self._init_menu_bar()

        # Main Tabs
        tab_widget = kui.widgets.TabWidget(parent=self)
        self.setCentralWidget(tab_widget)
        tab_widget.add_tab('Module Settings', kui.ModuleAttributeEditor(self.scene), True)
        tab_widget.add_tab('Skinning', qg.QWidget(parent=self))
        tab_widget.add_tab('Blend Shapes', qg.QWidget(parent=self))
        tab_widget.add_tab('Publish', qg.QWidget(parent=self))
    # ---------------------------------------------------------------------------------------------------------------- #

    # ---------------------------------------------------------------------------------------------------------------- #
    # ---------------------------------------------------------------------------------------------------------------- #
    # Build UI functions
    # ---------------------------------------------------------------------------------------------------------------- #
    # ---------------------------------------------------------------------------------------------------------------- #
    def _init_docks(self):
        # Add hidden docks here
        self.docks['placement_editor'] = kui.PlacementEditor(self.scene, parent=self)

        for dock in self.docks:
            self.docks[dock].hide()
            self.addDockWidget(qc.Qt.LeftDockWidgetArea, self.docks[dock], qc.Qt.Horizontal)

        # Add docks to show initially on startup
        self.docks['available_modules'] = kui.AvailableModules(self.scene, parent=self)
        self.docks['module_outliner'] = kui.ModuleOutliner(self.scene, main_ui=self, parent=self)

        self.addDockWidget(qc.Qt.LeftDockWidgetArea, self.docks['available_modules'], qc.Qt.Horizontal)
        self.addDockWidget(qc.Qt.LeftDockWidgetArea, self.docks['module_outliner'], qc.Qt.Horizontal)

    def _show_dock(self, dock_name):
        try:
            self.docks[dock_name].show()
        except KeyError:
            pass

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
        edit_submenu_placement = edit_menu.addMenu('Placement Systems')
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

        # EDIT MENU -----------------------------------------------------------------#
        edit_menu.setFixedWidth(215)
        # Actions
        edit_action_placement_create_all = qg.QAction('Create All', self)
        edit_action_placement_delete_all = qg.QAction('Delete All', self)
        edit_action_placement_create_sel = qg.QAction('Create Selected', self)
        edit_action_placement_delete_sel = qg.QAction('Delete Selected', self)
        edit_action_placement_reset_all = qg.QAction('Reset All', self)
        edit_action_placement_reset_sel = qg.QAction('Reset Selected', self)
        edit_action_placement_toggle_geo = qg.QAction('Toggle Geometry', self)

        # Functionality
        edit_action_placement_create_all.triggered.connect(self.display_in_dev_message)
        edit_action_placement_delete_all.triggered.connect(self.display_in_dev_message)
        edit_action_placement_create_sel.triggered.connect(self.display_in_dev_message)
        edit_action_placement_delete_sel.triggered.connect(self.display_in_dev_message)
        edit_action_placement_reset_all.triggered.connect(self.display_in_dev_message)
        edit_action_placement_reset_sel.triggered.connect(self.display_in_dev_message)
        edit_action_placement_toggle_geo.triggered.connect(self.display_in_dev_message)

        # Add Actions
        edit_sep01 = edit_submenu_placement.addSeparator()
        edit_sep01.setText('All')
        edit_submenu_placement.addAction(edit_action_placement_create_all)
        edit_submenu_placement.addAction(edit_action_placement_delete_all)
        edit_sep02 = edit_submenu_placement.addSeparator()
        edit_sep02.setText('Selected')
        edit_submenu_placement.addAction(edit_action_placement_create_sel)
        edit_submenu_placement.addAction(edit_action_placement_delete_sel)
        edit_sep03 = edit_submenu_placement.addSeparator()
        edit_sep03.setText('Reset')
        edit_submenu_placement.addAction(edit_action_placement_reset_all)
        edit_submenu_placement.addAction(edit_action_placement_reset_sel)
        edit_sep04 = edit_submenu_placement.addSeparator()
        edit_submenu_placement.addAction(edit_action_placement_toggle_geo)

        # WINDOWS MENU --------------------------------------------------------------#
        windows_menu.setFixedWidth(215)
        # Actions
        win_action_module_outliner = qg.QAction('Module Outliner', self)
        win_action_avail_modules = qg.QAction('Available Modules', self)
        win_action_parent_editor = qg.QAction('Parent Editor', self)
        win_action_placement_systems = qg.QAction('Placement Editor', self)
        win_action_space_editor = qg.QAction('Space Editor', self)
        win_action_global_settings = qg.QAction('Global Settings', self)
        # Functionality
        win_action_module_outliner.triggered.connect(partial(self._show_dock, 'module_outliner'))
        win_action_avail_modules.triggered.connect(partial(self._show_dock, 'available_modules'))
        win_action_parent_editor.triggered.connect(self.display_in_dev_message)
        win_action_placement_systems.triggered.connect(partial(self._show_dock, 'placement_editor'))
        win_action_space_editor.triggered.connect(self.display_in_dev_message)
        win_action_global_settings.triggered.connect(self.display_in_dev_message)
        # Add Actions
        windows_menu.addAction(win_action_module_outliner)
        windows_menu.addAction(win_action_avail_modules)
        win_sep01 = windows_menu.addSeparator()
        win_sep01.setText('Editors')
        windows_menu.addAction(win_action_parent_editor)
        windows_menu.addAction(win_action_placement_systems)
        windows_menu.addAction(win_action_space_editor)
        win_sep02 = windows_menu.addSeparator()
        windows_menu.addAction(win_action_global_settings)

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

    @staticmethod
    def get_maya_window():
        """
        Returns Maya's Main Window wrapped as a QWidget
        :return:
        """
        # Get Mayas window wrapped as a widget
        maya_main_window_ptr = OpenMayaUI.MQtUtil.mainWindow()
        maya_main_window = wrapInstance(long(maya_main_window_ptr),
                                        qg.QMainWindow)

        return maya_main_window
