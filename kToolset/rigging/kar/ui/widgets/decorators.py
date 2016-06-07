import PySide.QtCore as qc
import PySide.QtGui as qg

class Heading(qg.QWidget):
    """
    To write..
    """

    def __init__(self, label, parent=None, font_size=15, bottom_spacing=5):
        super(Heading, self).__init__(parent=parent)

        self.setLayout(qg.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(2)

        self.lay_title_bar = qg.QHBoxLayout()
        self.lay_title_bar.setContentsMargins(0, 0, 0, 0)
        self.lay_title_bar.setSpacing(2)
        self.lay_title_bar.setAlignment(qc.Qt.AlignLeft)
        self.layout().addLayout(self.lay_title_bar)

        font_heading = qg.QFont()
        font_heading.setPixelSize(font_size)
        lb_heading = qg.QLabel(label)
        lb_heading.setFont(font_heading)
        self.lay_title_bar.addWidget(lb_heading)

        self.layout().addWidget(Separator(parent=self))
        self.layout().addSpacerItem(qg.QSpacerItem(bottom_spacing, bottom_spacing))



class Separator(qg.QFrame):
    """
    Line widget used to visually separate other widgets
    """

    STYLE_SHEET = """
QFrame#separator
{
    border:0px solid rgba(0, 0, 0, 255);
    background-color: rgba(40, 40, 40, 255);
    max-height:1px;
    border-bottom:1px solid rgba(100, 100, 100, 255);
}
"""

    def __init__(self, is_vertical=False, parent=None):
        super(Separator, self).__init__(parent=parent)

        self.setObjectName('separator')
        self.setStyleSheet(self.STYLE_SHEET)

        if not is_vertical:
            self.setFrameStyle(qg.QFrame.HLine)
        else:
            self.setFrameStyle(qg.QFrame.VLine)
