# Python Imports
import uuid
from functools import partial
import re
# PySide Imports
import PySide.QtCore as qc
import PySide.QtGui as qg
# KAR Imports
from kToolset.kToolset.rigging.kar.utils import KAR_uiUtils as kuiUtils; reload(kuiUtils)

import pydoc

"""
NOTES:
Implement the option to display the widgets parent name on the right side of the list item properly.
Add variable to turn display of parent name on/off. When on, add parent text width into minimumWidth calculation
and work out correct x position to draw text. Align parent text right.
"""


# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# LIST
# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #

class ListWidget(qg.QWidget):
    """
    To Write..
    """

    # SIGNALS
    order_changed = qc.Signal(list)

    def __init__(self, parent=None, drag_enabled=True, drop_enabled=True):
        super(ListWidget, self).__init__(parent=parent)

        self.setStyleSheet(kuiUtils.get_style_sheet('stylesheet_listWidget'))

        self._multi_select = True
        self._item_display_state = 0  # 0 = No Icons, 1 = Small Icons, 2 = Large Icons

        self._items = []
        self._selected_items = []

        # Master Widget Layout
        self.setLayout(qg.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

        # Create Scroll Area for list
        self.scroll_area = qg.QScrollArea()
        self.scroll_area.setObjectName('darkList')
        self.scroll_area.setFocusPolicy(qc.Qt.NoFocus)
        self.scroll_area.setWidgetResizable(True)
        self.layout().addWidget(self.scroll_area)

        # List widget
        self.list_widget = qg.QWidget()
        self.list_widget.setObjectName('darkList')
        self.list_widget.setLayout(qg.QVBoxLayout())
        self.list_widget.layout().setContentsMargins(0, 0, 0, 0)
        self.list_widget.layout().setSpacing(0)
        self.list_widget.layout().setAlignment(qc.Qt.AlignTop)

        self.scroll_area.setWidget(self.list_widget)

        self.drag_enabled = drag_enabled
        self.drop_enabled = drop_enabled

        if self.drop_enabled:
            self._world_item = _ItemWidget(label='', icon_pixmap=None, data=None, parent=self.list_widget)
            self._world_item.received_drop.connect(partial(self.drop_event, self._world_item))
            self._world_item.setFixedHeight(24)
            self._world_item.paintEvent = self.override_function
            self.setAcceptDrops(True)

    # ---------------------------------------------------------------------------------------------------------------- #
    # ---------------------------------------------------------------------------------------------------------------- #
    # List Item Manipulation Functions
    # ---------------------------------------------------------------------------------------------------------------- #
    # ---------------------------------------------------------------------------------------------------------------- #
    def add_item(self, label, icon_pixmap=None, data=None):
        """
        Adds a new item to the list.

        :param label: Text to display on list item
        :param icon_pixmap: QPixmap to display on the left of text
        :param data: Arbitrary variable to store any required data, such as an identifier
        :returns Newly created _ListWidget
        """
        item = _ItemWidget(label, icon_pixmap, data, parent=self, drag_enabled=self.drag_enabled, drop_enabled=self.drop_enabled)
        self.list_widget.layout().addWidget(item)
        self._items.append(item)

        # Listen for drop events
        item.received_drop.connect(partial(self.drop_event, item))
        item.clicked.connect(partial(self._selection_updated, item))

        self.update_world_item()

        return item

    def update_world_item(self):
        """
        Moves the world item (blank _ListItem) to the bottom of the list

        The world item exists so the user can always drag an item back to world space and un-parent it from its
        current parent
        """
        if self.drop_enabled:
            self.list_widget.layout().addWidget(self._world_item)

    def move_and_parent(self, child_item, parent_item):
        """
        Sets the parent of a given item and moves that item visually underneath
        its new parent
        """
        child_children = self.get_children(child_item)

        if parent_item in child_children:
            print('Cannot parent child to grandchild..')
            return

        child_item.set_parent(parent_item)
        self.move_item_under(child_item, parent_item)

    def move_item_under(self, move_item, target_item):
        """
        Moves given _ListItem (and all children/grandchildren) visually underneath a target _ListItem

        This is essentially a convenience function that calculates the index change value and then
        calls the move_item_by function.
        """
        parent_index = self.list_widget.layout().indexOf(target_item)
        child_index_original = self.list_widget.layout().indexOf(move_item)

        index_change = parent_index - child_index_original + 1

        if child_index_original < parent_index:
            index_change -= 1

        self.move_item_by(move_item, index_change)

    def move_item_by(self, move_item, index_change):
        """
        Given an item, moves it and all of its children visually by a given number
        of positions

        :param move_item: Top most _ListItem of hierarchy to move
        :param index_change: int: number of places in list to move
        """
        children = [move_item] + self.get_children(move_item)

        for child in children:
            child_index = self.list_widget.layout().indexOf(child)
            self.list_widget.layout().insertWidget(child_index + index_change, child)
            child.update()

        self.update_world_item()

    # ---------------------------------------------------------------------------------------------------------------- #
    # ---------------------------------------------------------------------------------------------------------------- #
    # List Events
    # ---------------------------------------------------------------------------------------------------------------- #
    # ---------------------------------------------------------------------------------------------------------------- #
    def _selection_updated(self, selected_item):
        if self._multi_select:
            modifiers = qg.QApplication.keyboardModifiers()

            if modifiers == qc.Qt.ControlModifier:
                if selected_item not in self._selected_items:
                    self._selected_items.append(selected_item)
                elif selected_item in self._selected_items:
                    self._selected_items.remove(selected_item)
            elif modifiers == qc.Qt.ShiftModifier:
                try:
                    last_disp_index = self.list_widget.layout().indexOf(self._selected_items[0])
                except IndexError:
                    last_disp_index = None

                selected_disp_index = self.list_widget.layout().indexOf(selected_item)

                if last_disp_index is not None:
                    new_indices = range(min(selected_disp_index, last_disp_index),
                                        max(selected_disp_index, last_disp_index)+1)
                else:
                    new_indices = [selected_disp_index]

                self._selected_items += [self.list_widget.layout().itemAt(index).widget()
                                         for index in new_indices
                                         if self.list_widget.layout().itemAt(index).widget()
                                         not in self._selected_items]

            else:
                self._selected_items[:] = []
                if selected_item is not None:
                    self._selected_items.append(selected_item)

        for item in self._items:
            if item not in self._selected_items:
                item.selected = False
            elif item in self._selected_items:
                item.selected = True

    def remove_selected(self):
        """
        Removes all currently selected items and their children
        """
        # Make sure there is something to delete
        if len(self._selected_items) is 0:
            return

        deletion_items = []

        # Mark selected items for deletion
        for selected_item in self._selected_items:
            # Delete selected item
            if selected_item not in deletion_items:
                deletion_items.append(selected_item)

            # Delete children of selected item
            for item in self.get_children(selected_item):
                if item not in deletion_items:
                    deletion_items.append(item)

        # Delete items
        for item in deletion_items:
            del self._items[self._items.index(item)]
            self.list_widget.layout().removeWidget(item)
            item.deleteLater()

        # Make sure selection is cleared
        self._selection_updated(None)

    def remove_all(self):
        """
        Removes all items from the list
        """
        for item in self._items:
            self.list_widget.layout().removeWidget(item)
            item.deleteLater()

        self._items[:] = []
        self._selection_updated(None)

    def rename_selected(self, text):
        if isinstance(text, unicode):
            for item in self._selected_items:
                if not self._force_unique_names:
                    item.text = text
                else:
                    item.text = self._generate_unique_name(text)

    def dragEnterEvent(self, event):
        if self.drop_enabled:
            event.accept()

    def dropEvent(self, event):
        item = event.source()

        # Parent item to world and move to bottom of list
        event_items = self.resolve_drag_items(item)
        print event_items
        for event_item in event_items:
            event_item.parent_item = None
            event_item.update()
            self.move_item_under(event_item, self.get_display_order(self._items, reverse=True)[-1])

    def drop_event(self, target_item, event_args):
        """
        drop_event is triggered when the user drags and drops one list item onto another.
        If the item is dropped onto the top/middle section of another item, then it is parented
        underneath the target item.

        If the dropped item is dropped onto the bottom portion of a list item, it is moved underneath that item
        and inherits that items parent, rather than being parented to the item itself.

        :param target_item: _ListItem instance that was dropped onto
        :param event_args: List: [0] = instance of _ListItem that was dragged
                                 [1] = int representing position of drop, 0 = top/middle, 1 = bottom
        """
        # If drag/drop is disabled, return out of function.
        # There shouldn't be any calls to this function when disabled however
        # I'm a cautious cat
        if not self.drop_enabled:
            return

        dropped_item, location = event_args

        # If item is dropped on the blank world item (at bottom of list), parent the dropped item to the world
        # and move it to the bottom of the list (above blank world item)
        if target_item == self._world_item:
            dropped_item.parent_item = None
            dropped_item.update()
            self.move_item_under(dropped_item, self.get_display_order(self._items)[-1])
            return

        # Determines which items the event should apply to in case the user is dragging a selection
        event_items = self.resolve_drag_items(dropped_item)

        for item in event_items:
            # Make sure user is not trying to parent an item to one of its children
            if target_item in self.get_children(item):
                return

            if location == 0:
                self.move_and_parent(item, target_item)
            if location == 1:
                if self.get_children(target_item) != []:
                    self.move_and_parent(item, target_item)
                else:
                    item.parent_item = target_item.parent_item
                    item.update()
                    self.move_item_under(item, target_item)

    def resolve_drag_items(self, source_item):
        event_items = []
        if source_item in self._selected_items:
            event_items += self._selected_items
            event_items = self.get_display_order(event_items, reverse=True)
        else:
            self._selection_updated(None)
            self._selection_updated(source_item)
            event_items.append(source_item)

        return event_items

    def get_selected_data(self, hierarchy=False):
        """
        Returns a list containing the data from each selected item. If Hierarchy is True, then the data
        of each selected items children is also returned.

        The list is returned in the order in which the items are displayed

        :param hierarchy: Boolean: If true, the data from all selected item's children is also returned
        """
        items = []

        # Mark selected items for deletion
        for selected_item in self._selected_items:
            # Delete selected item
            if selected_item not in items:
                items.append(selected_item)

            if hierarchy:
                # Delete children of selected item
                for item in self.get_children(selected_item):
                    if item not in items:
                        items.append(item)

        return [item.data for item in self.get_display_order(items)]

    def get_all_data(self):
        """
        Returns a list containing the contents of each items data attribute

        The list is returned in the order in which the items are display
        """
        return [item.data for item in self.get_display_order(self._items)]

    def get_selected_items(self, hierarchy=False):
        """
        Returns a list containing the currently selected list item widgets. If Hierarchy is True, then the child items
        of each item are also returned.

        The list is returned in the order in which the items are displayed

        :param hierarchy: Boolean: If true, all selected item's children are also returned
        """
        items = []

        # Mark selected items for deletion
        for selected_item in self._selected_items:
            # Delete selected item
            if selected_item not in items:
                items.append(selected_item)

            if hierarchy:
                # Delete children of selected item
                for item in self.get_children(selected_item):
                    if item not in items:
                        items.append(item)

        return items

    def get_all_items(self):
        """
        Returns a list containing all current list items, ordered as they appear in the outliner (top to bottom)
        """
        return self.get_display_order(self._items)

    # ---------------------------------------------------------------------------------------------------------------- #
    # ---------------------------------------------------------------------------------------------------------------- #
    # List Display
    # ---------------------------------------------------------------------------------------------------------------- #
    # ---------------------------------------------------------------------------------------------------------------- #
    def set_icon_state(self, state):
        """
        Sets the display state of all list items icons.

        0 = No Icon
        1 = Small Icon (32px)
        2 = Large Icon (64px)

        :param state: Int: 0 = No Icon, 1 = Small Icon, 2 = Large Icon
        """
        if 0 <= state <= 2:
            for item in self._items:
                item.set_icon_state(state)

    # ---------------------------------------------------------------------------------------------------------------- #
    # ---------------------------------------------------------------------------------------------------------------- #
    # Utility
    # ---------------------------------------------------------------------------------------------------------------- #
    # ---------------------------------------------------------------------------------------------------------------- #
    def get_children(self, parent_item):
        """
        Given a _ListItem, returns a list of all children and grandchildren _ListItem's.

        :param parent_item: The parent _ListItem to find children/grandchildren for
        :return List: All children/grandchildren of given _ListItem
        """
        children = []

        def recursive_search(parent):
            """
            Given a _ListItem, recursively searches through all children and appends
            each one to the children list.

            :param parent: _ListItem of parent to find children/grandchildren for
            """
            for item in self._items:
                if item.parent_item == parent:
                    children.append(item)
                    recursive_search(item)

        recursive_search(parent_item)

        return children

    def get_display_order(self, items, reverse=False, in_place=False):
        """
        Given a list of _ListItems, either returns a new list, or modifies the existing list
        in place to be in the order in which each _ListItem is displayed.

        :param items: List of _ListItems to sort
        :param reverse: Boolean: If true, list is sorted in reverse order
        :param in_place: If True, list is modified in place, if False, a new ordered list
                         is returned.
        :return list
        """
        if not in_place:
            return sorted(items, key=lambda item: self.list_widget.layout().indexOf(item), reverse=reverse)
        if in_place:
            items.sort(items, key=lambda item: self.list_widget.layout().indexOf(item), reverse=reverse)

    def _generate_unique_name(self, text):
        list_names = [item.text for item in self._items]

        try:
            unique_mod = str(max([int(re.findall(r'\d+$', t)[0]) for t in list_names
                                  if re.findall(r'\d+$', t) != []]) + 1)
        except ValueError:
            unique_mod = 1

            return '%s%s' % (text, unique_mod)

    @staticmethod
    def override_function(*args):
        """
        Blank function, returns immediately.

        Used for overriding functions to nullify their effect
        """
        return


# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# ITEM WIDGET
# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
class _ItemWidget(qg.QWidget):
    """
    To Write..
    """
    # SIGNALS
    clicked = qc.Signal()
    received_drop = qc.Signal(list)
    parent_changed = qc.Signal()

    # CONSTANTS
    INDENT = 24

    DEFAULT = 0
    HOVER = 1
    DOWN = 2
    SELECTED = 3
    SELECTED_HOVER = 4

    # PAINTING
    COLOUR_DEFAULT = [50, 50, 50]
    COLOUR_HOVER = [75, 75, 75]
    COLOUR_DOWN = [25, 25, 25]
    COLOUR_SELECTED = [120, 140, 200]
    COLOUR_HOVER_SELECTED = [145, 165, 225]

    _brushes = {DEFAULT: qg.QBrush(qg.QColor(*COLOUR_DEFAULT)),
                HOVER: qg.QBrush(qg.QColor(*COLOUR_HOVER)),
                DOWN: qg.QBrush(qg.QColor(*COLOUR_DOWN)),
                SELECTED: qg.QBrush(qg.QColor(*COLOUR_SELECTED)),
                SELECTED_HOVER: qg.QBrush(qg.QColor(*COLOUR_HOVER_SELECTED))}

    def __init__(self, label, icon_pixmap, data, parent=None, drag_enabled=True, drop_enabled=True):
        super(_ItemWidget, self).__init__(parent=parent)

        # Text Pen
        self._pen_text = qg.QPen(qg.QColor(250, 252, 255), 1, qc.Qt.SolidLine)
        self._pen_border = qg.QPen(qg.QColor(0, 0, 0, 0), 1, qc.Qt.SolidLine)
        self._pen_line = qg.QPen(qg.QColor(*self.COLOUR_HOVER_SELECTED), 1, qc.Qt.SolidLine)

        # IDENTIFIER
        self.uuid = uuid.uuid4()

        self._text = label
        self._icon_pixmap = icon_pixmap
        self.data = data
        self.drag_enabled = drag_enabled
        self.drop_enabled = drop_enabled

        # Widget Settings
        if self.drop_enabled:
            self.setAcceptDrops(True)

        # Hierarchy
        self.parent_item = None
        self._children = []
        self.indent_width = 0

        # Button States
        self._hover = False
        self._is_down = False
        self._selected = False
        self._drag_hover_middle = False
        self._drag_hover_lower = False

        self._icon_size = 32
        self.set_icon_state(1)

        self.setMouseTracking(True)

    def set_parent(self, parent):
        """
        Set the parent of item. This will move the item underneath the parent and apply
        the appropriate indentation

        :param parent: _ListWidget: Widget to set as parent
        """
        self.parent_item = parent

        self.update()

    def update(self):
        """
        Overrides widgets default update event to add extra update functionality.

        Updates:
        Indentation of item
        Forces paintEvent
        """
        if self.parent_item is None:
            self.indent_width = 0
        else:
            try:
                self.indent_width = (self.parent_item.indent_width / self.INDENT + 1) * self.INDENT
            except AttributeError:
                self.indent_width = 0

        super(_ItemWidget, self).update()

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value):
        if isinstance(value, bool):
            self._selected = value
            self.update()

    # ---------------------------------------------------------------------------------------------------------------- #
    # ---------------------------------------------------------------------------------------------------------------- #
    # Painting/Text
    # ---------------------------------------------------------------------------------------------------------------- #
    # ---------------------------------------------------------------------------------------------------------------- #
    @property
    def text(self):
        """
        Returns item's text
        """
        return self._text

    @text.setter
    def text(self, text):
        """
        Sets the list items display text

        :param text: Unicode string to display
        """
        if isinstance(text, unicode):
            self._text = text

            fm = qg.QFontMetrics(qg.QFont())
            text_width = fm.width(text)

            self.setMinimumWidth(self._icon_size + self.indent_width + text_width + 16)

    def set_text_colour(self, rgba):
        """
        Changes the items label colour to RGB or RGBA value.

        :param rgba: Tuple/List: RGB or RGBA. i.e [255, 255,255] or [125, 50, 25, 200]
        """
        try:
            self._pen_text = qg.QPen(qg.QColor(*rgba), 1, qc.Qt.SolidLine)
            self.update()
        except AttributeError:
            pass

    def set_border_colour(self, rgba):
        """
        Updates the pen colour that draws the widgets line border

        :param rgba: Accepts list of RGB or RGBA values from 0-255
        """
        try:
            self._pen_border = qg.QPen(qg.QColor(*rgba), 1, qc.Qt.SolidLine)
            self.update()
        except AttributeError:
            pass

    def set_icon_state(self, state):
        """
        Sets the display state of icon.

        0 = No Icon
        1 = Small Icon (32px)
        2 = Large Icon (64px)

        :param state: Int: 0 = No Icon, 1 = Small Icon, 2 = Large Icon
        """
        if state is 1:
            self._icon_size = 32
            self.setFixedHeight(36)
        elif state is 2:
            self._icon_size = 64
            self.setFixedHeight(80)
        else:
            self._icon_size = 0
            self.setFixedHeight(25)

    def paintEvent(self, event):
        painter = qg.QStylePainter(self)
        painter.setRenderHint(qg.QPainter.Antialiasing)
        option = qg.QStyleOption()
        option.initFrom(self)

        x = option.rect.x()
        y = option.rect.y()
        height = option.rect.height() - 1
        width = option.rect.width() - 1

        # Set a transparent pen for drawing rectangle (no border)
        painter.setPen(self._pen_border)

        # Set brush
        if not self._selected and not self._is_down:
            if not self._hover:
                painter.setBrush(self._brushes[self.DEFAULT])
            else:
                painter.setBrush(self._brushes[self.HOVER])
        elif self._selected and not self._is_down:
            if not self._hover:
                painter.setBrush(self._brushes[self.SELECTED])
            else:
                painter.setBrush(self._brushes[self.SELECTED_HOVER])
        elif self._is_down:
            painter.setBrush(self._brushes[self.DOWN])
        else:
            painter.setBrush(self._brushes[self.DEFAULT])

        # Draw background rectangle
        painter.drawRect(qc.QRect(x+1, y+1, width-1, height - 1))

        # Draw Pixmap Icon
        if self._icon_pixmap is not None and self._icon_size > 0:
            painter.drawPixmap(qc.QRect(x+self.indent_width+8, y+(self._icon_size/10),
                                        self._icon_size, self._icon_size), self._icon_pixmap)

        # Draw Text
        painter.setPen(self._pen_text)
        painter.drawText(x+self.indent_width+self._icon_size+16, y, width, height,
                         (qc.Qt.AlignLeft | qc.Qt.AlignVCenter), self._text)

        if self.parent_item is not None:
            parent_text = self.parent_item._text
        else:
            parent_text = 'world'
        painter.drawText(x + self.indent_width + self._icon_size + 80, y, width, height,
                         (qc.Qt.AlignLeft | qc.Qt.AlignVCenter), parent_text)

        if self._drag_hover_lower:
            painter.setPen(self._pen_line)
            painter.drawLine(0, height, width, height)

    # ---------------------------------------------------------------------------------------------------------------- #
    # ---------------------------------------------------------------------------------------------------------------- #
    # Mouse/Drag Events
    # ---------------------------------------------------------------------------------------------------------------- #
    # ---------------------------------------------------------------------------------------------------------------- #
    def mousePressEvent(self, event):
        """
        Overrides widget's mousePressEvent. Used to enable dragging functionality when the middle
        mouse button is held down.

        :param event
        """
        # DRAG FUNCTIONALITY -------------------------------------#
        if event.button() == qc.Qt.LeftButton:
            self._is_down = True
            self.update()
        elif event.button() == qc.Qt.MidButton and self.drag_enabled:
            item_mime_data = qc.QMimeData()
            item_drag = qg.QDrag(self)
            item_drag.setMimeData(item_mime_data)
            item_drag.exec_(qc.Qt.CopyAction | qc.Qt.MoveAction, qc.Qt.CopyAction)

    def mouseReleaseEvent(self, event):
        """
        Overrides QWidget's mouseReleaseEvent to enable item selection and update the self._selected variable

        :param event
        """
        self._is_down = False

        if event.button() == qc.Qt.LeftButton:
            mouse_pos = event.pos()
            if self.rect().contains(mouse_pos):
                self.clicked.emit()

        self.update()

    def enterEvent(self, event):
        """
        Overrides QWidget's enterEvent. Fires every time mouse enters widget area.
        Sets the widget's state to be hover

        :param event:
        """
        self._hover = True
        self.update()

    def leaveEvent(self, event):
        """
        Overrides QWidget's leaveEvent. Fires every time mouse leaves widget area
        Sets hover state to False

        :param event:
        """
        self._hover = False
        self.update()

    def dragEnterEvent(self, event):
        """
        Overrides widgets default dragEnterEvent function and accepts the drag
        :param event:
        """
        if event.source() != self and self.drop_enabled:
            event.accept()

    def dragLeaveEvent(self, event):
        self.set_border_colour([0, 0, 0, 0])
        self._drag_hover_lower = False
        self.update()

    def dropEvent(self, event):
        """
        Overrides widgets default dropEvent function

        :param event:
        """

        if not self.drop_enabled:
            return

        dropped_widget = event.source()

        height = self.frameGeometry().height()
        pos_y = event.pos().y()

        h_section = height*0.30

        if pos_y < (height - h_section):
            self.received_drop.emit([dropped_widget, 0])
        else:
            self.received_drop.emit([dropped_widget, 1])

        # Clean up
        self.set_border_colour([0, 0, 0, 0])
        self._drag_hover_lower = False
        self.update()

        # Ideas:
        # Emit the dropped widget in a signal to the list

    def dragMoveEvent(self, event):
        """
        Overrides widgets default dragMoveEvent function

        :param event:
        """
        height = self.frameGeometry().height()

        pos_y = event.pos().y()
        h_section = height * 0.30

        if pos_y < (height - h_section):
            self.set_border_colour(self.COLOUR_HOVER_SELECTED)
        else:
            self._drag_hover_lower = True
            self.set_border_colour([0, 0, 0, 0])

        self.update()

# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# GROUP WIDGET
# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
class _GroupWidget(qg.QWidget):
    """
    To Write..
    """
    # SIGNALS
    clicked = qc.Signal()

    def __init__(self, parent=None):
        super(_GroupWidget, self).__init__(parent=parent)
