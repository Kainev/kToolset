# Python Imports
from functools import partial

# Maya Imports
import maya.cmds as cmds

# PySide Imports
import PySide.QtCore as qc
import PySide.QtGui as qg

# KAR Imports
from kToolset.kToolset.rigging.kar.utils import KAR_uiUtils as kuiUtils; reload(kuiUtils)

class TabWidget(qg.QWidget):
    """
    Widget for creating a tab menu that switches between different widgets
    """

    SELECTED = 'selected'  # Constant for setting the selected property of buttons

    def __init__(self, parent=None):
        """
        Sets main layout for widget and establishes
        """
        super(TabWidget, self).__init__(parent=parent)

        self._tab_buttons = []

        self.setStyleSheet(kuiUtils.get_style_sheet('stylesheet_tabWidget'))
        self.setLayout(qg.QVBoxLayout())
        self.layout().setContentsMargins(2, 2, 2, 2)
        self.layout().setSpacing(0)

        self.lay_tabs = qg.QHBoxLayout()
        self.lay_tabs.setAlignment(qc.Qt.AlignLeft)
        self.lay_tabs.setContentsMargins(0, 0, 0, 0)
        self.lay_tabs.setSpacing(2)
        self.layout().addLayout(self.lay_tabs)

        self.content_frame = qg.QFrame()
        self.content_frame.setFrameStyle(qg.QFrame.Panel | qg.QFrame.Raised)
        self.content_frame.setLayout(qg.QStackedLayout())
        self.content_frame.layout().setContentsMargins(0, 0, 0, 0)
        self.content_frame.layout().setSpacing(0)
        self.layout().addWidget(self.content_frame)


    def add_tab(self, label, content_widget, selected=False):
        """
        Adds a new tab and associates it with the given content_widget

        :param label: String: Text to display on tab button
        :param content_widget: QWidget: Widget to display when tab is selected
        :param selected: Boolean: If True, this tab is set to be the selected tab
        :return:
        """
        # Validate parameters
        if label in self._tab_buttons:
            cmds.warning("Cannot add tab. Name: '%s' is not unique.." % label)
            return

        if not isinstance(label, str):
            cmds.warning("Name: '%s' must be of type: Str" % label)
            return

        if len(self._tab_buttons) > 0:
            index = len(self._tab_buttons)
        else:
            index = 0

        # Create a new button to use as a tab
        self._tab_buttons.append(qg.QPushButton(label))
        self._tab_buttons[-1].setObjectName('tab')
        self._tab_buttons[-1].setFixedWidth(100)
        self._tab_buttons[-1].clicked.connect(partial(self._update_selection, index))

        if not selected:
            self._tab_buttons[-1].setProperty(self.SELECTED, False)
        elif selected:
            self._tab_buttons[-1].setProperty(self.SELECTED, True)
            self._update_selection(-1)

        self.lay_tabs.addWidget(self._tab_buttons[-1])
        self.content_frame.layout().addWidget(content_widget)

    def _update_selection(self, tab_index):
        """
        Given a tab index, changes the current tab selection and updates the stacked layout
        to display the corresponding content widget

        :param tab_index: Index of tab and content widget to display
        :return:
        """
        try:
            self.content_frame.layout().setCurrentIndex(tab_index)
        except IndexError:
            cmds.warning("Content Widget at index '%s' does not exist.." % tab_index)
            return

        try:
            for index, tab_button in enumerate(self._tab_buttons):
                if index != tab_index:
                    tab_button.setProperty(self.SELECTED, False)
                elif index == tab_index:
                    tab_button.setProperty(self.SELECTED, True)

                self.style().unpolish(tab_button)
                self.style().polish(tab_button)
        except IndexError:
            cmds.warning("Tab Button at index '%s' does not exist.." % tab_index)
            return


