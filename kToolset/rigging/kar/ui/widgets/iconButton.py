import PySide.QtCore as qc
import PySide.QtGui as qg


class IconButton(qg.QAbstractButton):
    """
    Button widget that displays an icon instead of text
    """
    def __init__(self, pixmap, pixmap_hover, pixmap_pressed=None, icon_size=(32,32), parent=None):
        super(IconButton, self).__init__(parent=parent)

        self.setFixedSize(icon_size[0]+2, icon_size[1]+2)

        self.icon_size = icon_size

        self.pixmap = pixmap
        self.pixmap_hover = pixmap_hover
        if pixmap_pressed is not None:
            self.pixmap_pressed = pixmap_pressed
        else:
            self.pixmap_pressed = pixmap_hover

        self.pressed.connect(self.update)
        self.released.connect(self.update)

    def paintEvent(self, event):
        icon_pixmap = self.pixmap_hover if self.underMouse() else self.pixmap
        if self.isDown():
            icon_pixmap = self.pixmap_pressed

        painter = qg.QPainter(self)
        painter.drawPixmap(qc.QRect(0, 0, self.icon_size[0], self.icon_size[1]+1), icon_pixmap)

    def enterEvent(self, event):
        self.update()

    def leaveEvent(self, event):
        self.update()