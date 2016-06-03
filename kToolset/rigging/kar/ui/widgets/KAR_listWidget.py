# Python Imports
import uuid
# PySide Imports
import PySide.QtCore as qc
import PySide.QtGui as qg

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

    def __init__(self, parent=None):
        super(ListWidget, self).__init__(parent=parent)

        self._multi_select = True
        self._item_display_state = 0  # 0 = No Icons, 1 = Small Icons, 2 = Large Icons

        self._items = []
        self._selected_indices = []

        # Master Widget Layout
        self.setLayout(qg.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

        # Create Scroll Area for list
        self.scroll_area = qg.QScrollArea()
        self.scroll_area.setFocusPolicy(qc.Qt.NoFocus)
        self.scroll_area.setWidgetResizable(True)
        self.layout().addWidget(self.scroll_area)

        # List widget
        self.list_widget = qg.QWidget()
        self.list_widget.setLayout(qg.QVBoxLayout())
        self.list_widget.layout().setContentsMargins(0, 0, 0, 0)
        self.list_widget.layout().setSpacing(0)
        self.list_widget.layout().setAlignment(qc.Qt.AlignTop)

        self.scroll_area.setWidget(self.list_widget)

    def add_item(self, label, icon_pixmap, data, parent=None):
        item = _ItemWidget(label, icon_pixmap, data, parent=self)
        self._items.append(item)
        self.list_widget.addWidget(item)
        item.set_parent(parent)

    # ---------------------------------------------------------------------------------------------------------------- #
    # ---------------------------------------------------------------------------------------------------------------- #
    # List Order Functions
    # ---------------------------------------------------------------------------------------------------------------- #
    # ---------------------------------------------------------------------------------------------------------------- #
    def move_item(self, item_id, index):
        pass

    def get_order(self):
        """
        Returns a list of UUIDs from index 0-n in the current display order, with index 0 being the top most list item
        and index n being the bottom most list item
        """
        return [item.uuid for item in self._items]






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
    parent_changed = qg.Signal()

    # CONSTANTS
    INDENT = 16

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

    _pen_clear = qg.QPen(qg.QColor(0, 0, 0, 0), 1, qc.Qt.SolidLine)

    def __init__(self, label, icon_pixmap, data, parent=None):
        super(_ItemWidget, self).__init__(parent=parent)

        # Text Pen
        self._pen_text = qg.QPen(qg.QColor(250, 252, 255), 1, qc.Qt.SolidLine)

        # IDENTIFIER
        self.uuid = uuid.uuid4()

        self._text = label
        self._icon_pixmap = icon_pixmap
        self._data = data

        # Widget Settings
        self.setAcceptDrops(True)

        # Hierarchy
        self._parent = None
        self._children = []
        self.indent_width = self.get_indent_from_parent()

        # Button States
        self._hover = False
        self._is_down = False
        self._selected = False

        self._icon_size = 32

    def set_parent(self, parent):
        """
        Set the parent of item. This will move the item underneath the parent and apply
        the appropriate indentation

        :param parent: _ListWidget: Widget to set as parent
        """

        self._parent = parent

    def get_indent_from_parent(self):
        """
        Retrieves the parents indent level, increments it by 1 and returns the value
        """
        if self._parent is None:
            return 0
        else:
            try:
                indent = (self._parent.indent_level + 1) * self.INDENT
                return indent
            except AttributeError:
                return 0

    # ---------------------------------------------------------------------------------------------------------------- #
    # ---------------------------------------------------------------------------------------------------------------- #
    # Painting/Text
    # ---------------------------------------------------------------------------------------------------------------- #
    # ---------------------------------------------------------------------------------------------------------------- #
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

    def set_text(self, text):
        """
        Sets the list items display text

        :param text: Unicode string to display
        """
        if isinstance(text, unicode):
            self._text = text
            
            fm = qg.QFontMetrics(qg.QFont())
            text_width = fm.width(text)
            
            self.setMinimumWidth(self._icon_size+self.indent_width+text_width+16)

    def set_icon_state(self, state):
        """
        Sets the icon size given an integer.

        0 = No Icon
        1 = Small Icon (32px)
        2 = Large Icon (64px)

        :param state: Int:
        """
        if state is 1:
            self._icon_size = 32
            self.setFixedHeight(40)
        elif state is 2:
            self._icon_size = 64
            self.setFixedHeight(80)
        else:
            self._icon_size = 0
            self.setFixedHeight(20)

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
        painter.setPen(self._pen_clear)

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
            painter.drawPixmap(qc.QRect(x+8, y+(self._icon_size/10),
                                        self._icon_size, self._icon_size), self._icon_pixmap)

        # Draw Text
        painter.setPen(self._pen_text)
        painter.drawText(x+self.indent_width+self._icon_size+5, y, width, height,
                         (qc.Qt.AlignLeft | qc.Qt.AlignVCenter), self._text)

    # ---------------------------------------------------------------------------------------------------------------- #
    # ---------------------------------------------------------------------------------------------------------------- #
    # Mouse/Drag Events
    # ---------------------------------------------------------------------------------------------------------------- #
    # ---------------------------------------------------------------------------------------------------------------- #
    def dragEnterEvent(self, event):
        """
        Overrides widgets default dragEnterEvent function and accepts the drag
        :param event:
        """
        event.accept()

    def dropEvent(self, event):
        """
        Overrides widgets default dropEvent function

        :param event:
        """
        dropped_widget = event.source()

        # Ideas:
        # Emit the dropped widget in a signal to the list

    def mousePressEvent(self, event):
        """
        Overrides widget's mousePressEvent. Used to enable dragging functionality when the middle
        mouse button is held down.

        :param event
        """
        # DRAG FUNCTIONALITY -------------------------------------#
        if event.button() == qc.Qt.MidButton:
            item_mime_data = qc.QMimeData()
            item_drag = qg.QDrag(self)
            item_drag.setMimeData(item_mime_data)

    def mouseReleaseEvent(self, event):
        """
        Overrides QWidget's mouseReleaseEvent to enable item selection and update the self._selected variable

        :param event
        """
        self._is_down = False

        if event.button() == qc.Qt.LeftButton:
            mouse_pos = event.pos()
            if self.rect().contains(mouse_pos):
                self._selected = True
                self.clicked.emit()

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
