# Python Imports
import inspect

# PySide Imports
import PySide.QtCore as qc
import PySide.QtGui as qg

def get_style_sheet(file_name):
    """
    To write..
    :param file_name:
    :return:
    """
    full_path = inspect.stack()[0][1]
    print full_path
    split_path = r"\kar"
    #style_sheet_path = r'C:/Users/kaine.vangemer/Documents/maya/scripts\kToolset\kToolset\rigging\kar\ui\stylesheets\stylesheet_tabWidget.qss' #full_path.split(split_path, 1)[0] + split_path + '\ui\stylesheets\%s.qcc' % file_name
    style_sheet_path = full_path.split(split_path, 1)[0] + split_path + '\ui\stylesheets\%s.qss' % file_name
    style_sheet_file = qc.QFile(style_sheet_path)
    style_sheet_file.open(qc.QFile.ReadOnly)
    style_sheet = str(style_sheet_file.readAll())
    print style_sheet_path

    return style_sheet