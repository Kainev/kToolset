# Python Imports
import inspect

# PySide Imports
import PySide.QtCore as qc
import PySide.QtGui as qg


def get_style_sheet(file_name):
    """
    Given a file name, returns the corresponding .qss stylesheet from the 'stylesheets' directory

    :param file_name: String: File name of stylesheet, WITHOUT EXTENSION
    :return: String: Stylesheet contents of given file name
    """
    full_path = inspect.stack()[0][1]
    split_path = r"\kar"
    style_sheet_path = full_path.split(split_path, 1)[0] + split_path + '\ui\stylesheets\%s.qss' % file_name
    style_sheet_file = qc.QFile(style_sheet_path)
    style_sheet_file.open(qc.QFile.ReadOnly)
    style_sheet = str(style_sheet_file.readAll())

    return style_sheet


def get_icon(file_name):
    """
    Given a file name, returns the corresponding .PNG image from the 'icons' directory as a QPixmap() object

    :param file_name: String: File name of icon, WITHOUT EXTENSION
    :return: QPixmap: QPixmap containing the specified .PNG image
    """

    full_path = inspect.stack()[0][1]
    print full_path
    split_path = r"\kar"
    icon_path = full_path.split(split_path, 1)[0] + split_path + '\ui\icons\%s.png' % file_name
    icon_pixmap = qg.QPixmap(icon_path)

    return icon_pixmap
