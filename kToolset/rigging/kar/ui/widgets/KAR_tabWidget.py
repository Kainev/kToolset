# Maya Imports
import maya.cmds as cmds

# PySide Imports
import PySide.QtCore as qc
import PySide.QtGui as qg

class TabWidget(qg.QWidget):
    """
    Widget for creating a tab menu that switches between different widgets
    """

    SELECTED = 'selected' # Constant for setting the selected property of buttons

    def __init__(self):
        """
        Sets main layout for widget and establishes
        """
        super(TabWidget, self).__init__()

        self._tab_buttons = []

        self.setLayout(qg.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

        self.lay_tabs = qg.QHBoxLayout()
        self.lay_tabs.setAlignment(qc.Qt.AlignLeft)
        self.lay_tabs.setContentsMargins(0, 0, 0, 0)
        self.lay_tabs.setSpacing(2)
        self.layout().addLayout(self.lay_tabs)

        self.lay_content = qg.QStackedLayout()
        self.lay_content.setContentsMargins(0, 0, 0, 0)
        self.lay_content.setSpacing(0)
        self.layout().addLayout(self.lay_content)


    def add_tab(self, name, content_widget, selected=False):
        """
        Adds a new tab and associates it with the given content_widget

        :param name: String: Text to display on tab button
        :param content_widget: QWidget: Widget to display when tab is selected
        :param selected: Boolean: If True, this tab is set to be the selected tab
        :return:
        """
        # Validate parameters
        if name in self._tab_buttons:
            cmds.warning("Cannot add tab. Name: '%s' is not unique.." % name)
            return

        if not isinstance(name, str):
            cmds.warning("Name: '%s' must be of type: Str" % name)
            return

        # Create a new button to use as a tab
        self._tab_buttons.append(qg.QPushButton(name))
        # Find the index of the button (it will always be the last element)
        index = self._tab_buttons.index(qg.QPushButton(name))
        self._tab_buttons[index].setFixedWidth(100)
        self._tab_buttons[index].clicked.connect(partial(self._tab_selected, index))

        if not selected:
            self._tab_buttons[index].setProperty(self.SELECTED, False)
        elif selected:
            self._tab_buttons[index].setProperty(self.SELECTED, True)
            self._update_selection(index)

        self.lay_tabs.addWidget(self._tab_buttons[index])
        self.lay_tabs.addWidget(content_widget)

    def _update_selection(self, tab_index):
        """
        Given a tab index, changes the current tab selection and updates the stacked layout
        to display the corresponding content widget

        :param tab_index: Index of tab and content widget to display
        :return:
        """
        try:
            self.lay_content.setCurrentIndex(tab_index)
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


